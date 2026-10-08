# Independence log: step B judge (version 2)

Session: fresh session, files in this folder only. No other branch, earlier result, web source, subagent, workflow or other model was used. Every decision, merged obligation and reason in `decisions.json` and every unit text was written by me; a script only assembled the JSON files.

## Decisions (22)

- Pairs in `pair_votes_across.json`: 20 (16 with three votes, 1 with two, 3 with one).
- `merge`: 16 (all two- and three-vote pairs except I-06/T-01).
- `majority not applied`: 1 (I-06/T-01).
- `separate`: 2 (one-vote pairs H-08/K-01 and H-09/I-14; obligations related but not identical).
- `chain check: merge`: 2 (T-03/Y-05, which is also the one-vote pair, and S-09/Y-06).
- `chain check: separate`: 1 (T-01/T-02).

## Chains

- I-12 with T-03 and Y-05: direct check T-03/Y-05 passes; one unit M-10 of three entries.
- I-17 with S-09 and Y-06: direct check S-09/Y-06 passes; one unit M-12 of three entries.
- I-06 with T-01 and T-02: direct check T-01/T-02 fails (a merged sentence is either a list of two checks or the family T membership test). Both links have three votes; I kept I-06/T-02 (I-06's falsifiability wording and rule 428 match T-02) and recorded I-06/T-01 as `majority not applied`. T-01 stays its own unit.
- H-08 with K-04 (three votes) and K-01 (one vote): K-01 kept separate, so no chain.
- I-14 with S-18 (three votes) and H-09 (one vote): H-09 kept separate, so no chain.

## Units made from merges (14)

| unit | members | families | distinct rules | list |
|---|---|---|---|---|
| M-01 | A-04, I-05 | A, I | 8 | units.json |
| M-02 | A-05, H-12 | A, H | 2 | units.json |
| M-03 | D-01, H-11 | D, H | 2 | units.json |
| M-04 | D-02, S-20 | D, S | 7 | units.json |
| M-05 | D-03, H-13 (proxy group) | D, H | 1 | single_rule_units.json |
| M-06 | D-06, S-03 | D, S | 4 | units.json |
| M-07 | H-08, K-04 | H, K | 1 | single_rule_units.json |
| M-08 | H-10 (boundary register), S-06 | H, S | 8 | units.json (candidate pattern; H-10 belongs under its condition: migration completed, no caller, published API or supported release needs the old path) |
| M-09 | I-06, T-02 | I, T | 5 | units.json |
| M-10 | I-12, T-03, Y-05 | I, T, Y | 10 | units.json |
| M-11 | I-14, S-18 | I, S | 2 | units.json |
| M-12 | I-17, S-09, Y-06 | I, S, Y | 3 | units.json |
| M-13 | S-13, T-05 | S, T | 2 | units.json |
| M-14 | S-24, Y-07 | S, Y | 4 | units.json |

All 14 merged units span two or more families; M-10 and M-12 span three. No two entries of one family share a unit.

Totals: 114 entries form 98 units; 75 units hold two or more distinct rules (`units.json`), 23 hold one (`single_rule_units.json`).

## Pairs kept separate

- I-06 / T-01 (three votes): `majority not applied`.
- T-01 / T-02 (chain check): separate.
- H-08 / K-01 (one vote): separate.
- H-09 / I-14 (one vote): separate.

## Statement

No two final units are listed as one pattern by two or more coders, except the pair recorded as `majority not applied` (I-06/T-01).
