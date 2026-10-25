"""Recombine local program scores with unchanged saved LLM judgments."""
import argparse
import copy
import hashlib
import json
import statistics
import tempfile
from pathlib import Path

from openpyxl import load_workbook

from test_scoring_v2 import CRITERIA, FINALIZER, KEY, TASK, evaluate, program_details

REVISION = '评分器 v2（2026-10-26）'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def saved(path):
    backup = path.with_name(path.stem + '.v1' + path.suffix)
    return read_json(backup if backup.exists() else path)


def rescore_folder(folder, candidate, rubric_sha):
    original = saved(folder / 'judge.json')
    result = evaluate(candidate)
    program = program_details(result)
    original_details_path = folder / 'reward-details.v1.json'
    details = read_json(original_details_path) if original_details_path.exists() else {'reward': []}
    blocks = details['reward'] if isinstance(details['reward'], list) else [details['reward']]
    llm_blocks = [copy.deepcopy(block) for block in blocks if block.get('kind') != 'programmatic']
    assert all(item.get('name') in {'L01', 'L02', 'L03'} for block in llm_blocks for item in block.get('criteria', []))
    details['reward'] = [program] + llm_blocks
    pooled, counted, broken = FINALIZER.pooled_score(details)
    assert not broken
    completed = original.get('llm_status') == 'COMPLETED'
    if not completed:
        assert result['score'] == 0 and not llm_blocks
    final_score = round(pooled, 6)
    write_json(folder / 'reward-details.json', details)
    revision = {'label': REVISION, 'method': 'offline_program_rescore_with_saved_llm',
                'new_llm_calls': 0, 'saved_llm_complete': completed,
                'saved_llm_candidate_sha256': original.get('candidate_sha256'),
                'old_score': original['score_final'], 'new_score': final_score,
                'original_judgment': 'judge.v1.json',
                'limitation': '保存的 LLM 判定原样复用；不是新增模型运行或新增 LLM 裁判。'}
    reward = {'reward': final_score, 'graded_score': final_score,
              'criteria_counted': float(counted), 'verifier_error': 0.0,
              'programmatic_score': round(result['score'], 6),
              'llm_status': original.get('llm_status'), 'scoring_revision': revision}
    if not completed:
        reward['score_basis'] = '程序分上界为 0；尚未完成的 LLM 项均为负项，总分必为 0，未补造判定。'
    write_json(folder / 'reward.json', reward)
    llm_criteria = copy.deepcopy([item for item in original['criteria'] if item['criterion_id'].startswith('L')])
    program_criteria = [
        {'criterion_id': item['name'], 'score': item['raw'], 'evidence': item['evidence'],
         'sdk_value': item['value'], 'raw': item['raw'],
         'weight': -item['weight'] if item['negate'] else item['weight'],
         'negate': item['negate'], 'kind': 'programmatic', 'description': item['description'],
         'gate_reason': item['gate_reason'],
         'source_pointer': f'reward-details.json#/reward/0/criteria/{index}'}
        for index, item in enumerate(program['criteria'])]
    judge = copy.deepcopy(original)
    judge.update(candidate_sha256=digest(candidate), rubric_sha256=rubric_sha,
                 delivery_rubric_sha256=rubric_sha, criteria=program_criteria + llm_criteria,
                 positive_weight_total=51, score_final=final_score, reward=final_score,
                 graded_score=final_score, hybrid_score=final_score, criteria_counted=counted,
                 programmatic_score=round(result['score'], 6), scoring_revision=revision,
                 interface_gate_passed=result['interface_gate_passed'], interface_errors=result['interface_errors'],
                 reward_details_sha256=digest(folder / 'reward-details.json'))
    judge['weighted_sum'] = sum(item['weight'] * item['score'] for item in judge['criteria'] if item['score'] is not None)
    judge['raw_score'] = judge['weighted_sum'] / 51 if completed else None
    assert llm_criteria == [item for item in judge['criteria'] if item['criterion_id'].startswith('L')]
    write_json(folder / 'judge.json', judge)
    write_json(folder / 'programmatic_score.json', result)
    write_json(folder / 'extraction_v2.json', __import__('test_scoring_v2').ENGINE.extract(candidate, KEY))
    return {'old_score': original['score_final'], 'new_score': final_score,
            'programmatic_score': round(result['score'], 6), 'llm_status': original.get('llm_status'),
            'criteria_counted': counted}


def stats(values):
    return {'values': values, 'n': len(values), 'mean': statistics.mean(values),
            'min': min(values), 'max': max(values),
            'stddev_population': statistics.pstdev(values),
            'stddev_sample': statistics.stdev(values),
            'pass_stddev_lt_0_05': statistics.stdev(values) < 0.05}


def main(trace):
    root = TASK.parents[1]
    baseline = read_json(TASK / 'validation/revision_v2_baseline.json')
    for relative, expected in baseline['protected_files'].items():
        assert digest(root / relative) == expected, relative
    rubric_sha = digest(TASK / 'rubrics.json')
    summary = {'revision': REVISION, 'scores': {}, 'new_solver_runs': 0, 'new_llm_calls': 0}
    for folder in sorted(trace.rglob('judge.json')):
        folder = folder.parent
        label = saved(folder / 'judge.json')['candidate_label']
        candidate = trace / 'golden/candidate.xlsx' if label == 'golden' else trace / f'rollouts/{label}/candidate.xlsx'
        score = rescore_folder(folder, candidate, rubric_sha)
        if folder.parent.name != 'judge_runs':
            summary['scores'][label] = score
    consistency = saved(trace / 'consistency.json')
    consistency['unit'] = '同一参考答卷的程序重算，与五份已保存 LLM 判定分别重组；不是新增重复裁判。'
    for group in consistency['groups']:
        judges = [read_json(trace / f'judge_runs/{run_id}/judge.json') for run_id in group['run_ids']]
        group['total_score'] = stats([judge['score_final'] for judge in judges])
        group['criteria'] = []
        for item in judges[0]['criteria']:
            identifier = item['criterion_id']
            values = [next(criterion['score'] for criterion in judge['criteria']
                           if criterion['criterion_id'] == identifier) for judge in judges]
            group['criteria'].append({'criterion_id': identifier, 'weight': item['weight'],
                                      'kind': item['kind'], **stats(values)})
    consistency['scoring_revision'] = REVISION
    write_json(trace / 'consistency.json', consistency)
    discrimination = saved(trace / 'discrimination_cases.json')
    with tempfile.TemporaryDirectory(dir=TASK / 'validation') as temporary:
        candidate = Path(temporary) / 'partial.xlsx'
        for case in discrimination['cases']:
            book = load_workbook(TASK / 'solution/golden/answer.xlsx')
            for change in case['changed_cells']:
                sheet, address = change['cell'].split('!')
                book[sheet][address] = change['set_to']
            book.save(candidate)
            result = evaluate(candidate)
            case['programmatic_total'] = round(result['score'], 6)
            case['positive_credit'] = {identifier: verdict['credit'] for identifier, verdict in result['verdicts'].items()
                                       if verdict['weight'] > 0}
            case['penalties_triggered'] = [identifier for identifier, verdict in result['verdicts'].items()
                                           if verdict['weight'] < 0 and verdict['credit']]
    discrimination['method'] = '以修订后参考答案为底，按既有 changed_cells 重建七份部分正确控制卷并离线评分；仅程序子集，不对控制卷推定 LLM 违规或未违规。'
    discrimination['scoring_revision'] = REVISION
    discrimination['model_answers'] = {label: score['new_score'] for label, score in summary['scores'].items() if label != 'golden'}
    write_json(trace / 'discrimination_cases.json', discrimination)
    quality = saved(trace / 'quality_report.json')
    quality['rubric_sha256'] = rubric_sha
    quality['target'].update(sha256=digest(trace / 'golden/candidate.xlsx'), score_final=summary['scores']['golden']['new_score'])
    for model in quality['rollout_summary']['models']:
        model['score_final'] = summary['scores'][model['model']]['new_score']
    quality['judge']['score_basis'] = '程序判据按 v2 离线重算，LLM 逐条判定原样复用；无新增裁判。Opus 未完成的负项保留未完成，零分由程序上界推出。'
    quality['consistency']['status'] = 'RECOMPUTED_WITH_SAVED_JUDGMENTS'
    quality['consistency']['note'] = consistency['unit']
    quality['discrimination']['reference_score'] = summary['scores']['golden']['new_score']
    quality['discrimination']['model_scores'] = discrimination['model_answers']
    quality['discrimination']['partial_credit_cases']['totals'] = {case['case']: case['programmatic_total'] for case in discrimination['cases']}
    quality['scoring_revision'] = summary
    write_json(trace / 'quality_report.json', quality)
    for folder in [TASK, trace]:
        record = saved(folder / 'records.jsonl')
        record['scoring_revision'] = summary
        target = folder / record['target']['path']
        record['target'].update(bytes=target.stat().st_size, sha256=digest(target))
        (folder / 'records.jsonl').write_text(json.dumps(record, ensure_ascii=False) + '\n')
    golden_structure = read_json(trace / 'golden/structural_checks.json')
    golden_structure.update(candidate_sha256=digest(trace / 'golden/candidate.xlsx'),
                            programmatic_score=1.0, scoring_revision=REVISION)
    write_json(trace / 'golden/structural_checks.json', golden_structure)
    summary['golden_copy_count'] = len(baseline['golden_copies'])
    summary['negative_case_count'] = len(read_json(TASK / 'validation/negative_cases/cases.json')['cases'])
    summary['all_saved_llm_criteria_unchanged'] = True
    summary['instruction_and_model_workbooks_unchanged'] = True
    write_json(TASK / 'validation/scoring_v2_checks.json', summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trajectory_case', type=Path)
    main(parser.parse_args().trajectory_case)
