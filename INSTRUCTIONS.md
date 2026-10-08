# Judge instructions: kind review

You are the judge (Claude Opus 5.5, high effort). You are not a fourth coder. One fresh session for each family that has entries with no majority. Use only the files in your folder. Do not read any earlier result.

## Inputs for a family

`entries/<family>.json`, `rules.json`, `detector_source_inspections.json`, `families.json`, the kind test below, and `kind_votes/<family>.json` from the orchestrator. The vote file lists, for each entry, the kind and reason of coder 1, coder 2 and coder 3, and marks the entries with no majority.

## What to decide

1. An entry for which two or three coders give the same kind is settled. Do not change it.
2. For each entry with no majority (three different kinds), apply the kind test to each rule of the entry yourself, read the three reasons, and decide the kind. Give one or two sentences of reason that name what the rules check.
3. For a boundary register, write the condition.

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

## Output

`kind_decisions/<family>.json`: a JSON array with one object for each entry you decided: `entry_id`, `kind`, `condition`, `reason`, `rule_kinds`, `misfit_rules` (same form as the coder output). Also `run_info/<family>.json`.
