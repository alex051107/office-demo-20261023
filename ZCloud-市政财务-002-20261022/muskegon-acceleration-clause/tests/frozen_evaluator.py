"""Deterministic task scorer for <TASK_ID> (no LLM judge).

python3 score_output.py --key results_key.json --candidate answer.xlsx|DIR --out SCORE_DIR
Reads cached values (data_only) and formulas; static and recalculated workbooks are both accepted.
Score = clip((earned positive weight - triggered penalty weight) / total positive weight, 0, 1); no core cap.
Results rows are matched by label; Detail records by plan, one credit per record and field (per_record).
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import re
import unicodedata
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ERRORS = {'#VALUE!', '#REF!', '#DIV/0!', '#NAME?', '#N/A', '#NUM!', '#NULL!', '#SPILL!', '#CALC!'}


def normalized(value):
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.strftime('%Y-%m-%d')
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    text = unicodedata.normalize('NFKC', str(value if value is not None else '')).casefold()
    text = re.sub(r'[‐-―−]', '-', text)
    return re.sub(r'\s+', ' ', text).strip().rstrip('.;:')


def key_value(field, value):
    text = normalized(value)
    if field == 'case':
        text = re.sub(r'^case\s*', '', text)
    if field == 'invoice':
        text = text.replace(' ', '')
    return text


def number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (float, int)):
        return float(value) if math.isfinite(value) else None
    if not isinstance(value, str):
        return None
    text = value.strip().replace(',', '').replace('$', '').replace('USD', '').strip()
    if text.startswith('(') and text.endswith(')'):
        text = '-' + text[1:-1]
    try:
        result = float(text)
        return result if math.isfinite(result) else None
    except ValueError:
        return None


def number_matches(raw, gold, spec):
    observed = number(raw)
    if observed is None:
        return False
    for target in [gold] + list(spec.get('alternatives', [])):
        if abs(observed - float(target)) <= spec.get('abs', 0) + spec.get('rel', 0) * abs(float(target)) + 1e-10:
            return True
    return False


def extract(answer, key):
    if answer is None or not answer.is_file():
        return {'status': 'OUTPUT_MISSING', 'sheets': {}, 'errors': []}
    try:
        values = load_workbook(answer, data_only=True)
    except Exception as error:  # noqa: BLE001
        return {'status': 'JUDGE_ERROR', 'error': str(error), 'sheets': {}, 'errors': []}
    sheets, errors = {}, []
    for name, definition in key['interfaces'].items():
        expected = {normalized(h) for h in definition['headers']}
        ws = next((s for s in values.worksheets if normalized(s.title) == normalized(name)), None)
        if ws is None:
            candidates = [s for s in values.worksheets if expected <= {normalized(c.value) for c in next(s.iter_rows(max_row=1), [])}]
            ws = candidates[0] if len(candidates) == 1 else None
        if ws is None:
            sheets[name] = {'actual_name': None, 'headers': [], 'records': {}, 'rows': [], 'unsupported': []}
            continue
        raw = list(ws.iter_rows())
        headers = [normalized(c.value) for c in raw[0]] if raw else []
        index = {h: i for i, h in enumerate(headers) if h}
        allowed = {'|'.join(key_value(f, v) for f, v in zip(definition['key'], k)) for k in definition.get('allowed_keys', definition['expected_keys'])}
        records, order, unsupported = {}, [], []
        for rn, cells in enumerate(raw[1:], 2):
            rec = {}
            for field, pos in index.items():
                if pos < len(cells):
                    c = cells[pos]
                    rec[field] = {'raw': c.value if not isinstance(c.value, (datetime.datetime, datetime.date)) else normalized(c.value),
                                  'cell': f'{ws.title}!{get_column_letter(pos + 1)}{rn}'}
            ident = '|'.join(key_value(f, rec.get(f, {}).get('raw')) for f in definition['key'])
            if not ident.strip('|'):
                continue
            order.append(ident)
            records.setdefault(ident, []).append(rec)
            if ident not in allowed:
                unsupported.append(ident)
        sheets[name] = {'actual_name': ws.title, 'headers': headers, 'records': records, 'rows': order, 'unsupported': unsupported}
    for ws in values.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.data_type == 'e' or (isinstance(c.value, str) and c.value.strip().upper() in ERRORS):
                    errors.append(f'{ws.title}!{c.coordinate}')
    values.close()
    return {'status': 'PARSED', 'sheets': sheets, 'errors': errors}


def observations(evidence, sheet, ident, field):
    recs = evidence['sheets'].get(sheet, {}).get('records', {}).get(ident, [])
    return [r.get(normalized(field), {'raw': None, 'cell': None}) for r in recs]


def score(evidence, key):
    verdicts, charged = {}, set()
    for c in key['rows']:
        ident = key_value('label', c['label'])
        obs = observations(evidence, 'Results', ident, 'value')
        met = bool(obs) and all(number_matches(o['raw'], c['gold'], c) for o in obs)
        charged.update(o['cell'] for o in obs if o['cell'])
        verdicts[c['criterion_id']] = {'credit': int(met), 'evidence': obs, 'expected': c['gold']}
    for c in key['tables']:
        field, spec = next(iter(c['value_columns'].items()))
        gold = c['gold'][0]
        ident = '|'.join(key_value(f, gold[f]) for f in c['key'])
        obs = observations(evidence, c['sheet'], ident, field)
        if spec.get('type') == 'number':
            met = bool(obs) and all(number_matches(o['raw'], gold[field], spec) for o in obs)
        else:
            met = bool(obs) and all(normalized(o['raw']) == normalized(gold[field]) for o in obs)
        charged.update(o['cell'] for o in obs if o['cell'])
        verdicts[c['criterion_id']] = {'credit': int(met), 'evidence': obs, 'expected': gold[field]}
    for c in key['checks']:
        kind = c['kind']
        if kind == 'header':
            data = evidence['sheets'].get(c['sheet'], {})
            definition = key['interfaces'][c['sheet']]
            want = [normalized(h) for h in c['headers']]
            got = data.get('headers', [])
            met = normalized(data.get('actual_name')) == normalized(c['sheet']) and set(want) <= set(got)
            if c['sheet'] == 'Results':
                order = ['|'.join(key_value(f, v) for f, v in zip(definition['key'], k)) for k in definition['expected_keys']]
                met = met and got[:len(want)] == want and data.get('rows', [])[:len(order)] == order
            observed = got
        elif kind == 'results_units':
            obs = [o for c2 in key['rows'] for o in observations(evidence, 'Results', key_value('label', c2['label']), 'unit')]
            met = len(obs) == len(key['rows']) and all(normalized(o['raw']) == 'usd' for o in obs)
            observed = obs
        elif kind == 'error_cells':
            observed = [e for e in evidence.get('errors', []) if e not in charged]
            met = bool(observed)
        elif kind == 'unsupported_records':
            observed = evidence['sheets'].get(c['sheet'], {}).get('unsupported', [])
            met = bool(observed)
        else:
            raise ValueError(f'unimplemented check kind {kind}')
        verdicts[c['criterion_id']] = {'credit': int(met), 'evidence': observed}
    criteria = key['rows'] + key['tables'] + key['checks']
    total = sum(c['weight'] for c in criteria if c['weight'] > 0)
    earned = sum(c['weight'] * verdicts[c['criterion_id']]['credit'] for c in criteria if c['weight'] > 0)
    penalty = sum(-c['weight'] * verdicts[c['criterion_id']]['credit'] for c in criteria if c['weight'] < 0)
    s = min(1.0, max(0.0, (earned - penalty) / total))
    for c in criteria:
        v = verdicts[c['criterion_id']]
        v.update(weight=c['weight'], dimension=c['dimension'],
                 status=('triggered' if v['credit'] else 'clear') if c['weight'] < 0 else ('met' if v['credit'] else 'not_met'))
    core = [c for c in key['rows'] + key['tables'] if c.get('relation')]
    result = {'status': 'SCORED', 'task_id': key['task_id'], 'score': s, 'S0': s, 'S': s, 'cap_enabled': False,
              'total_weight': total, 'earned': earned, 'penalty_weight': penalty, 'accepted_S0': s >= .70,
              'root_criteria_met': sum(verdicts[c['criterion_id']]['credit'] for c in core), 'root_criteria': len(core),
              'verdicts': verdicts}
    if evidence['status'] == 'JUDGE_ERROR':
        result.update(status='JUDGE_ERROR', score=None, S0=None, S=None, accepted_S0=None, error=evidence.get('error'))
    elif evidence['status'] == 'OUTPUT_MISSING':
        result.update(status='OUTPUT_MISSING')
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--key', type=Path, required=True)
    ap.add_argument('--candidate', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    key = json.loads(a.key.read_text())
    answer = a.candidate if a.candidate.is_file() else a.candidate / 'answer.xlsx'
    evidence = extract(answer, key)
    result = score(evidence, key)
    a.out.mkdir(parents=True, exist_ok=True)
    for name, value in (('extraction.json', evidence), ('score.json', result)):
        (a.out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n')
    (a.out / 'reward.txt').write_text(f"{result['S0']}\n")
    print(json.dumps({k: result[k] for k in ('status', 'S0')}))
    return 2 if result['status'] == 'JUDGE_ERROR' else 0


if __name__ == '__main__':
    raise SystemExit(main())
