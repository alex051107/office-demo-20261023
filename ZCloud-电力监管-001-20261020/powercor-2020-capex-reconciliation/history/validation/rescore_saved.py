"""Recombine round-2 program checks with original valid saved golden judgments offline."""
import copy
import hashlib
import importlib.util
import json
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

import openpyxl

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT.parents[1] / (ROOT.parent.name + '-轨迹报告') / ROOT.name
VERSION = 'v2 (2026-10-26)'
NOTE = '新版金标文字未重新裁判；沿用原有效文字判定'
ARCHIVE = 'golden/rejudge_attempts_20261026'
PROVENANCE = {'score_status': 'PROVISIONAL', 'score_note': NOTE,
              'score_revision': 'round3_golden_record_correction',
              'score_basis': 'round2_program_plus_original_valid_saved_llm',
              'new_llm_calls': 0, 'invalid_attempt_archive': ARCHIVE,
              'invalid_attempt_archive_path_base': 'trajectory_case_root'}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def backup(path):
    saved = path.with_name(path.stem + '.v1' + path.suffix)
    if saved.exists():
        saved = path.with_name(path.stem + '.round1' + path.suffix)
    if not saved.exists():
        saved.write_bytes(path.read_bytes())
    return saved


def write_json(path, value):
    if path.exists() and path.name in {
        'reward.json', 'reward-details.json', 'judge.json', 'quality_report.json',
        'consistency.json', 'discrimination_cases.json',
    }:
        backup(path)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    if len(sys.argv) != 1:
        raise SystemExit('Offline recombination accepts no new judge-result directory.')
    saved_runs = [f'golden_r{index}' for index in range(1, 6)]
    scorer = load_module('saved_rescore_engine', ROOT / 'tests/score_output.py')
    finalizer = load_module('saved_rescore_finalizer', ROOT / 'tests/finalize.py')
    key = json.loads((ROOT / 'tests/results_key.json').read_text())
    rubric = json.loads((ROOT / 'rubrics.json').read_text())
    program = key['rows'] + key['tables'] + key['checks']
    items = {item['id']: item for item in rubric['items']}
    rubric_hash = digest(ROOT / 'rubrics.json')
    candidates = {'golden': TRACE / 'golden/candidate.xlsx'}
    candidates.update({folder.name: folder / 'candidate.xlsx' for folder in (TRACE / 'rollouts').iterdir() if folder.is_dir()})
    results = {}
    for label, path in candidates.items():
        evidence = scorer.extract(path, key)
        results[label] = scorer.score(evidence, key)
        assert results[label]['status'] != 'JUDGE_ERROR'
    folders = [TRACE / 'golden'] + sorted((TRACE / 'rollouts').iterdir())
    folders += sorted(folder for folder in (TRACE / 'judge_runs').iterdir() if (folder / 'reward-details.json').exists())
    updated = []
    judges = {}
    for folder in folders:
        if not (folder / 'judge.json').exists():
            continue
        label = folder.name.split('_r')[0] if folder.parent.name == 'judge_runs' else folder.name
        if label != 'golden':
            judges[folder.name] = json.loads((folder / 'judge.json').read_text())
            continue
        result = results[label]
        assert result['score'] == result['signed_pooled_score'] == 1.0
        assert all(not rule['triggered'] for rule in result['score_policy'].values())
        details_path = folder / 'reward-details.json'
        old_details = json.loads((folder / 'reward-details.v1.json').read_text())
        old_judge = json.loads((folder / 'judge.v1.json').read_text())
        old_reward = json.loads((folder / 'reward.v1.json').read_text())
        assert old_reward['verifier_error'] == 0 and old_judge['judge_completed']
        blocks = old_details['reward']
        blocks = blocks if isinstance(blocks, list) else [blocks]
        saved_llm = [copy.deepcopy(block) for block in blocks if block['kind'] != 'programmatic']
        saved_ids = {criterion.get('name', criterion.get('id')) for block in saved_llm for criterion in block['criteria']}
        assert saved_ids == {'L01', 'L02', 'L03'}, (folder, saved_ids)
        assert not finalizer.count_errors({'reward': saved_llm})
        assert all(criterion['value'] == 1 and criterion['raw'] == 'no'
                   for block in saved_llm for criterion in block['criteria'])
        criteria = []
        judge_criteria = []
        for item in program:
            criterion_id = item['criterion_id']
            credit = result['verdicts'][criterion_id]['credit']
            value = 1 - credit if item['weight'] < 0 else credit
            criterion = {'name': criterion_id, 'weight': abs(item['weight']), 'negate': item['weight'] < 0,
                         'raw': credit, 'value': value, 'description': items[criterion_id]['description']}
            criteria.append(criterion)
            judge_criteria.append({'criterion_id': criterion_id, 'score': credit, 'sdk_value': value,
                                   'raw': credit, 'weight': item['weight'], 'negate': item['weight'] < 0,
                                   'kind': 'programmatic', 'description': items[criterion_id]['description'],
                                   'evidence': result['verdicts'][criterion_id]['evidence'],
                                   'source_pointer': f'reward-details.json#/reward/0/criteria/{len(criteria)-1}'})
        details = {'reward': [{'kind': 'programmatic', 'score': result['signed_pooled_score'], 'criteria': criteria}] + saved_llm,
                   'score_policy': result['score_policy']}
        pooled, counted, broken = finalizer.pooled_score(details)
        assert broken == 0 and counted == 13
        total = round(finalizer.apply_score_policy(pooled, result['score_policy']), 6)
        assert result['interface_gate']['passed'] or total == 0
        assert details['reward'][1:] == saved_llm
        old_llm_criteria = [copy.deepcopy(item) for item in old_judge['criteria'] if item['criterion_id'].startswith('L')]
        assert len(old_llm_criteria) == 3
        judge_criteria += old_llm_criteria
        reward = copy.deepcopy(old_reward)
        reward.update(reward=total, graded_score=total, signed_pooled_score=round(pooled, 6),
                      criteria_counted=float(counted), verifier_error=0.0)
        judge = copy.deepcopy(old_judge)
        weighted_sum = sum(item['weight'] * item['score'] for item in judge_criteria)
        judge.update(candidate_sha256=digest(candidates[label]), delivery_rubric_sha256=rubric_hash,
                     reward=total, score_final=total, graded_score=total, hybrid_score=total,
                     raw_score=total, weighted_sum=weighted_sum, criteria_counted=counted,
                     criteria=judge_criteria, llm_status='REUSED_VALID_SAVED_JUDGMENTS')
        judge['score_policy'] = result['score_policy']
        judge['offline_rescore'] = {
            'scorer_version': VERSION, 'programmatic_score': result['score'], 'interface_gate': result['interface_gate'],
            'old_reward': old_reward['reward'], 'new_reward': total,
            'saved_llm_candidate_sha256': old_judge['candidate_sha256'],
            'saved_llm_details': 'reward-details.v1.json',
            'new_llm_calls': 0,
            'saved_llm_judge': 'judge.v1.json', 'saved_llm_run_id': old_judge['source_run'],
            'scope': NOTE,
        }
        details.update(PROVENANCE)
        reward.update(PROVENANCE)
        reward.update(programmatic_score=result['score'], score_policy=result['score_policy'])
        judge.update(PROVENANCE)
        judge['status'] = 'PROVISIONAL'
        judge['limitations'] = [
            'rubric_sha256保留原有效文字判定的历史绑定；delivery_rubric_sha256为当前第二轮规则。程序判据和容差按当前规则重算，LLM判定来自已保存历史明细，不追认其已裁判新版文字。'
            if '评分条目、权重和容差一致' in limitation else limitation
            for limitation in old_judge.get('limitations', [])
        ] + [NOTE]
        write_json(details_path, details)
        judge['reward_details_sha256'] = digest(details_path)
        write_json(folder / 'judge.json', judge)
        write_json(folder / 'reward.json', reward)
        judges[folder.name] = judge
        updated.append({'path': folder.relative_to(TRACE).as_posix(), 'candidate': label,
                        'old_score': old_reward['reward'], 'new_score': total,
                        'programmatic_score': result['score'], 'interface_gate': result['interface_gate']})
    finalizer_dir = ROOT / 'validation/finalizer/golden'
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        graded = temporary / 'reward.json'
        graded.write_text('{"reward": 1.0}\n')
        (temporary / 'reward-details.json').write_bytes((TRACE / 'golden/reward-details.json').read_bytes())
        output = temporary / 'finalized/reward.json'
        subprocess.run([sys.executable, str(ROOT / 'tests/finalize.py'), '--graded', str(graded),
                        '--graded-rc', '0', '--out', str(output)], check=True)
        receipt = json.loads(output.read_text())
        assert receipt['reward'] == receipt['signed_pooled_score'] == 1.0
        assert receipt['criteria_counted'] == 13 and receipt['verifier_error'] == 0
        receipt.update(programmatic_score=1.0, score_policy=judges['golden']['score_policy'], **PROVENANCE)
        output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
        for name in ['reward.json', 'reward-details.json', 'reward.txt']:
            (finalizer_dir / name).write_bytes((output.parent / name).read_bytes())
    runtime_path = ROOT / 'validation/round2_runtime_checks.json'
    runtime = json.loads(runtime_path.read_text())
    golden_runtime = next(entry for entry in runtime['primary_candidates'] if entry['candidate'] == 'golden')
    golden_runtime.update(reward=receipt['reward'], criteria_counted=receipt['criteria_counted'],
                          verifier_error=receipt['verifier_error'], **PROVENANCE)
    runtime.update(golden_finalizer_recheck='PASS_OFFLINE_SAVED_VALID_LLM', new_judge_calls=0,
                   invalid_golden_attempt_report=ARCHIVE + '/task_validation/round2_runtime_checks.json')
    write_json(runtime_path, runtime)
    consistency_path = TRACE / 'consistency.json'
    consistency = json.loads(backup(consistency_path).read_text())
    consistency['saved_llm_candidate_sha256'] = judges['golden']['offline_rescore']['saved_llm_candidate_sha256']
    consistency['reference_candidate_sha256'] = digest(candidates['golden'])
    consistency['scorer_version'] = VERSION
    consistency['unit'] = 'Five original valid saved golden judgments recombined with round-2 program checks; no new judgments'
    consistency.update(PROVENANCE)
    for group in consistency['groups']:
        if group['run_ids'][0].startswith('golden_'):
            group['run_ids'] = saved_runs
            group.update(PROVENANCE)
            group.pop('unassessed_criteria', None)
        runs = [judges[run_id] for run_id in group['run_ids']]
        group['n'] = len(runs)
        def stats(values):
            return {'scores': values, 'n': len(values), 'mean': statistics.mean(values), 'min': min(values), 'max': max(values),
                    'stddev_population': statistics.pstdev(values) if len(values) > 1 else None,
                    'stddev_sample': statistics.stdev(values) if len(values) > 1 else None,
                    'pass_stddev_lt_0_05': statistics.stdev(values) < 0.05 if len(values) > 1 else None}
        group['total_score'] = stats([run['reward'] for run in runs])
        group['criteria'] = []
        for item in rubric['items']:
            criterion_id = item['id']
            values = [next(criterion['score'] for criterion in run['criteria'] if criterion['criterion_id'] == criterion_id) for run in runs]
            entry = {'criterion_id': criterion_id, 'kind': 'agent' if criterion_id.startswith('L') else 'programmatic',
                     'weight': item['weight'], **stats(values)}
            entry['values'] = entry.pop('scores')
            group['criteria'].append(entry)
        group['failed_criteria'] = [entry['criterion_id'] for entry in group['criteria'] if entry['pass_stddev_lt_0_05'] is False]
        group['criterion_requirement_status'] = 'PASS' if not group['failed_criteria'] else 'FAIL'
    consistency['status'] = 'PASS' if all(group['criterion_requirement_status'] == 'PASS' for group in consistency['groups']) else 'FAIL'
    consistency['limitations'] = [NOTE, 'σ仅描述原五次有效文字判定经现行程序判据重合成的稳定性，不证明新版金标文字已重新裁判。']
    write_json(consistency_path, consistency)
    discrimination_path = TRACE / 'discrimination_cases.json'
    discrimination = json.loads(backup(discrimination_path).read_text())
    with tempfile.TemporaryDirectory(dir=ROOT / 'validation') as temporary:
        for case in discrimination['cases']:
            workbook = openpyxl.load_workbook(candidates['golden'])
            for change in case['changed_cells']:
                sheet, coordinate = change['cell'].split('!')
                workbook[sheet][coordinate] = change['set_to']
            candidate = Path(temporary) / 'partial.xlsx'
            workbook.save(candidate)
            result = scorer.score(scorer.extract(candidate, key), key)
            case['programmatic_total'] = result['score']
            case['positive_credit'] = {item['criterion_id']: result['verdicts'][item['criterion_id']]['credit'] for item in key['rows']}
            case['penalties_triggered'] = [item['criterion_id'] for item in key['checks'] if result['verdicts'][item['criterion_id']]['credit']]
            workbook.close()
    discrimination['scorer_version'] = VERSION
    discrimination['method'] = '以参考答案为底，保留前k项正确结果，其余值乘1.25；用本轮程序评分器和独立后置规则计算。LLM按未违规作程序分对照，不调用模型或裁判，不据此认定金标LLM质量。'
    discrimination['model_answers'] = {label: result['score'] for label, result in results.items() if label != 'golden'}
    discrimination.update(reference_score=judges['golden']['reward'], reference_programmatic_score=1.0, **PROVENANCE)
    write_json(discrimination_path, discrimination)
    quality_path = TRACE / 'quality_report.json'
    quality = json.loads(backup(quality_path).read_text())
    quality['rubric_sha256'] = rubric_hash
    quality['scorer_version'] = VERSION
    quality['target'].update(sha256=digest(candidates['golden']), score_final=judges['golden']['reward'])
    quality['judge']['score_basis'] = NOTE
    quality['judge']['formula'] = 'round(apply_score_policy(clip((sum(w_i*q_i for w_i>0)-sum(abs(w_j)*v_j for w_j<0))/s_max,0,1),score_policy),6)'
    quality['judge']['llm_status'] = 'REUSED_VALID_SAVED_JUDGMENTS'
    quality['judge']['fresh_golden_runs'] = 0
    quality['judge']['saved_valid_golden_runs'] = 5
    quality['judge']['invalid_rejudge_attempts'] = 1
    quality['judge']['required_golden_runs'] = 5
    quality['judge']['semantic_reliability'] = 'Original valid judgments only; revised text not rejudged; contradictory attempt excluded.'
    quality['round2_status'] = 'PROGRAM_COMPLETE_GOLDEN_PROVISIONAL_SAVED_LLM'
    for model in quality['rollout_summary']['models']:
        model['score_final'] = judges[model['model']]['reward']
        model['scorer_version'] = VERSION
    quality['rollout_summary']['average_score'] = statistics.mean(model['score_final'] for model in quality['rollout_summary']['models'])
    quality['consistency']['status'] = consistency['status']
    for entry, group in zip(quality['consistency']['groups'], consistency['groups']):
        entry['total_scores'] = group['total_score']['scores']
        entry['repeats'] = group['n']
        entry['pass_stddev_lt_0_05'] = group['total_score']['pass_stddev_lt_0_05']
        entry['total_stddev_sample'] = group['total_score']['stddev_sample']
        samples = [item['stddev_sample'] for item in group['criteria'] if item['stddev_sample'] is not None]
        entry['max_criterion_stddev_sample'] = max(samples) if samples else None
    quality['discrimination']['reference_score'] = judges['golden']['reward']
    quality['discrimination']['note'] = NOTE + '；金标程序分1.0，合成分1.0；异常输出不计分。部分正确样例仅验证程序区分度。'
    quality['discrimination']['model_scores'] = discrimination['model_answers']
    quality['discrimination']['partial_credit_cases']['totals'] = {case['case']: case['programmatic_total'] for case in discrimination['cases']}
    quality['limitations'] = [entry for entry in quality['limitations'] if 'v2' not in entry and not entry.startswith('rubrics.json 在评分后只改过说明字段')]
    quality['limitations'].append('第二轮修改程序判据、派生容差与后置评分规则，保持各条权重和LLM文本不变；delivery_rubric_sha256记录当前导出，历史裁判rubric摘要保留用于追溯。')
    quality['limitations'].append(NOTE)
    quality.update(PROVENANCE)
    quality['target'].update(programmatic_score=1.0, **PROVENANCE)
    quality['consistency'].update(PROVENANCE)
    excluded = json.loads((TRACE / 'excluded_runs.json').read_text())
    historical_count = excluded.get('historical_incomplete_count', excluded['count'])
    excluded['reason_categories'] = list(dict.fromkeys(excluded['reason_categories'] + ['裁判判定与理由矛盾']))
    excluded.update(count=historical_count + 1, historical_incomplete_count=historical_count,
                    invalid_rejudge_count=1, invalid_rejudge_archive=ARCHIVE,
                    note=f'{historical_count}次历史超时/连接中断及1次判定与理由矛盾的金标裁判错误均排除；不作成绩或零分。')
    write_json(TRACE / 'excluded_runs.json', excluded)
    quality['excluded_judge_jobs'].update(count=excluded['count'], note=excluded['note'])
    write_json(quality_path, quality)
    for root in [ROOT, TRACE]:
        record_path = root / 'records.jsonl'
        records = [json.loads(line) for line in backup(record_path).read_text().splitlines() if line.strip()]
        for record in records:
            record.update(reference_score=judges['golden']['reward'], **PROVENANCE)
            record['scorer_version'] = VERSION
            record['reference_sha256'] = digest(candidates['golden'])
            if 'golden' in record:
                record['golden'].update(reward=judges['golden']['reward'], **PROVENANCE)
                for rollout in record['rollouts']:
                    label = Path(rollout['path']).parts[1]
                    rollout['reward'] = judges[label]['reward']
        metadata = json.loads((root / 'metadata/task_metadata.json').read_text())
        golden_group = next(group for group in consistency['groups'] if group['candidate_label'] == 'golden')
        metadata.update(reference_hybrid_score=judges['golden']['reward'],
                        reference_judge_mean=golden_group['total_score']['mean'],
                        reference_judge_stddev=golden_group['total_score']['stddev_sample'],
                        reference_judge_runs_completed=5, reference_judge_runs_required=5,
                        reference_judge_status='PROVISIONAL_SAVED_VALID_JUDGMENTS',
                        reference_fresh_valid_judge_runs=0, reference_invalid_judge_attempts=1,
                        scorer_version=VERSION, **PROVENANCE)
        write_json(root / 'metadata/task_metadata.json', metadata)
        record_path.write_text(''.join(json.dumps(record, ensure_ascii=False) + '\n' for record in records))
    run_metadata = json.loads((TRACE / 'golden/run_metadata.json').read_text())
    run_metadata.update(score_preserved=judges['golden']['reward'], this_export_paid_calls=0,
                        scorer_version=VERSION, status='PROVISIONAL_SAVED_VALID_JUDGMENTS',
                        saved_valid_judge_runs=5, fresh_valid_judge_runs=0, **PROVENANCE)
    write_json(TRACE / 'golden/run_metadata.json', run_metadata)
    write_json(TRACE / 'validation/golden_round2_judge_status.json', {
        'status': 'JUDGE_ERROR_EXCLUDED', 'is_score': False, 'valid_score': None, 'attempt_count': 1,
        'valid_fresh_runs': 0, 'included_in_statistics': False, 'count_as_zero': False,
        'reason': 'L01-L03均判yes违规，理由却称无违规且声称答卷不存在。',
        'raw_attempt': ARCHIVE, 'cost_guard_stopped': True, 'new_calls_this_correction': 0,
        'saved_valid_runs': saved_runs, 'representative_score': judges['golden']['reward'], **PROVENANCE})
    summary = {'scorer_version': VERSION, 'revision': 'round3_golden_record_correction',
               'new_model_calls': 0, 'new_judge_calls': 0, 'new_network_calls': 0,
               'golden_saved_valid_run_ids': saved_runs, 'golden_fresh_run_ids': [],
               'rescored': updated, 'consistency_status': consistency['status'], **PROVENANCE}
    write_json(TRACE / 'validation/rescore_summary.json', summary)
    print(json.dumps({'rescored_score_sets': len(updated), 'primary_scores': {label: judges[label]['reward'] for label in candidates},
                      'consistency': consistency['status']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
