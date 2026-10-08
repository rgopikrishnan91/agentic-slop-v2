#!/usr/bin/env python3
"""Tally the kind review. Usage: python3 tools/kind_votes.py <c1 kinds dir> <c2 kinds dir> <c3 kinds dir> <out dir>"""
import json,sys,os,glob,collections
KINDS=['candidate pattern','proxy group','boundary register']
here=os.path.dirname(os.path.abspath(__file__)); E=os.path.join(here,'..','kind_review','coder','entries')
dirs=sys.argv[1:4]; out=sys.argv[4]; os.makedirs(out,exist_ok=True); rows=[]; summ=collections.Counter(); err=[]
for ef in sorted(glob.glob(os.path.join(E,'*.json'))):
    f=os.path.basename(ef)[:-5]; ents=json.load(open(ef)); V=[]
    for k,d in enumerate(dirs):
        p=os.path.join(d,f+'.json')
        if not os.path.exists(p): err.append(f'coder {k+1}: file for family {f} is missing'); V.append({}); continue
        x={r['entry_id']:r for r in json.load(open(p))}; V.append(x)
        for e in ents:
            r=x.get(e['id'])
            if not r: err.append(f'coder {k+1}: entry {e["id"]} has no answer'); continue
            if r.get('kind') not in KINDS: err.append(f'coder {k+1}: {e["id"]} kind not valid')
            if set(map(str,r.get('rule_kinds',{})))!=set(map(str,e['rule_ids'])): err.append(f'coder {k+1}: {e["id"]} rule_kinds must have each rule of the entry')
            if r.get('kind')=='boundary register' and not (r.get('condition') or '').strip(): err.append(f'coder {k+1}: {e["id"]} boundary register without condition')
    res=[]
    for e in ents:
        vs=[V[k].get(e['id'],{}) for k in range(3)]; ks=[v.get('kind') for v in vs]; c=collections.Counter(ks); lab,n=c.most_common(1)[0]
        status='full' if n==3 else 'majority' if n==2 else 'no majority'; summ[status]+=1; rows.append(ks)
        mis=collections.Counter(str(m['rule_id']) for v in vs for m in v.get('misfit_rules',[]))
        res.append(dict(entry_id=e['id'],status=status,majority_kind=lab if n>=2 else None,votes={f'coder{k+1}':dict(kind=vs[k].get('kind'),condition=vs[k].get('condition',''),reason=vs[k].get('reason','')) for k in range(3)},
          rule_kinds={str(r):[vs[k].get('rule_kinds',{}).get(str(r)) for k in range(3)] for r in e['rule_ids']},misfit_votes=dict(mis)))
    json.dump(res,open(os.path.join(out,f+'.json'),'w'),indent=1,ensure_ascii=False)
if err: print('\n'.join(err)); sys.exit(1)
N=len(rows); cnt=[[r.count(c) for c in KINDS] for r in rows]; Pb=sum((sum(v*v for v in c)-3)/6 for c in cnt)/N; pj=[sum(c[j] for c in cnt)/(3*N) for j in range(3)]; Pe=sum(p*p for p in pj)
s=dict(entries=N,full_agreement=summ['full'],majority_2_of_3=summ['majority'],no_majority=summ['no majority'],fleiss_kappa=None if Pe==1 else round((Pb-Pe)/(1-Pe),3),kind_share=dict(zip(KINDS,[round(p,3) for p in pj])))
json.dump(s,open(os.path.join(out,'_summary.json'),'w'),indent=1); print(json.dumps(s,indent=1))
