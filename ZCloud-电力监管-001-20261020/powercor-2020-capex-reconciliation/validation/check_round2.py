"""Check post-pooling policies through the delivered finalizer without model calls."""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    scorer = load_module('policy_scorer', ROOT / 'tests/score_output.py')
    finalizer = load_module('policy_finalizer', ROOT / 'tests/finalize.py')
    key = json.loads((ROOT / 'tests/results_key.json').read_text())
    criteria = key['rows'] + key['checks']
    outcomes = []
    for candidate in sorted((ROOT / 'validation').glob('*_cases/*.xlsx')):
        result = scorer.score(scorer.extract(candidate, key), key)
        entries = [{'name': item['criterion_id'], 'weight': abs(item['weight']),
                    'negate': item['weight'] < 0,
                    'value': 1 - result['verdicts'][item['criterion_id']]['credit'] if item['weight'] < 0
                    else result['verdicts'][item['criterion_id']]['credit']}
                   for item in criteria]
        entries += [{'name': name, 'weight': 3, 'negate': True, 'value': 1} for name in ['L01', 'L02', 'L03']]
        details = {'reward': {'kind': 'programmatic_policy_control', 'criteria': entries},
                   'score_policy': result['score_policy']}
        pooled, counted, broken = finalizer.pooled_score(details)
        assert counted == 13 and broken == 0
        assert round(finalizer.apply_score_policy(pooled, result['score_policy']), 6) == result['score']
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            (folder / 'reward.json').write_text(json.dumps({'reward': pooled}))
            (folder / 'reward-details.json').write_text(json.dumps(details))
            subprocess.run([sys.executable, str(ROOT / 'tests/finalize.py'), '--graded',
                            str(folder / 'reward.json'), '--graded-rc', '0', '--out',
                            str(folder / 'final/reward.json')], check=True)
            receipt = json.loads((folder / 'final/reward.json').read_text())
            assert receipt['reward'] == result['score'] and not receipt['verifier_error'], candidate.name
            recorded = json.loads((folder / 'final/reward-details.json').read_text())
            assert recorded['score_policy'] == result['score_policy']
        outcomes.append({'case': candidate.stem, 'score': result['score'], 'finalizer_cli_passed': True})
    low = {'required_sheet_gate': {'triggered': False}, 'must_clause_cap': {'triggered': True}}
    assert finalizer.apply_score_policy(0.4, low) == 0.4
    low['required_sheet_gate']['triggered'] = True
    assert finalizer.apply_score_policy(1.0, low) == 0.0
    for value in [1, 1.2, 1.23, 1.234, 1.234567]:
        assert scorer.has_precision(value, 'General')
    assert scorer.has_precision(1.234567, '0.00')
    assert not scorer.has_precision('1.234', '0.000')
    report = {'status': 'PASS', 'finalizer_cli_cases': len(outcomes),
              'cap_never_increases_score': True, 'gate_overrides_full_pool': True,
              'precision_controls_passed': True, 'cases': outcomes}
    (ROOT / 'validation/round2_policy_checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'cases'}))


if __name__ == '__main__':
    main()
