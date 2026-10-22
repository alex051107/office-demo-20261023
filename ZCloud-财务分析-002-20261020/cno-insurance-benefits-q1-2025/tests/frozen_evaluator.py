"""Offline workbook extraction and deterministic atomic weighted scoring."""
from pathlib import Path
import argparse, ast, json, math, re, unicodedata
from openpyxl import load_workbook

def norm(x):
 s=unicodedata.normalize('NFKC',str(x or '')).casefold()
 return re.sub(r'\s+',' ',re.sub('[‐-―−]','-',s)).strip().rstrip('.;:')
def num(x):
 if isinstance(x,bool):return None
 if isinstance(x,(int,float)):return float(x) if math.isfinite(x) else None
 s=re.sub(r'[,$\s]','',str(x or '')).rstrip('%')
 if s.startswith('(') and s.endswith(')'):s='-'+s[1:-1]
 try:
  v=float(s);return v if math.isfinite(v) else None
 except ValueError:return None
def canon(x,aliases):
 n=norm(x)
 for key,values in aliases.items():
  if n in [norm(key)]+[norm(v) for v in values]:return norm(key)
 return n

def extract(path,key):
 if not Path(path).is_file():return {'status':'OUTPUT_MISSING','sheets':{},'formulas':[]}
 try:
  w=load_workbook(path,data_only=True); fw=load_workbook(path,data_only=False)
 except Exception as e:return {'status':'JUDGE_ERROR','error':str(e),'sheets':{},'formulas':[]}
 sheets={}; formula_cells=[]; resolving=set()
 errors=[]
 ERR={'#DIV/0!','#VALUE!','#REF!','#NAME?','#N/A','#NUM!','#NULL!','#SPILL!','#CALC!'}
 for s_ in w:
  for row_ in s_.iter_rows():
   for c_ in row_:
    if c_.data_type=='e' or (isinstance(c_.value,str) and c_.value.strip().upper() in ERR):errors.append(s_.title+'!'+c_.coordinate)
 def value(sh,coord):
  c=w[sh][coord];f=fw[sh][coord]
  if f.data_type!='f':return c.value
  formula_cells.append(sh+'!'+coord)
  if c.value is not None:return c.value
  ident=(sh,coord)
  if ident in resolving:return None
  resolving.add(ident)
  try:
   expr=f.value[1:].replace('$','')
   refs={}
   def ref(m):
    name=m.group(1) or m.group(2) or sh;cell=m.group(3);v=value(name,cell)
    if num(v) is None: raise ValueError('unresolved cell')
    token='v'+str(len(refs));refs[token]=num(v);return token
   expr=re.sub(r"(?:'([^']+)'!|([A-Za-z_][A-Za-z0-9_ ]*)!)?([A-Z]+[0-9]+)",ref,expr)
   def ev(n):
    if isinstance(n,ast.Expression):return ev(n.body)
    if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
    if isinstance(n,ast.Name):return refs[n.id]
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):return ev(n.operand)*(1 if isinstance(n.op,ast.UAdd) else -1)
    if isinstance(n,ast.BinOp):
     a,b=ev(n.left),ev(n.right)
     if isinstance(n.op,ast.Add):return a+b
     if isinstance(n.op,ast.Sub):return a-b
     if isinstance(n.op,ast.Mult):return a*b
     if isinstance(n.op,ast.Div):return a/b
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id.upper() in ['SUM','ROUND','ABS']:
     a=[ev(x) for x in n.args];return sum(a) if n.func.id.upper()=='SUM' else round(*a) if n.func.id.upper()=='ROUND' else abs(a[0])
    raise ValueError('unsupported formula')
   return ev(ast.parse(expr,mode='eval'))
  except Exception:return None
  finally:resolving.remove(ident)
 for sheet,definition in key['interfaces'].items():
  allowed=[norm(sheet)]+[norm(x) for x in definition.get('aliases',[])]
  candidates=[s for s in w if norm(s.title) in allowed]
  if not candidates:
   candidates=[s for s in w if set(definition['key']) <= {canon(c.value,definition.get('header_aliases',{})) for c in s[1]}]
  if len(candidates)!=1:
   sheets[sheet]={'headers':[],'records':{},'extra':[],'actual_name':None};continue
  s=candidates[0]; headers=[canon(c.value,definition.get('header_aliases',{})) for c in s[1]]
  expected={tuple(canon(v,definition.get('value_aliases',{})) for v in x) for x in definition['expected_keys']}
  records={};extra=[]
  for row in list(s)[1:]:
   record={h:{'raw':value(s.title,c.coordinate),'cell':s.title+'!'+c.coordinate,'format':c.number_format} for h,c in zip(headers,row) if h}
   ident=tuple(canon(record.get(h,{}).get('raw'),definition.get('value_aliases',{})) for h in definition['key'])
   if not any(ident):continue
   records.setdefault('|'.join(ident),[]).append(record)
   if ident not in expected:extra.append(ident)
  sheets[sheet]={'headers':headers,'records':records,'extra':extra,'actual_name':s.title}
 w.close();fw.close()
 return {'status':'PARSED','sheets':sheets,'formulas':sorted(set(formula_cells)),'error_cells':errors}

def observations(e,key,ref):
 sheet,ident,field=ref; aliases=key['interfaces'][sheet].get('value_aliases',{})
 enc='|'.join(canon(x,aliases) for x in ident)
 return [r.get(field,{'raw':None,'cell':None,'format':''}) for r in e['sheets'].get(sheet,{}).get('records',{}).get(enc,[])]
def amount(e,key,ref,percent=False):
 oo=observations(e,key,ref);vv=[]
 for o in oo:
  v=num(o['raw'])
  if v is None:return None
  if percent and '%' in o['format'] and not isinstance(o['raw'],str):v*=100
  if ref[0]=='Analysis' and ref[2]=='amount':
   units=observations(e,key,[ref[0],ref[1],'unit'])
   u=norm(units[0]['raw']) if units else ''
   if key.get('amount_base_unit')=='usd millions':
    if u in ['usd','usd dollars','dollars']:v/=1e6
    elif u in ['usd thousands','usd thousand','thousands of usd']:v/=1000
   else:
    if u in ['usd','usd dollars','dollars']:v/=1000
    elif u in ['usd millions','usd million','millions of usd']:v*=1000
  vv.append(v)
 if not vv or max(vv)-min(vv)>1e-8:return None
 return vv[0]
def score(e,key):
 verdicts={}; criteria=key['rows']+key['tables']+key['checks']
 for c in key['rows']+key['tables']:
  if c in key['rows']:
   ref=['Results',[c['label']],'value'];spec=c;gold=c['gold']
  else:
   field,spec=next(iter(c['value_columns'].items()));r=c['gold'][0]
   ref=[c['sheet'],[r[k] for k in c['key']],field];gold=r[field]
  v=amount(e,key,ref,spec.get('percent_forms',False));met=v is not None and abs(v-gold)<=spec.get('abs',0)+spec.get('rel',0)*abs(gold)+1e-9
  verdicts[c['criterion_id']]={'credit':float(met),'observed':v,'expected':gold,'evidence':observations(e,key,ref)}
 for c in key['checks']:
  typ=c['kind']; observed=None;credit=0.
  if typ=='aggregate':
   pf=c.get('percent_refs') or [False]*len(c['refs'])
   vals=[amount(e,key,r,p_) for r,p_ in zip(c['refs'],pf)]; observed=vals
   credit=float(all(v is not None for v in vals) and abs(sum(a*b for a,b in zip(vals,c['coefficients'])))<=c['abs']+1e-8)
  elif typ=='source':
   oo=observations(e,key,c['ref']);observed=oo
   # Recognized supplied file/title alias. No winning filing, count, or sequence is required.
   credit=float(bool(oo) and all(any(re.search(p,norm(o['raw']),re.I) for p in key['source_patterns']) for o in oo))
  elif typ=='header':
   d=e['sheets'].get(c['sheet'],{});observed=d.get('headers',[])
   nonempty=any(x.get('raw') not in [None,''] for rr in d.get('records',{}).values() for r in rr for h,x in r.items() if h not in key['interfaces'][c['sheet']]['key'])
   credit=float(nonempty and set(key['interfaces'][c['sheet']]['headers'])<=set(observed))
  elif typ=='error_cells':
   observed=e.get('error_cells',[]);credit=float(bool(observed))
  elif typ=='unsupported_records':
   extra=[x for s in e['sheets'].values() for x in s.get('extra',[])];observed=extra
   denominator=sum(len(d['expected_keys']) for d in key['interfaces'].values())
   credit=min(1,len(extra)/denominator)
  else:raise ValueError(typ)
  verdicts[c['criterion_id']]={'credit':credit,'evidence':observed}
 total=sum(c['weight'] for c in criteria if c['weight']>0)
 earned=sum(c['weight']*verdicts[c['criterion_id']]['credit'] for c in criteria)
 for c in criteria:verdicts[c['criterion_id']].update(weight=c['weight'],dimension=c['dimension'])
 bygroup={}
 for c in criteria:
  bygroup.setdefault(c['budget_group'],0);bygroup[c['budget_group']]+=c['weight']*verdicts[c['criterion_id']]['credit']
 positive=[c for c in criteria if c['weight']>0]
 baseline=sum(c['baseline_weight']*verdicts[c['criterion_id']]['credit'] for c in key['rows'])/sum(c['baseline_weight'] for c in key['rows'])
 result={'status':'SCORED','task_id':key['task_id'],'score':min(1,max(0,earned/total)),'total_weight':total,'earned':earned,'groups':bygroup,
  'baseline_roots_score':baseline,'equal_criterion_score':sum(verdicts[c['criterion_id']]['credit'] for c in positive)/len(positive),
  'equal_business_score':sum(verdicts[c['criterion_id']]['credit'] for c in key['rows']+key['tables'])/(len(key['rows'])+len(key['tables'])),
  'verdicts':verdicts,'core_cap':False,'llm_judge_fraction':0}
 if e['status']=='JUDGE_ERROR':result.update(status='JUDGE_ERROR',score=None,error=e.get('error'))
 if e['status']=='OUTPUT_MISSING':result.update(status='OUTPUT_MISSING',score=0.0)
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--key',type=Path,required=True);p.add_argument('--candidate',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args();key=json.loads(a.key.read_text());path=a.candidate if a.candidate.is_file() else a.candidate/'answer.xlsx'
 e=extract(path,key);r=score(e,key);a.out.mkdir(parents=True,exist_ok=True)
 for f,d in [('extraction.json',e),('score.json',r)]: (a.out/f).write_text(json.dumps(d,ensure_ascii=False,indent=2,default=str)+'\n')
 (a.out/'reward.txt').write_text(str(r['score'] if r['score'] is not None else '')+'\n');print(json.dumps({'status':r['status'],'score':r['score']}))
 return 2 if r['status']=='JUDGE_ERROR' else 0
if __name__=='__main__':raise SystemExit(main())
