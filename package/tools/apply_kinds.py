#!/usr/bin/env python3
"""Apply the kind review. Usage: python3 tools/apply_kinds.py <kind_votes dir> <kind_decisions dir> <output patterns_kind_reviewed.json>"""
import json,sys,os,glob,collections
here=os.path.dirname(os.path.abspath(__file__)); E=os.path.join(here,'..','kind_review','coder','entries')
kv,kd,outp=sys.argv[1:4]; out=[]; err=[]; c=collections.Counter()
for ef in sorted(glob.glob(os.path.join(E,'*.json'))):
    f=os.path.basename(ef)[:-5]; votes={r['entry_id']:r for r in json.load(open(os.path.join(kv,f+'.json')))}
    dp=os.path.join(kd,f+'.json'); dec={r['entry_id']:r for r in json.load(open(dp))} if os.path.exists(dp) else {}
    for e in json.load(open(ef)):
        v=votes[e['id']]
        if v['status']=='no majority':
            d=dec.get(e['id'])
            if not d or d.get('kind') not in ('candidate pattern','proxy group','boundary register'): err.append(f'{e["id"]}: no majority and no judge decision'); continue
            kind=d['kind']; cond=d.get('condition',''); how='judge'; reason=d.get('reason','')
        else:
            kind=v['majority_kind']; how=v['status']; conds=[x['condition'] for x in v['votes'].values() if x['kind']==kind and x.get('condition')]; cond=conds[0] if conds else ''; reason=''
            if e['id'] in dec: err.append(f'{e["id"]}: the judge decided an entry that has a majority')
        mis=sorted(r for r,n in v['misfit_votes'].items() if n>=2)
        x=dict(e); x['entry_kind']=kind; x['kind_condition']=cond if kind=='boundary register' else ''; x['kind_decision']=how; x['kind_judge_reason']=reason; x['kind_misfit_rule_ids']=mis; x['uncertain_rule_ids']=[]
        out.append(x); c[kind]+=1
if err: print('\n'.join(err)); sys.exit(1)
json.dump(out,open(outp,'w'),indent=1,ensure_ascii=False); print('entries',len(out),dict(c))
