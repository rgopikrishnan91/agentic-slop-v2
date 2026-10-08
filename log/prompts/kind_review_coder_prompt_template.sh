#!/bin/bash
c=$1; f=$2; m=$3
cat <<P
You are Coder $c in the kind review step of a research coding study. This is a fresh session. The repository root is your folder; it holds only the files for this session: INSTRUCTIONS.md, entries/$f.json, rules.json, detector_source_inspections.json, families.json.

Read INSTRUCTIONS.md and follow it exactly for family $f. Read the family definition, every entry in entries/$f.json, and every rule of those entries (name and full description in rules.json, plus its note in detector_source_inspections.json when there is one).

Rules for this session:
- Use only the files in this folder. Do not fetch, list, or check out any other git branch, and do not read any file outside this folder. Do not use the web, except to open a tool URL from rules.json when a rule description is not clear.
- Do the work yourself. Do not use subagents, workflows, or any other agent or model.
- Do not generate reasons with a script; write each reason for its entry.

Output (create these two files):
- kinds/$f.json in the format given in INSTRUCTIONS.md.
- run_info/$f.json with: role ("coder $c"), the model identifier that the system reports (call the get_session tool with no session_id and report session_context.model and external_metadata.last_served_model), effort setting, date, tools used.

The roster model for coder $c is $m. If the model that runs you is not $m, write the real one in run_info and say so in your final message.

When done, commit only kinds/$f.json and run_info/$f.json and push to branch orch/kr-c$c-$f (the branch you are on). Do not open a pull request. Final message: the files written, the number of entries by kind, and the model identifier reported.
P
