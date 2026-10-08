#!/usr/bin/env python3
"""Check the judge's step B output against the rules of step B version 2. Usage: python3 tools/check_step_b.py <dir with judge output and inputs>"""
import json,sys,os,collections,itertools,re
d=sys.argv[1]; L=lambda n: json.load(open(os.path.join(d,n)))
K=L('patterns_kind_reviewed.json'); A=L('patterns_agreed.json'); U=L('units.json'); S=L('single_rule_units.json'); D=L('decisions.json'); PV=L('pair_votes_across.json')
err=[]; warn=[]
kin={e['id']:e for e in K}; ag={e['id']:e for e in A}
if set(kin)!=set(ag): err.append('patterns_agreed.json must have the same entries as patterns_kind_reviewed.json')
for i,e in ag.items():
    if i in kin and sorted(map(str,e['rule_ids']))!=sorted(map(str,kin[i]['rule_ids'])): err.append(f'{i}: rule_ids changed')
    if not e.get('unit_id'): err.append(f'{i}: no unit_id')
units=collections.defaultdict(list)
for e in A: units[e.get('unit_id')].append(e)
votes={(p['a'],p['b']):p['n_votes'] for p in PV['pairs']}
dec={}
for x in D:
    a,b=sorted([x['a'],x['b']]); dec[(a,b)]=x
    if x.get('decision') not in ('merge','separate','majority not applied','chain check: merge','chain check: separate'): err.append(f'{a}/{b}: decision not valid')
    if 'merge' in x.get('decision','') and 'separate' not in x['decision'] and x['decision']!='majority not applied' and not (x.get('merged_invariant') or '').strip(): err.append(f'{a}/{b}: merge without merged_invariant')
for k in votes:
    if k not in dec: err.append(f'{k[0]}/{k[1]}: listed pair has no decision')
for uid,es in units.items():
    for x,y in itertools.combinations(sorted(e['id'] for e in es),2):
        k=(x,y); dd=dec.get(k); fx,fy=kin[x]['family'],kin[y]['family']; kx,ky=kin[x]['entry_kind'],kin[y]['entry_kind']
        if not dd or dd['decision'] not in ('merge','chain check: merge'): err.append(f'unit {uid}: {x} and {y} are in one unit without a merge decision or chain check for this pair')
        if fx==fy and (not dd or dd['decision']!='chain check: merge'): err.append(f'unit {uid}: {x} and {y} are in the same family; permitted only with a chain check')
        if kx!=ky and {kx,ky}!={'candidate pattern','boundary register'}: err.append(f'unit {uid}: {x} ({kx}) and {y} ({ky}) have kinds that cannot be merged')
        if dd and dd['decision']=='merge' and votes.get(k,0)==1: warn.append(f'unit {uid}: {x}/{y} merged on one vote; the reason must show that the obligations are identical')
    if len({(e.get('name'),e.get('invariant'),e.get('entry_kind')) for e in es})>1: err.append(f'unit {uid}: member entries do not carry the same unit name, invariant and kind')
for k,n in votes.items():
    dd=dec.get(k)
    if dd and n>=2 and dd['decision']=='separate': err.append(f'{k[0]}/{k[1]}: two or three votes but decision is separate; use merge or majority not applied')
    if dd and dd['decision'] in ('merge',) and ag[k[0]].get('unit_id')!=ag[k[1]].get('unit_id'): err.append(f'{k[0]}/{k[1]}: decision is merge but the entries are in two units')
nr=lambda es: len({str(r) for e in es for r in e['rule_ids']})
multi={u for u,es in units.items() if nr(es)>=2}; single=set(units)-multi
if {u['unit_id'] for u in U}!=multi: err.append('units.json must hold the units with two or more distinct rules, and only those')
if {u['unit_id'] for u in S}!=single: err.append('single_rule_units.json must hold the units with one distinct rule, and only those')
norm=lambda s: re.sub(r'[^a-z ]','',re.sub(r'\b[A-Z]-\d+\b','',s or '').lower()).strip()
c=collections.Counter(norm(x.get('reason')) for x in D)
for s,n in c.items():
    if n>=3 and len(s)>30: err.append(f'the same reason text is used for {n} decisions: "{s[:70]}..."')
    if len(s)<30: warn.append(f'a reason is very short: "{s}"')
print('units',len(units),'with two or more rules',len(multi),'with one rule',len(single),'decisions',len(D))
for x in warn: print('WARNING',x)
print('\n'.join(err) if err else 'OK: no errors'); sys.exit(1 if err else 0)
