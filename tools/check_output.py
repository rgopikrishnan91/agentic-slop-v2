#!/usr/bin/env python3
"""Coverage check. Usage: python3 tools/check_output.py patterns_agreed.json   (also works for patterns_kind_reviewed.json)"""
import json,sys,collections,os
here=os.path.dirname(os.path.abspath(__file__)); rules=json.load(open(os.path.join(here,'..','step_b','coder','rules.json'))); P=json.load(open(sys.argv[1])); err=[]
want=collections.defaultdict(set)
for r in rules:
    fc=r['family_codes']; fc=fc if isinstance(fc,list) else [x.strip().strip("'\"") for x in str(fc).strip('[]').replace(';',',').split(',') if x.strip()]
    for f in fc: want[f].add(str(r['rule_id']))
got=collections.defaultdict(list); ids=set()
for e in P:
    if e.get('id') in ids: err.append(f"{e.get('id')}: id occurs two times")
    ids.add(e.get('id'))
    if e.get('entry_kind') not in ('candidate pattern','proxy group','boundary register'): err.append(f"{e.get('id')}: entry_kind not valid")
    got[e.get('family')]+=[str(x) for x in e.get('rule_ids',[])]
for f in sorted(set(want)|set(got)):
    g=got.get(f,[]); dup=[x for x,c in collections.Counter(g).items() if c>1]
    if dup: err.append(f"family {f}: rules in two entries: {sorted(dup)}")
    if set(g)!=want.get(f,set()): err.append(f"family {f}: missing {sorted(want.get(f,set())-set(g))} extra {sorted(set(g)-want.get(f,set()))}")
print('entries',len(P),'memberships',sum(len(v) for v in got.values()),'expected',sum(len(v) for v in want.values()))
print('\n'.join(err) if err else 'OK: no errors'); sys.exit(1 if err else 0)
