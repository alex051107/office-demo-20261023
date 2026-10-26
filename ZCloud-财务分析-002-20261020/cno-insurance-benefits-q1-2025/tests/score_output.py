"""Frozen CNO decisions; duplicate Summary positives removed; existing signed weights."""
import copy, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('s4_frozen_bridge',HERE/'frozen_bridge.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
FROZEN=json.loads((HERE/'frozen_key.json').read_text())
def extract(answer,key): return base.extract(answer,FROZEN)
def score(evidence,key):
    original=base.score(evidence,FROZEN)
    if original['status']=='JUDGE_ERROR': return original
    criteria=key['rows']+key['tables']+key['checks'];verdicts={}
    for c in criteria:
        cid=c['criterion_id'];v=copy.deepcopy(original['verdicts'][cid])
        if c.get('s3_transform')=='violation_complement':
            v['original_compliance_credit']=v['credit'];v['credit']=1-v['credit']
        v.update(weight=c['weight'],dimension=c['dimension'])
        verdicts[cid]=v
    smax=sum(c['weight'] for c in criteria if c['weight']>0)
    numerator=sum(c['weight']*(1-round(1-verdicts[c['criterion_id']]['credit'],4) if c['weight']<0 else round(verdicts[c['criterion_id']]['credit'],4)) for c in criteria)
    pooled=round(max(0,min(1,numerator/smax)),6)
    rules=original.get('post_pool_rules',[])
    score=min([pooled]+[rule['cap'] for rule in rules if rule['triggered']])
    gate=original.get('interface_gate',{'failed':False,'errors':[]})
    return {'status':original['status'],'score':0.0 if gate['failed'] else score,'verdicts':verdicts,
            'score_before_post_pool_rules':pooled,'post_pool_rules':rules,'interface_gate':gate}
