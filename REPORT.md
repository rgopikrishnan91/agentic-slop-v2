# Report: Task 1 rerun (Claude run), kind review and step B version 2

Orchestrator log: `log/orchestrator_log.md`. Per-session log (session id, dispatched model, reported model, effort): `log/sessions.tsv`. Role outputs: `work/`.

## Sessions

38 fresh cloud sessions, each started from its own branch holding only its clean folder.

| Step | Role | Sessions | Dispatched model | Reported model (all sessions) |
|---|---|---|---|---|
| Kind review | Coder 1 | 11 | claude-opus-4-6 | claude-opus-4-6 |
| Kind review | Coder 2 | 11 | claude-opus-4-8 | claude-opus-4-8 |
| Kind review | Coder 3 | 11 | claude-opus-5 | claude-opus-5 |
| Kind review | Judge | 1 (family A) | claude-opus-5-5 | claude-opus-5-5 |
| Step B | Coder 1, 2, 3 | 1 each | as above | as above |
| Step B | Judge | 1 | claude-opus-5-5 | claude-opus-5-5 |

Every session reported its model from the platform (`session_context.model` and `last_served_model`), and every one matched the roster. No fallback occurred.

## Step 1: kind review

- **Agreement:** Fleiss' kappa over the three coders is **0.892** (114 entries).
- **Entries by agreement:** 106 full agreement, 7 with a 2-of-3 majority, 1 decided by the judge (A-03, boundary register).
- **Entries by kind:** candidate pattern 79, proxy group 20, boundary register 15.
- **Misfit rules** (rules that two or more coders gave a different kind from their entry): 20 distinct rules, 21 rule-in-entry memberships.
- `check_output.py` on `patterns_kind_reviewed.json`: OK (384 memberships, as expected).

## Step 2: step B, version 2

**Pairs listed by each coder**

| Coder | SAME | HIGHLY SIMILAR | Total |
|---|---|---|---|
| Coder 1 | 6 | 13 | 19 |
| Coder 2 | 5 | 12 | 17 |
| Coder 3 | 6 | 11 | 17 |

`pair_votes.py` found no errors. It gave 20 distinct pairs: 16 with three votes, 1 with two votes, and 3 with one vote. So 17 pairs had two or three votes.

**Judge decisions (22)**

| Decision | Count |
|---|---|
| merge | 16 |
| separate | 2 (one-vote pairs H-08/K-01 and H-09/I-14) |
| majority not applied | 1 (I-06/T-01) |
| chain check: merge | 2 (T-03/Y-05, S-09/Y-06) |
| chain check: separate | 1 (T-01/T-02) |

- **`majority not applied`:** I-06/T-01 had three votes. The judge kept the chain link I-06/T-02 instead. The direct T-01/T-02 check failed: a sentence covering both was either a list or family T's own membership test. Both links had three votes, and the judge chose I-06/T-02 for its closer obligation and the rule the two share (428).
- **Units made:** 98 units. 75 have two or more distinct rules and 23 have one rule.
- **Merged units:** 14, and all 14 span two or more families. Two of them span three families: M-10 (I-12, T-03, Y-05) and M-12 (I-17, S-09, Y-06).
- **Merged units that hold only one rule:** two, and both are in the one-rule list: M-05 (D-03 + H-13, proxy group) and M-07 (H-08 + K-04).
- **Candidate pattern with a boundary register:** M-08 (H-10 + S-06). H-10 belongs under the condition that the migration is complete and nothing still needs the old path.
- **Checks:** `check_output.py patterns_agreed.json` is OK, and `check_step_b.py` is OK with no warnings. Both were run by the judge and run again by the orchestrator.

## Final

| List | Units | candidate pattern | proxy group | boundary register | Entry memberships | Rule memberships | Distinct rules |
|---|---|---|---|---|---|---|---|
| Pattern units (two or more rules) | 75 | 59 | 10 | 6 | 89 | 335 | 307 |
| One-rule units | 23 | 6 | 9 | 8 | 25 | 23 | 22 |

Three rules appear in both lists. Together the two lists cover all 326 rules.

## Limits

1. **Kind hints in entry texts.** The names and rationales of the entries were written by coders who had a kind in mind, so some texts hint at an earlier kind. The kind review instructions told the coders to decide from the rules.
2. **Rerun designed after a first step B.** This rerun was designed after the results of a first step B were seen. *The first result and the reason for the change are not in the handover package, so the orchestrator cannot report them. The study lead must add them here.* No role was given any earlier result.
3. **One vendor.** All coders are Claude models. Agreement shows consistency, not validity.
4. **Effort.** The roster says "high", but the orchestrator cannot set effort when creating a session. Sessions report "high" or "default" in their run_info. The family A kind-review judge reported that the harness effort setting was **low**.
5. **Isolation.** Each session got a clean folder on its own git branch (depth-1 clone). All branches are in one repository, so a session could in principle fetch another branch. The prompts forbade this, and every session changed only its own output files. Coders of one step ran in parallel. No coder output reached the orchestrator branch before all coders of that step had finished.
6. **Judge folder addition.** `tools/check_output.py` reads `step_b/coder/rules.json` relative to `tools/`. An identical copy of `rules.json` was placed at that path in the step B judge folder so the script runs unedited. No tool or role output was edited.
7. **Prompt additions.** Session prompts added operational instructions (output paths, commit to own branch, report model via `get_session`, no delegation). Step B prompts allowed scripts for layout and file assembly but not for decisions or reasons. The prompt texts are in `log/prompts/`.
