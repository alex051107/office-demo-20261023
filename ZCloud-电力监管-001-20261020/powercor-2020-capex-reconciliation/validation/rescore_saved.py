"""Recombine deterministic workbook scores with the saved LLM judgments offline."""
import copy
import hashlib
import importlib.util
import json
import statistics
import sys
import tempfile
from pathlib import Path

import openpyxl

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT.parents[1] / (ROOT.parent.name + '-轨迹报告') / ROOT.name
VERSION = 'v2 (2026-10-26)'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def backup(path):
    saved = path.with_name(path.stem + '.v1' + path.suffix)
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
        result = results[label]
        details_path = folder / 'reward-details.json'
        old_details = json.loads(backup(details_path).read_text())
        old_judge = json.loads(backup(folder / 'judge.json').read_text())
        old_reward = json.loads(backup(folder / 'reward.json').read_text())
        blocks = old_details['reward']
        blocks = blocks if isinstance(blocks, list) else [blocks]
        saved_llm = [copy.deepcopy(block) for block in blocks if block['kind'] != 'programmatic']
        saved_ids = {criterion.get('name', criterion.get('id')) for block in saved_llm for criterion in block['criteria']}
        assert saved_ids == {'L01', 'L02', 'L03'}, (folder, saved_ids)
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
        details = {'reward': [{'kind': 'programmatic', 'score': result['score'], 'criteria': criteria}] + saved_llm}
        pooled, counted, broken = finalizer.pooled_score(details)
        assert broken == 0 and counted == 13
        total = round(pooled, 6)
        assert result['interface_gate']['passed'] or total == 0
        assert details['reward'][1:] == saved_llm
        old_llm_criteria = [copy.deepcopy(item) for item in old_judge['criteria'] if item['criterion_id'].startswith('L')]
        assert len(old_llm_criteria) == 3
        judge_criteria += old_llm_criteria
        reward = copy.deepcopy(old_reward)
        reward.update(reward=total, graded_score=total, criteria_counted=float(counted), verifier_error=0.0)
        judge = copy.deepcopy(old_judge)
        weighted_sum = sum(item['weight'] * item['score'] for item in judge_criteria)
        judge.update(candidate_sha256=digest(candidates[label]), delivery_rubric_sha256=rubric_hash,
                     reward=total, score_final=total, graded_score=total, hybrid_score=total,
                     raw_score=total, weighted_sum=weighted_sum, criteria_counted=counted,
                     criteria=judge_criteria, llm_status='REUSED_SAVED_JUDGMENTS')
        judge['offline_rescore'] = {
            'scorer_version': VERSION, 'programmatic_score': result['score'], 'interface_gate': result['interface_gate'],
            'old_reward': old_reward['reward'], 'new_reward': total,
            'saved_llm_candidate_sha256': old_judge['candidate_sha256'],
            'saved_llm_details': 'reward-details.v1.json', 'new_llm_calls': 0,
            'scope': 'New programmatic checks; saved L01-L03 reused unchanged, not a new LLM evaluation.',
        }
        write_json(details_path, details)
        judge['reward_details_sha256'] = digest(details_path)
        write_json(folder / 'judge.json', judge)
        write_json(folder / 'reward.json', reward)
        judges[folder.name] = judge
        updated.append({'path': folder.relative_to(TRACE).as_posix(), 'candidate': label,
                        'old_score': old_reward['reward'], 'new_score': total,
                        'programmatic_score': result['score'], 'interface_gate': result['interface_gate']})
    consistency_path = TRACE / 'consistency.json'
    consistency = json.loads(backup(consistency_path).read_text())
    consistency['saved_llm_candidate_sha256'] = consistency['reference_candidate_sha256']
    consistency['reference_candidate_sha256'] = digest(candidates['golden'])
    consistency['scorer_version'] = VERSION
    consistency['unit'] = 'offline recombination of one fixed candidate with five saved judge jobs; no new solver or LLM runs'
    for group in consistency['groups']:
        runs = [judges[run_id] for run_id in group['run_ids']]
        def stats(values):
            return {'scores': values, 'n': len(values), 'mean': statistics.mean(values), 'min': min(values), 'max': max(values),
                    'stddev_population': statistics.pstdev(values), 'stddev_sample': statistics.stdev(values),
                    'pass_stddev_lt_0_05': statistics.stdev(values) < 0.05}
        group['total_score'] = stats([run['reward'] for run in runs])
        group['criteria'] = []
        for item in rubric['items']:
            criterion_id = item['id']
            values = [next(criterion['score'] for criterion in run['criteria'] if criterion['criterion_id'] == criterion_id) for run in runs]
            entry = {'criterion_id': criterion_id, 'kind': 'agent' if criterion_id.startswith('L') else 'programmatic',
                     'weight': item['weight'], **stats(values)}
            entry['values'] = entry.pop('scores')
            group['criteria'].append(entry)
        group['failed_criteria'] = [entry['criterion_id'] for entry in group['criteria'] if not entry['pass_stddev_lt_0_05']]
        group['criterion_requirement_status'] = 'PASS' if not group['failed_criteria'] else 'FAIL'
    consistency['status'] = 'PASS' if all(group['criterion_requirement_status'] == 'PASS' for group in consistency['groups']) else 'FAIL'
    consistency['limitations'].append('v2程序离线复算，沿用每次既有LLM判定；修订金标没有重新请求LLM审查。')
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
    discrimination['model_answers'] = {label: result['score'] for label, result in results.items() if label != 'golden'}
    write_json(discrimination_path, discrimination)
    quality_path = TRACE / 'quality_report.json'
    quality = json.loads(backup(quality_path).read_text())
    quality['rubric_sha256'] = rubric_hash
    quality['scorer_version'] = VERSION
    quality['target'].update(sha256=digest(candidates['golden']), score_final=judges['golden']['reward'])
    quality['judge']['score_basis'] = 'v2程序离线复算后，按finalize.py池化原有每份答卷第1次LLM判定；无新增调用。'
    quality['judge']['llm_status'] = 'REUSED_SAVED_JUDGMENTS'
    for model in quality['rollout_summary']['models']:
        model['score_final'] = judges[model['model']]['reward']
        model['scorer_version'] = VERSION
    quality['rollout_summary']['average_score'] = statistics.mean(model['score_final'] for model in quality['rollout_summary']['models'])
    quality['consistency']['status'] = consistency['status']
    for entry, group in zip(quality['consistency']['groups'], consistency['groups']):
        entry['total_scores'] = group['total_score']['scores']
        entry['total_stddev_sample'] = group['total_score']['stddev_sample']
        entry['max_criterion_stddev_sample'] = max(item['stddev_sample'] for item in group['criteria'])
    quality['discrimination']['reference_score'] = judges['golden']['reward']
    quality['discrimination']['model_scores'] = discrimination['model_answers']
    quality['discrimination']['partial_credit_cases']['totals'] = {case['case']: case['programmatic_total'] for case in discrimination['cases']}
    quality['limitations'].append('v2金标仅更新阅读呈现和解释；新的程序评分已运行，LLM条款及历史判定未变，不宣称重新完成LLM验收。')
    write_json(quality_path, quality)
    for root in [ROOT, TRACE]:
        record_path = root / 'records.jsonl'
        records = [json.loads(line) for line in backup(record_path).read_text().splitlines() if line.strip()]
        for record in records:
            record['scorer_version'] = VERSION
            record['reference_sha256'] = digest(candidates['golden'])
            if 'golden' in record:
                record['golden']['reward'] = judges['golden']['reward']
                for rollout in record['rollouts']:
                    label = Path(rollout['path']).parts[1]
                    rollout['reward'] = judges[label]['reward']
        record_path.write_text(''.join(json.dumps(record, ensure_ascii=False) + '\n' for record in records))
    summary = {'scorer_version': VERSION, 'new_model_calls': 0, 'new_judge_calls': 0,
               'score_source': 'tests/finalize.py pooled_score, with saved L01-L03 blocks unchanged',
               'rescored': updated, 'consistency_status': consistency['status']}
    write_json(TRACE / 'validation/rescore_summary.json', summary)
    print(json.dumps({'rescored_score_sets': len(updated), 'primary_scores': {label: judges[label]['reward'] for label in candidates},
                      'consistency': consistency['status']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
