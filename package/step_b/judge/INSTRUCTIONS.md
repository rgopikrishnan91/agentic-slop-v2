# Judge instructions: step B, version 2

You are the judge (Claude Opus 5.5, high effort). You are not a fourth coder. One fresh session. Use only the files in your folder. Do not read any earlier result.

## Inputs

`patterns_kind_reviewed.json`, `rules.json`, `detector_source_inspections.json`, `families.json`, the three coders' `across_pairs.json` (as `coder1.json`, `coder2.json`, `coder3.json`), and `pair_votes_across.json` from the orchestrator.

## The merge test

Two entries can be one pattern only if all of these hold.

1. **One obligation, in one statement.** You can write one sentence, "X must ...", that covers both entries and that tells a reviewer what to look for in code, without reading the member rules. If the sentence needs a list joined by "or" (several artifacts, several mechanisms, several kinds of check), or if it is so general that it could cover most entries of a family, the test fails.
2. **The legitimate cases stay valid.** Each case that one entry accepts as legitimate is also acceptable under the merged obligation.
3. **Same kind.** Both entries have the same kind. One exception: a candidate pattern and a boundary register can be one pattern if, under the condition of the boundary register, its failure is the obligation of the candidate pattern. A proxy group states no obligation, so it can be merged only with a proxy group that uses the same measure.

Shared rules are not enough: one rule can show two different failures, and that is why it is in two families. A shared symptom is not enough.

### Examples (they are not from the rule set of this study)

- Family P has "Image without a text alternative". Family Q has "Icon button with no accessible name". Merged obligation: "Every non-text control or image must expose a text equivalent." One statement; a reviewer knows what to check; the legitimate case (an image that carries no information and is marked as such) is valid for both. The test passes.
- Family P has "Money amount stored in a floating-point type". Family Q has "Timestamp stored without a time zone". A merged obligation would be "A stored value must use a type that keeps its meaning", which could cover most data entries, or "amounts must be exact or timestamps must carry a zone", which is a list. The test fails. They stay two patterns.
- Family P has "User-facing text that is not passed through the translation function" and family Q has an entry with the same obligation and the same legitimate case, written from the point of view of Q. These obligations are identical. The test passes.

## What to decide

1. **Pairs listed by two or three coders.** Apply the merge test. Write the merged obligation. If the test passes, the two entries become one unit. If you cannot write the merged obligation without a list or without making it general, do not merge: record the pair as `majority not applied` with the reason. This must be rare; the coders applied the same test.
2. **Pairs listed by one coder.** They stay separate. One exception: you find that the two obligations are identical (the same obligation and the same legitimate cases; they differ only in the point of view of the family). "Similar" or "special case" is not enough for a pair with one vote.
3. **Chains.** If A merges with B and B merges with C, check A against C directly with the merge test before you make one unit of the three. This is so also when A and C are in the same family. If A with C fails, do not make one unit: keep the link with more votes and leave the other entry separate; say which.
4. **No other merging inside a family.** Two entries of one family can be in one unit only through rule 3, with the direct check written down.
5. **Kind of a unit.** By the merge test, the entries of a unit have the same kind, or they are a candidate pattern with a boundary register; then the unit is a candidate pattern and you write the condition under which the boundary register belongs.
6. **Units with one rule.** After merging, a unit that holds one distinct rule is not counted as a pattern. It goes to the separate list. Do not merge it into another unit to avoid this.
7. **Reasons.** For each decision write the two obligations in your own words and say why they are, or are not, one. A sentence that could be put under any pair is not a reason. A script checks for repeated reasons.

## Output

- `patterns_agreed.json`: every entry of `patterns_kind_reviewed.json` with a `unit_id`. In a merged unit, write the same unit name, invariant, legitimate case and kind into each member entry, and keep the entry's own text in `entry_name`, `entry_invariant`, `entry_legitimate`. An entry that is not merged has its own `unit_id`.
- `units.json`: the units with two or more distinct rules: `unit_id`, `name`, `invariant`, `legitimate`, `kind`, `member_entries`, `families`, `rule_ids`.
- `single_rule_units.json`: the units with one distinct rule, in the same form.
- `decisions.json`: one object for each pair in `pair_votes_across.json` and for each chain check: `a`, `b`, `votes`, `decision` (`merge`, `separate`, `majority not applied`, `chain check: merge`, `chain check: separate`), `merged_invariant` (for a merge), `reason`.
- `independence_log.md`: units made, pairs kept separate, and the statement that no two final units are listed as one pattern by two or more coders, except the pairs recorded as `majority not applied`.
- `run_info.json`.

Run `python3 tools/check_output.py patterns_agreed.json` and `python3 tools/check_step_b.py .` and correct every error.
