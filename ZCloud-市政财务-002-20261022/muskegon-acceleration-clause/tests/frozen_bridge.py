"""Normalize frozen evaluator APIs without changing their criterion decisions."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('frozen_business_engine', HERE / 'frozen_evaluator.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

def extract(answer, key):
    answer = Path(answer)
    if hasattr(engine, 'extract'):
        return engine.extract(answer, key)
    if not answer.is_file():
        return {'status': 'OUTPUT_MISSING'}
    try:
        return {'status': 'EXTRACTED', 'book': engine.read_static(answer), 'formulas': engine.read_formulas(answer)}
    except Exception as e:
        return {'status': 'JUDGE_ERROR', 'error': str(e)}

def score(evidence, key):
    criteria = key.get('rows', []) + key.get('tables', []) + key.get('checks', [])
    if hasattr(engine, 'extract'):
        return engine.score(evidence, key)
    if evidence['status'] in {'OUTPUT_MISSING', 'JUDGE_ERROR'}:
        return {'status': evidence['status'], 'score': 0 if evidence['status']=='OUTPUT_MISSING' else None,
                'verdicts': {c['criterion_id']: {'credit': 0} for c in criteria}}
    result = engine.score_book(key, evidence['book'], formulas=evidence['formulas'])
    per_record = {c['criterion_id'] for c in key.get('tables', []) if c.get('pass_rule', {}).get('per_record')}
    for c in criteria:
        cid = c['criterion_id']; v = result['verdicts'][cid]
        if c['weight'] < 0:
            credit = int(v['status'] in {'triggered', 'met'})
        elif cid in per_record and 'credit_fraction' in v:
            credit = v['credit_fraction']
        else:
            credit = int(v['status']=='met')
        v['credit'] = credit
    return result
