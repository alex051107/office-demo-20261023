"""Compute criterion credits and explicit violation complements."""
import copy
import importlib.util
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('s3_frozen_bridge', HERE/'frozen_bridge.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
FROZEN = json.loads((HERE/'frozen_key.json').read_text())

def extract(answer, key):
    return base.extract(answer, FROZEN)


def score(evidence, key):
    original = base.score(evidence, FROZEN)
    all_c = key.get('rows', []) + key.get('tables', []) + key.get('checks', [])
    if original['status'] == 'JUDGE_ERROR':
        return original
    verdicts = {}
    for c in all_c:
        cid = c['criterion_id']; source = c.get('source_criterion', cid)
        v = copy.deepcopy(original['verdicts'][source])
        if c.get('s3_transform') == 'violation_complement':
            v['original_compliance_credit'] = v['credit']
            v['credit'] = 1-v['credit']
            v['status'] = 'triggered' if v['credit'] else 'not_triggered'
        verdicts[cid] = v
    total = sum(c['weight'] for c in all_c if c['weight']>0)
    numerator = sum(c['weight']*(1-round(1-verdicts[c['criterion_id']]['credit'],4) if c['weight']<0 else round(verdicts[c['criterion_id']]['credit'],4)) for c in all_c)
    return {'status':original['status'], 'score':round(max(0,min(1,numerator/total)),6), 'verdicts':verdicts}
