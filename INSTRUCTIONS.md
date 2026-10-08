# Coder instructions: kind review

Start in a fresh session with no earlier conversation. Use only the files in this folder. Do not use the web, except to open a tool URL from `rules.json` when a rule description is not clear.

## The task

`entries/<family code>.json` holds the entries of one family. Each entry is a group of rules that an earlier step put together. The groups are fixed. For each entry, decide its kind: `candidate pattern`, `proxy group` or `boundary register`.

No kind is given in the entry. Do not try to guess an earlier kind from the name or the rationale of the entry: these texts were written by other coders and can be wrong about the kind. Decide from the rules of the entry.

## Files

- `entries/<family code>.json`: the entries of the family (id, name, rationale, invariant, roles, relations, legitimate case, rule IDs).
- `rules.json`: the rules. `detector_source_inspections.json`: notes on what some detectors do.
- `families.json`: the family definitions.

## The kind test

Apply this test to each rule of the entry. Read the rule in `rules.json` (name and full description) and, if there is one, its note in `detector_source_inspections.json`. Ask the questions in this order and stop at the first "yes".

1. **Does the rule text itself say what is wrong?** Then the rule is a `candidate pattern` rule. This is so also when the rule uses a number or a keyword to find the case, if the text says what the failure is.
2. **Does the rule only count, measure, or match a word, and not say what is wrong?** Then the rule is a `proxy group` rule. It selects code for a person to look at.
3. **Does the rule state a failure that belongs to this family only if an added condition holds, and the rule does not check that condition?** Then the rule is a `boundary register` rule. Write the condition.

If no question gives "yes", use question 1 or 2, whichever is nearer, and say so in the reason.

The kind is not a measure of how sure you are, and it is not a measure of how good the detector is. A rule with a weak detector can still state a failure.

### Examples (they are not from the rule set of this study)

Suppose a family "Accessibility failures: the interface cannot be used by a person who relies on assistive technology."
- "An image element has no text alternative." Question 1: yes. It says what is wrong. Candidate pattern.
- "A caption longer than 40 characters is cut off by its container." Question 1: yes. It uses a number, but it says what is wrong (text is cut off). Candidate pattern.
- "A page has more than 30 images." Question 1: no. Question 2: yes. It is a count; it does not say what is wrong. Proxy group.
- "The word 'click' occurs in a link text." Question 1: no. Question 2: yes. It matches a word. Proxy group.
- "An animation starts by itself when the page opens." Question 1: it states a possible failure, but it is an accessibility failure only if the user has no way to stop the animation, and the rule does not check that. Question 3: yes. Boundary register, with the condition "the user cannot stop the animation".

### From the rules to the entry

The kind of the entry is the kind that most of its rules get. If two kinds have the same number of rules, take the kind of the rules that the entry's invariant describes, and say so. List each rule whose own kind is different from the kind of the entry in `misfit_rules`. Do not move, split or join rules: the groups are fixed in this step.

## Sessions

One family in each fresh session. In each session read these instructions, the family definition, the entries of the family, and every rule of those entries.

## Output

`kinds/<family code>.json`: a JSON array with one object for each entry of the family:

```
{"entry_id": "X-01",
 "kind": "candidate pattern | proxy group | boundary register",
 "question": 1,
 "condition": "for a boundary register: the added condition; else an empty string",
 "reason": "one or two sentences about what the rules of this entry check",
 "rule_kinds": {"<rule id>": "candidate pattern | proxy group | boundary register"},
 "misfit_rules": [{"rule_id": "<rule id>", "kind": "<its own kind>", "reason": "one sentence"}]}
```

`rule_kinds` has every rule of the entry. Write each reason for that entry; do not use one sentence form for all entries and do not generate reasons with a script.

Also write `run_info/<family code>.json`: role (coder 1, 2 or 3), the model identifier that the system reports, effort setting, date, tools used. Do not delegate the work.
