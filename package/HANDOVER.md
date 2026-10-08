# Handover: Task 1 rerun, kind review and step B version 2 (Claude run)

This package starts from the output of step A of the same run: one list of entries for each of the 11 families. Round 1 and step A are not run again. Two steps are run, in this order: the kind review, then step B version 2. See `ROSTER.md` for the models.

## What is in the package

- `kind_review/coder/`: instructions, `entries/<family>.json`, `rules.json`, `detector_source_inspections.json`, `families.json`.
- `kind_review/judge/INSTRUCTIONS.md`.
- `step_b/coder/`: instructions, `rules.json`, `detector_source_inspections.json`, `families.json`. The entry file is added by a script after the kind review.
- `step_b/judge/INSTRUCTIONS.md`.
- `tools/`: scripts for the orchestrator.

The entries in `kind_review/coder/entries/` are the step A entries without their earlier kind and without the notes of the earlier judge.

## Step 1: kind review

1. **Coders.** Coder 1, coder 2 and coder 3, each with one fresh session for each family (33 sessions). Clean folder for a session: `kind_review/coder/` with only the one family file in `entries/`. Output: `kinds/<family>.json` and `run_info/<family>.json`.
2. **Tally.** `python3 tools/kind_votes.py <c1 kinds dir> <c2 kinds dir> <c3 kinds dir> kind_votes`. It writes `kind_votes/<family>.json` and `kind_votes/_summary.json` (Fleiss' kappa, entries with full agreement, with a majority, with no majority).
3. **Judge.** One fresh session for each family that has one or more entries with no majority. Clean folder: `kind_review/judge/INSTRUCTIONS.md`, the family's `entries` file, `rules.json`, `detector_source_inspections.json`, `families.json`, and `kind_votes/<family>.json`. Output: `kind_decisions/<family>.json`.
4. **Apply.** `python3 tools/apply_kinds.py kind_votes <kind_decisions dir> step_b/coder/patterns_kind_reviewed.json`. It writes the entries with the reviewed kind, the condition of each boundary register, and `kind_misfit_rule_ids` (rules that two or more coders gave a different kind from the entry). It stops if an entry has no kind.

## Step 2: step B, version 2

1. **Coders.** Coder 1, coder 2 and coder 3, one fresh session each (3 sessions). Clean folder: `step_b/coder/` with `patterns_kind_reviewed.json`. Output: `across_pairs.json`, `run_info.json`.
2. **Tally.** `python3 tools/pair_votes.py c1/across_pairs.json c2/across_pairs.json c3/across_pairs.json step_b/coder/patterns_kind_reviewed.json > pair_votes_across.json`. The script stops with an error if a file lists a pair of one family or a label that is not SAME or HIGHLY SIMILAR. Then send the file back to that coder's session to correct it; do not edit it yourself.
3. **Judge.** One fresh session. Clean folder: `step_b/judge/INSTRUCTIONS.md`, `patterns_kind_reviewed.json`, `rules.json`, `detector_source_inspections.json`, `families.json`, the three pair files as `coder1.json`, `coder2.json`, `coder3.json`, `pair_votes_across.json`, and `tools/`. Output: `patterns_agreed.json`, `units.json`, `single_rule_units.json`, `decisions.json`, `independence_log.md`, `run_info.json`.
4. **Check.** `python3 tools/check_output.py patterns_agreed.json` and `python3 tools/check_step_b.py <judge output dir>`.

## Rules for the orchestrator

- The orchestrator moves files and runs the scripts. It does not code and does not judge.
- Every session is fresh: no earlier conversation and no memory. Each session gets a clean folder with only the files named above.
- Give no role any file that is not in this package or made by a step of this package. In particular: no round 1 files, no step A coder files or pool files, no result of an earlier step B, no report or agreement number of an earlier run, no result of another vendor's run, no earlier atlas, and no rule labels.
- Do not edit a role's output. If a script rejects a file, return it to the same session with the script's message. If an edit cannot be avoided, keep the original file, and write in the log what was changed and why.
- Keep a log with the session identifier, dispatched model and reported model of every session.

## What to report

- Kind review: Fleiss' kappa over the three coders; entries with full agreement, with a majority, and decided by the judge; entries by kind; number of misfit rules.
- Step B: pairs listed by each coder, by label; pairs with two or three votes; decisions of the judge by type; units made; units that span two or more families; any `majority not applied`.
- Final: pattern units (two or more rules) by kind; one-rule units by kind; memberships in each list.

## Limits to report

- The names and rationales of the entries were written by coders who had a kind in mind, so some texts hint at an earlier kind. The kind review instructions tell the coder to decide from the rules.
- This rerun was designed after the results of a first step B were seen. Report the first result and the reason for the change.
- The coders are models of one vendor. Agreement shows consistency, not validity.
