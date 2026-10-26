"""Recombine current program scores with fresh golden or saved model judgments."""
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
    round1 = path.with_name(path.stem + '.round1' + path.suffix)
    backup = round1 if round1.exists() else path.with_name(path.stem + '.v1' + path.suffix)
    return read_json(backup if backup.exists() else path)


def rescore_folder(folder, candidate, rubric_sha, fresh=None):
    original = saved(folder / 'judge.json')
    result = evaluate(candidate)
    program = program_details(result)
    original_details_path = folder / 'reward-details.round1.json'
    if not original_details_path.exists():
        original_details_path = folder / 'reward-details.v1.json'
    if fresh is not None:
        original_details_path = fresh / 'reward-details.json'
    details = read_json(original_details_path) if original_details_path.exists() else {'reward': []}
    blocks = details['reward'] if isinstance(details['reward'], list) else [details['reward']]
    llm_blocks = [copy.deepcopy(block) for block in blocks if block.get('kind') != 'programmatic']
    assert all(item.get('name') in {'L01', 'L02', 'L03'} for block in llm_blocks for item in block.get('criteria', []))
    details = {'reward': [program] + llm_blocks, 'score_rules': result['score_rules']}
    pooled, counted, broken = FINALIZER.pooled_score(details)
    assert not broken
    completed = fresh is not None or original.get('llm_status') == 'COMPLETED'
    if not completed:
        assert result['score'] == 0 and not llm_blocks
    final_score = round(FINALIZER.apply_score_rules(pooled, result), 6)
    details['pooling'] = {'before_rules': pooled, 'after_rules': final_score}
    write_json(folder / 'reward-details.json', details)
    revision = {'label': REVISION, 'method': 'offline_program_rescore_with_saved_llm',
                'round': 2, 'new_llm_calls': int(fresh is not None), 'saved_llm_complete': completed,
                'saved_llm_candidate_sha256': original.get('candidate_sha256'),
                'old_score': original['score_final'], 'new_score': final_score,
                'original_judgment': 'judge.round1.json' if (folder / 'judge.round1.json').exists() else 'judge.v1.json',
                'llm_judgment_origin': 'new_real_golden' if fresh else 'saved_historical',
                'limitation': '金标使用本轮真实裁判；模型答卷只复用保存判定，未新增求解运行。' if fresh else '保存的 LLM 判定原样复用；金标此分仅为历史判定重组，不能替代本轮五次新裁判。'}
    if fresh is not None:
        assert read_json(fresh / 'reward.json')['verifier_error'] == 0
        assert read_json(fresh / 'run_metadata.json')['cost_guard_passed']
        revision['method'] = 'current_program_with_new_real_golden_judgment'
    reward = {'reward': final_score, 'graded_score': final_score,
              'criteria_counted': float(counted), 'verifier_error': 0.0,
              'programmatic_score': round(result['score'], 6),
              'llm_status': 'COMPLETED' if completed else original.get('llm_status'), 'scoring_revision': revision}
    if not completed:
        reward['score_basis'] = '程序分上界为 0；尚未完成的 LLM 项均为负项，总分必为 0，未补造判定。'
    write_json(folder / 'reward.json', reward)
    llm_criteria = copy.deepcopy([item for item in original['criteria'] if item['criterion_id'].startswith('L')])
    if fresh is not None:
        llm_criteria = [
            {'criterion_id': item.get('name', item.get('id')), 'score': 1.0 - item['value'],
             'evidence': None, 'reason': item.get('reasoning'), 'sdk_value': item['value'],
             'raw': item.get('raw'), 'weight': -item['weight'], 'negate': True, 'kind': 'agent',
             'description': item['description'],
             'source_pointer': f'reward-details.json#/reward/{block_index + 1}/criteria/{item_index}'}
            for block_index, block in enumerate(llm_blocks)
            for item_index, item in enumerate(block['criteria'])]
        assert {item['criterion_id'] for item in llm_criteria} == {'L01', 'L02', 'L03'}
        assert read_json(fresh / 'reward.json')['criteria_counted'] == 20
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
                 header_errors=result['header_errors'], score_rules=result['score_rules'],
                 reward_details_sha256=digest(folder / 'reward-details.json'))
    judge['weighted_sum'] = sum(item['weight'] * item['score'] for item in judge['criteria'] if item['score'] is not None)
    judge['raw_score'] = judge['weighted_sum'] / 51 if completed else None
    if fresh is not None:
        receipt = read_json(fresh / 'run_metadata.json')
        judge.update(started_at=receipt['started_at'], finished_at=receipt['finished_at'],
                     source_run=folder.name, llm_status='COMPLETED', judge_completed=True,
                     provider_response_id=None, usage={'account_usage_delta_usd': receipt['account_usage_delta_usd']},
                     selection_policy='golden_r1 selected before comparison; five new sequential judgments',
                     raw_response=json.dumps({item['criterion_id']: {'score': item['raw'], 'reasoning': item['reason']}
                                              for item in llm_criteria}, ensure_ascii=False))
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


def main(trace, fresh_root=None):
    root = TASK.parents[1]
    baseline = read_json(TASK / 'validation/revision_v2_baseline.json')
    for relative, expected in baseline['protected_files'].items():
        assert digest(root / relative) == expected, relative
    rubric_sha = digest(TASK / 'rubrics.json')
    attempt_status = read_json(trace / 'judge_runs/golden_round2_status.json')
    summary = {'revision': REVISION, 'round': 2, 'scores': {}, 'new_solver_runs': 0,
               'new_llm_calls': attempt_status['attempted_runs'],
               'new_valid_golden_judgments': 5 if fresh_root else 0,
               'golden_judgment_status': 'COMPLETED' if fresh_root else attempt_status['status'],
               'golden_score_basis': 'new_real_judgments' if fresh_root else 'provisional_saved_historical_judgments'}
    for folder in sorted(trace.rglob('judge.json')):
        folder = folder.parent
        label = saved(folder / 'judge.json')['candidate_label']
        candidate = trace / 'golden/candidate.xlsx' if label == 'golden' else trace / f'rollouts/{label}/candidate.xlsx'
        fresh = fresh_root / (folder.name if folder.parent.name == 'judge_runs' else 'golden_r1') if fresh_root and label == 'golden' else None
        score = rescore_folder(folder, candidate, rubric_sha, fresh)
        if folder.parent.name != 'judge_runs':
            summary['scores'][label] = score
    consistency = saved(trace / 'consistency.json')
    consistency['unit'] = '同一修订后参考答卷与当前程序判据，五次独立真实 LLM 裁判；模型答卷判定未重跑。' if fresh_root else '程序重算与保存判定重组。'
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
    consistency['round2_golden_judgments'] = attempt_status
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
            case['score_rules'] = result['score_rules']
            case['positive_credit'] = {identifier: verdict['credit'] for identifier, verdict in result['verdicts'].items()
                                       if verdict['weight'] > 0}
            case['penalties_triggered'] = [identifier for identifier, verdict in result['verdicts'].items()
                                           if verdict['weight'] < 0 and verdict['credit']]
    discrimination['method'] = '以修订后参考答案为底，按既有 changed_cells 重建七份部分正确控制卷并离线评分；仅程序子集，不对控制卷推定 LLM 违规或未违规。'
    discrimination['scoring_revision'] = REVISION
    discrimination['round'] = 2
    discrimination['golden_hybrid_score_basis'] = summary['golden_score_basis']
    discrimination['model_answers'] = {label: score['new_score'] for label, score in summary['scores'].items() if label != 'golden'}
    write_json(trace / 'discrimination_cases.json', discrimination)
    quality = saved(trace / 'quality_report.json')
    quality['rubric_sha256'] = rubric_sha
    quality['target'].update(sha256=digest(trace / 'golden/candidate.xlsx'), score_final=summary['scores']['golden']['new_score'])
    quality['target']['score_status'] = 'NEW_REAL_JUDGMENTS' if fresh_root else 'PROVISIONAL_SAVED_JUDGMENTS'
    for model in quality['rollout_summary']['models']:
        model['score_final'] = summary['scores'][model['model']]['new_score']
    quality['judge']['score_basis'] = '第二轮程序评分；金标五次新真实 LLM 裁判，模型保存的判定原样复用。' if fresh_root else '第二轮程序评分与保存的历史 LLM 判定重组；金标五次新裁判因费用停止而未完成，金标总分仅为暂定重组值。'
    quality['judge']['formula'] = 'signed-weight pooling / 51, clipped to [0,1], then required_sheet_gate=0, required_header_cap<=0.69, must_clause_cap<=0.69'
    quality['judge']['round2_golden_judgments'] = attempt_status
    quality['consistency']['status'] = 'FIVE_NEW_GOLDEN_JUDGMENTS' if fresh_root else 'BLOCKED_NEW_GOLDEN_JUDGMENTS'
    quality['consistency']['note'] = consistency['unit']
    quality['consistency']['groups'] = [
        {'candidate': group['candidate_label'], 'repeats': len(group['run_ids']),
         'total_scores': group['total_score']['values'],
         'total_stddev_sample': group['total_score']['stddev_sample'],
         'max_criterion_stddev_sample': max(item['stddev_sample'] for item in group['criteria']),
         'pass_stddev_lt_0_05': group['total_score']['pass_stddev_lt_0_05'] and all(item['pass_stddev_lt_0_05'] for item in group['criteria']),
         'judgment_origin': 'new_real_golden' if fresh_root else 'saved_historical'}
        for group in consistency['groups']]
    quality['discrimination']['reference_score'] = summary['scores']['golden']['new_score']
    quality['discrimination']['model_scores'] = discrimination['model_answers']
    quality['discrimination']['partial_credit_cases']['totals'] = {case['case']: case['programmatic_total'] for case in discrimination['cases']}
    quality['scoring_revision'] = summary
    quality['limitations'] = [note for note in quality['limitations'] if not note.startswith('rubrics.json 在评分后')]
    quality['limitations'].extend([
        '第二轮保留 20 个判据及全部权重，更新程序判据描述与汇总规则；judge.json 记录当前交付 rubric 的哈希。',
        '本轮金标仅 1 次真实尝试、0 次有效完成；费用超限后停止。五次新真实裁判与其逐项及总分标准差尚未完成。'])
    quality['overall_delivery_compliance'] = 'PARTIAL_ROUND2_GOLDEN_JUDGMENTS_BLOCKED_COST_GUARD'
    write_json(trace / 'quality_report.json', quality)
    for folder in [TASK, trace]:
        record = saved(folder / 'records.jsonl')
        record['scoring_revision'] = summary
        target = folder / record['target']['path']
        record['target'].update(bytes=target.stat().st_size, sha256=digest(target))
        if 'rubric' in record and 'sha256' in record['rubric']:
            record['rubric']['sha256'] = rubric_sha
        (folder / 'records.jsonl').write_text(json.dumps(record, ensure_ascii=False) + '\n')
    golden_structure = read_json(trace / 'golden/structural_checks.json')
    golden_structure.update(candidate_sha256=digest(trace / 'golden/candidate.xlsx'),
                            programmatic_score=1.0, scoring_revision=REVISION)
    write_json(trace / 'golden/structural_checks.json', golden_structure)
    summary['golden_copy_count'] = len(baseline['golden_copies'])
    cases = read_json(TASK / 'validation/negative_cases/cases.json')['cases']
    summary['negative_case_count'] = sum(case['category'] == 'negative' for case in cases)
    summary['positive_control_count'] = sum(case['category'] == 'positive_control' for case in cases)
    summary['all_saved_model_llm_criteria_unchanged'] = True
    summary['instruction_and_model_workbooks_unchanged'] = True
    write_json(TASK / 'validation/scoring_v2_checks.json', summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trajectory_case', type=Path)
    parser.add_argument('--fresh-golden-root', type=Path)
    args = parser.parse_args()
    main(args.trajectory_case, args.fresh_golden_root)
