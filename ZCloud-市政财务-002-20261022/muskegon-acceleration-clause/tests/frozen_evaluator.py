"""Deterministic task scorer for <TASK_ID> (no LLM judge).

python3 score_output.py --key results_key.json --candidate answer.xlsx|DIR --out SCORE_DIR
Reads cached values (data_only) and formulas; static and recalculated workbooks are both accepted.
Signed-weight pooling precedes the required-sheet gate and named binary caps.
Required headers are positional and trimmed; business rows are matched by label or plan.
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import re
import unicodedata
from decimal import Decimal
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
    sheets, errors, interface_errors, header_errors = {}, [], [], []
    for name, definition in key['interfaces'].items():
        ws = values[name] if name in values.sheetnames else None
        if ws is None:
            interface_errors.append({'sheet': name, 'reason': 'required_sheet_missing_or_misnamed'})
            sheets[name] = {'actual_name': None, 'headers': [], 'records': {}, 'rows': [], 'unsupported': []}
            continue
        raw = list(ws.iter_rows())
        used_columns = max((cell.column for row in raw for cell in row if cell.value is not None), default=0)
        header_values = [cell.value for cell in raw[0][:used_columns]] if raw else []
        required_headers = definition['headers']
        trimmed_headers = [value.strip() if isinstance(value, str) else value for value in header_values]
        if (trimmed_headers[:len(required_headers)] != required_headers
                or definition.get('exact_column_count', False) and used_columns != len(required_headers)):
            header_errors.append({'sheet': name, 'reason': 'required_header_prefix_mismatch',
                                  'expected': required_headers, 'observed': header_values})
        headers = [normalized(value) for value in header_values]
        index = {normalized(header): position for position, header in enumerate(required_headers)}
        allowed = definition.get('allowed_keys', definition['expected_keys'])
        records, order, unsupported, raw_labels, row_numbers = {}, [], [], [], []
        for rn, cells in enumerate(raw[1:], 2):
            if not any(cell.value is not None for cell in cells[:len(required_headers)]):
                continue
            rec = {}
            for field, pos in index.items():
                if pos < len(cells):
                    c = cells[pos]
                    rec[field] = {'raw': c.value if not isinstance(c.value, (datetime.datetime, datetime.date)) else normalized(c.value),
                                  'cell': f'{ws.title}!{get_column_letter(pos + 1)}{rn}',
                                  'number_format': c.number_format}
            ident = '|'.join(key_value(f, rec.get(f, {}).get('raw')) for f in definition['key'])
            if not ident.strip('|'):
                unsupported.append({'row': rn, 'label': None, 'reason': 'business_row_without_label',
                                    'has_business_value': rec.get('value', {}).get('raw') not in (None, '')})
                continue
            order.append(ident)
            row_numbers.append(rn)
            raw_labels.append([rec.get(field, {}).get('raw') for field in definition['key']])
            if ident in records:
                unsupported.append({'row': rn, 'label': ident, 'reason': 'duplicate_required_record',
                                    'has_business_value': rec.get('value', {}).get('raw') not in (None, '')})
            records.setdefault(ident, []).append(rec)
            if raw_labels[-1] not in allowed:
                unsupported.append({'row': rn, 'label': ident, 'reason': 'unexpected_record',
                                    'has_business_value': rec.get('value', {}).get('raw') not in (None, '')})
        sheets[name] = {'actual_name': ws.title, 'headers': headers, 'records': records,
                        'rows': order, 'raw_labels': raw_labels, 'row_numbers': row_numbers,
                        'unsupported': unsupported}
    for ws in values.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.data_type == 'e' or (isinstance(c.value, str) and c.value.strip().upper() in ERRORS):
                    errors.append(f'{ws.title}!{c.coordinate}')
    values.close()
    return {'status': 'PARSED', 'sheets': sheets, 'errors': errors,
            'interface_errors': interface_errors, 'header_errors': header_errors}


def observations(evidence, sheet, ident, field):
    recs = evidence['sheets'].get(sheet, {}).get('records', {}).get(ident, [])
    return [r.get(normalized(field), {'raw': None, 'cell': None}) for r in recs]


def precision_matches(observation, places=2, at_least=False):
    raw = observation['raw']
    value = number(raw)
    if value is None:
        return False
    if abs(value - round(value, places)) <= 1e-10:
        return True
    if at_least and -Decimal(str(value)).as_tuple().exponent >= places:
        return True
    sections = observation.get('number_format', 'General').split(';')
    section = sections[1] if number(raw) < 0 and len(sections) > 1 else sections[0]
    section = re.sub(r'"[^\"]*"|\\.|\[[^\]]*\]|_.|\*.', '', section)
    match = re.search(r'[0#?][0#?,]*\.([0#?]+)', section)
    return bool(match and (len(match.group(1)) >= places if at_least else len(match.group(1)) == places)
                and match.group(1).count('0') >= places
                and not re.search(r'%|[Ee][+-]|[0#?],', section[match.end():])) and not section.endswith(',')


def apply_score_rules(pooled, rules):
    return min([pooled] + [rule['maximum_score'] for rule in rules if rule['triggered']])


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
        if c['weight'] < 0:
            met = not met
        charged.update(o['cell'] for o in obs if o['cell'])
        verdicts[c['criterion_id']] = {'credit': int(met), 'evidence': obs, 'expected': gold[field]}
    for c in key['checks']:
        kind = c['kind']
        if kind == 'header':
            observed = evidence.get('header_errors', [])
            met = bool(observed)
        elif kind == 'row_order':
            observed = evidence['sheets'].get(c['sheet'], {}).get('raw_labels', [])
            expected = key['interfaces'][c['sheet']]['expected_keys']
            row_numbers = evidence['sheets'].get(c['sheet'], {}).get('row_numbers', [])
            met = observed[:len(expected)] != expected or row_numbers[:len(expected)] != list(range(2, 2 + len(expected)))
        elif kind == 'results_units':
            groups = [observations(evidence, 'Results', key_value('label', row['label']), 'unit') for row in key['rows']]
            obs = [item for group in groups for item in group]
            met = any(not group for group in groups) or any(o['raw'] != 'USD' for o in obs)
            observed = obs
        elif kind == 'source_notes':
            groups = [observations(evidence, 'Results', key_value('label', row['label']), 'source_note') for row in key['rows']]
            observed = [item for group in groups for item in group]
            met = any(not group for group in groups) or any(
                not isinstance(item['raw'], str) or not item['raw'].strip()
                or number(item['raw']) is not None for item in observed)
        elif kind == 'money_precision':
            groups = [observations(evidence, sheet, key_value(definition['key'][0], ident[0]), 'value')
                      for sheet, definition in key['interfaces'].items() for ident in definition['expected_keys']]
            observed = [item for group in groups for item in group]
            met = any(not group for group in groups) or any(not precision_matches(item) for item in observed)
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
    gate_passed = evidence['status'] == 'PARSED' and not evidence.get('interface_errors')
    total = sum(c['weight'] for c in criteria if c['weight'] > 0)
    earned = sum(c['weight'] * verdicts[c['criterion_id']]['credit'] for c in criteria if c['weight'] > 0)
    penalty = sum(-c['weight'] * verdicts[c['criterion_id']]['credit'] for c in criteria if c['weight'] < 0)
    pooled = min(1.0, max(0.0, (earned - penalty) / total))
    must_reasons = [{'criterion_id': identifier, 'reason': reason}
                    for identifier, reason in [('S04', 'required_source_empty_or_numeric_only'),
                                               ('S02', 'required_unit_mismatch')]
                    if verdicts[identifier]['credit']]
    must_reasons.extend({'sheet': sheet, **record}
                        for sheet, content in evidence['sheets'].items()
                        for record in content.get('unsupported', [])
                        if record.get('has_business_value') and record['reason'] != 'duplicate_required_record')
    rules = [
        {'name': 'required_sheet_gate', 'triggered': not gate_passed, 'maximum_score': 0.0,
         'reasons': evidence.get('interface_errors', []) or ([] if gate_passed else [evidence['status']])},
        {'name': 'required_header_cap', 'triggered': bool(evidence.get('header_errors')), 'maximum_score': 0.69,
         'reasons': evidence.get('header_errors', [])},
        {'name': 'must_clause_cap', 'triggered': bool(must_reasons), 'maximum_score': 0.69,
         'reasons': must_reasons},
    ]
    final = apply_score_rules(pooled, rules)
    for c in criteria:
        v = verdicts[c['criterion_id']]
        v.update(weight=c['weight'], dimension=c['dimension'],
                 status=('triggered' if v['credit'] else 'clear') if c['weight'] < 0 else ('met' if v['credit'] else 'not_met'))
    core = [c for c in key['rows'] + key['tables'] if c.get('relation')]
    result = {'status': 'SCORED', 'task_id': key['task_id'], 'score': final, 'S0': pooled, 'S': final,
              'cap_enabled': True, 'score_rules': rules,
              'interface_gate_passed': gate_passed,
              'interface_errors': evidence.get('interface_errors', []),
              'header_errors': evidence.get('header_errors', []),
              'total_weight': total, 'earned': earned, 'penalty_weight': penalty,
              'accepted_S0': pooled >= .70, 'accepted': final >= .70,
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
