#!/usr/bin/env python3
"""Tally the step B pairs. Usage: python3 tools/pair_votes.py c1.json c2.json c3.json patterns_kind_reviewed.json > pair_votes_across.json"""
import json,sys,collections
P={e['id']:e for e in json.load(open(sys.argv[4]))}; V=collections.defaultdict(dict); err=[]
for k,p in enumerate(sys.argv[1:4]):
    d=json.load(open(p)); d=d if isinstance(d,list) else d.get('pairs',[])
    for x in d:
        a,b=x.get('a'),x.get('b')
        if a not in P or b not in P: err.append(f'coder {k+1}: unknown entry in pair {a} / {b}'); continue
        if P[a]['family']==P[b]['family']: err.append(f'coder {k+1}: pair {a} / {b} is inside one family; not permitted in step B')
        if x.get('label') not in ('SAME','HIGHLY SIMILAR'): err.append(f'coder {k+1}: pair {a} / {b} has label {x.get("label")}; list only SAME and HIGHLY SIMILAR')
        if not (x.get('merged_invariant') or '').strip(): err.append(f'coder {k+1}: pair {a} / {b} has no merged_invariant')
        a,b=sorted([a,b]); V[(a,b)][f'coder{k+1}']=dict(label=x.get('label'),broader=x.get('broader',''),merged_invariant=x.get('merged_invariant',''),reason=x.get('reason',''))
if err: sys.stderr.write('\n'.join(err)+'\n'); sys.exit(1)
out=[dict(a=a,b=b,families=[P[a]['family'],P[b]['family']],kinds=[P[a]['entry_kind'],P[b]['entry_kind']],n_votes=len(v),status='two or three votes' if len(v)>=2 else 'one vote',votes=v) for (a,b),v in sorted(V.items())]
json.dump(dict(summary=dict(pairs=len(out),two_or_three_votes=sum(o['n_votes']>=2 for o in out),three_votes=sum(o['n_votes']==3 for o in out),one_vote=sum(o['n_votes']==1 for o in out)),listed_by=[sum(1 for v in V.values() if f'coder{k+1}' in v) for k in range(3)],pairs=out),sys.stdout,indent=1,ensure_ascii=False)
