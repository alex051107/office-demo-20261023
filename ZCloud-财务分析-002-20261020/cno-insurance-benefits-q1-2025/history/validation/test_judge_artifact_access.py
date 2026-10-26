"""Regression checks for candidate-access evidence and saved judgments."""
import argparse
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


TASK = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    finalizer = load('artifact_finalizer', TASK / 'tests/finalize.py')
    checker = load('artifact_checker', TASK / 'tests/llm_artifact_check.py')
    golden = TASK / 'solution/golden_output/answer.xlsx'
    blind = json.loads((TASK / 'validation/judge_fixtures/saved_blind.json').read_text())
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        graded = folder / 'graded/reward.json'
        graded.parent.mkdir()
        graded.write_text('{"programmatic": 1.0}')
        valid = {'reward': [
            {'kind': 'programmatic', 'criteria': [{'name': 'control', 'weight': 10,
              'value': 1.0, 'negate': False}]},
            {'kind': 'agent', 'criteria': [
                {'id': name, 'weight': 3, 'value': 1.0, 'negate': True,
                 'reasoning': "Results!D2 contains a source citation with no unsupported assertion."}
                for name in ['L01', 'L02', 'L03']]}]}
        cases = [
            ('evidence_backed_control', valid, False),
            ('saved_blind_C_golden_r4', {'reward': [valid['reward'][0], blind['agent']]}, True),
        ]
        for name, reason, expected in [
            ('no_cell', 'No unsupported assertions were found.', True),
            ('source_only_cell', 'The source Text!A131 supports this conclusion.', True),
            ('nonexistent_candidate_cell', 'Results!ZZ9999 supports this conclusion.', True),
            ('missing_with_cell', 'Results!D2 cannot be read because candidate workbook is missing.', True),
            ('unreadable_with_cell', 'Results!D2：无法解析候选文件。', True),
            ('missing_source_not_artifact', '候选 Results!D2 引用了不存在的来源文件。', False),
            ('missing_source_english', 'The candidate workbook Results!D2 cites a missing source file.', False),
            ('quoted_cell', "'Results'!$D$2 contains no audit-completion claim.", False),
        ]:
            detail = copy.deepcopy(valid)
            detail['reward'][1]['criteria'][0]['reasoning'] = reason
            cases.append((name, detail, expected))
        for name, detail, expected_error in cases:
            graded.with_name('reward-details.json').write_text(json.dumps(detail))
            output = folder / name / 'reward.json'
            subprocess.run([sys.executable, str(TASK / 'tests/finalize.py'),
                            '--graded', str(graded), '--graded-rc', '0',
                            '--candidate', str(golden), '--out', str(output)], check=True)
            receipt = json.loads(output.read_text())
            assert bool(receipt['verifier_error']) == expected_error, (name, receipt)
            if expected_error:
                assert receipt['reward'] == 0
                exit_message = json.loads(output.with_name('reward_exit_message.json').read_text())
                assert exit_message['exit_code'] == 'judge:artifact_access_error', name
            else:
                assert receipt['reward'] == 1.0, name
                assert not output.with_name('reward_exit_message.json').exists(), name
        saved_valid = 0
        for fixture in (TASK / 'validation/judge_fixtures').glob('saved_valid_*.json'):
            payload = json.loads(fixture.read_text())
            assert checker.evidence_errors({'reward': payload['agent']}, golden) == [], fixture.name
            saved_valid += 1
        assert checker.evidence_errors({'reward': blind['agent']}, folder / 'missing.xlsx') == []
    print(json.dumps({'artifact_access_regressions': len(cases),
                      'saved_blind_cases': 1, 'saved_valid_cases': saved_valid,
                      'missing_candidate_keeps_program_gate': True}))


if __name__ == '__main__':
    main()
