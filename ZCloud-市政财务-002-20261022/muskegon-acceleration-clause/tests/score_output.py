"""S3 policy layer: frozen decisions, explicit violation complements, unit conversion."""
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

def converted_results(evidence):
    # Independently compare the same requested monetary results in base AUD.
    # This does not require any new candidate column or reward a unit label.
    engine = base.engine
    key = copy.deepcopy(FROZEN)
    book = copy.deepcopy(evidence['book'])
    rows = engine.find_sheet(book, key.get('sheet', 'Results'))
    cols = engine.result_columns(key, rows)
    if rows and cols and 'value' in cols:
        for row in rows[1:]:
            if len(row) > cols['value']:
                v = engine.parse_number(row[cols['value']])
                row[cols['value']] = v * 1000000 if isinstance(v, (int, float)) else None
    for c in key['rows']:
        c['gold'] *= 1000000
        c['accepted'] = [v*1000000 for v in c.get('accepted', [])]
        c['tolerance']['abs'] *= 1000000
    for alt in key.get('alternative_sets', []):
        alt['gold'] = {k:v*1000000 for k,v in alt['gold'].items()}
    return engine.score_rows(key, book, evidence.get('formulas'))[0]

def score(evidence, key):
    original = base.score(evidence, FROZEN)
    all_c = key.get('rows', []) + key.get('tables', []) + key.get('checks', [])
    if original['status'] == 'JUDGE_ERROR':
        return original
    converted = converted_results(evidence) if evidence['status'] != 'OUTPUT_MISSING' and any(c.get('s3_transform')=='aud_base' for c in all_c) else {}
    verdicts = {}
    for c in all_c:
        cid = c['criterion_id']; source = c.get('source_criterion', cid)
        v = copy.deepcopy(original['verdicts'][source])
        if c.get('s3_transform') == 'aud_base':
            v = copy.deepcopy(converted.get(source, {'status':'not_met', 'evidence':'missing workbook'}))
            v['credit'] = int(v['status']=='met')
        elif c.get('s3_transform') == 'violation_complement':
            v['original_compliance_credit'] = v['credit']
            v['credit'] = 1-v['credit']
            v['status'] = 'triggered' if v['credit'] else 'not_triggered'
        verdicts[cid] = v
    total = sum(c['weight'] for c in all_c if c['weight']>0)
    numerator = sum(c['weight']*(1-round(1-verdicts[c['criterion_id']]['credit'],4) if c['weight']<0 else round(verdicts[c['criterion_id']]['credit'],4)) for c in all_c)
    return {'status':original['status'], 'score':round(max(0,min(1,numerator/total)),6), 'verdicts':verdicts}
