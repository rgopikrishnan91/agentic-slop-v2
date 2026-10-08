# Coder instructions: step B, version 2: are the patterns unique across families?

Start in a fresh session with no earlier conversation. Use only the files in this folder. Do not use the web. Do not read any earlier result.

## Files

- `patterns_kind_reviewed.json`: the entries of all 11 families, each with its reviewed kind. Inside each family the entries are already unique.
- `rules.json`, `detector_source_inspections.json`, `families.json`: to read the rules of an entry and the family definitions.

## Question

A rule can be in two families, and the families touch each other. So the same failure can occur in two families under two names. Find every pair of entries **in two different families** that is one pattern.

Do not list a pair of entries of the same family. That question is closed.

## Labels

- `SAME`: the two entries break the same obligation and accept the same legitimate cases.
- `HIGHLY SIMILAR`: one entry is a special case of the other, or they differ only in artifact type, language, detection method, or the point of view of the family, **and** the pair passes the merge test below. Name the entry with the broader obligation in `broader`.
- A pair you do not list is `DISTINCT`.

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

## What to do

1. Read all entries: candidate patterns first, then boundary registers, then proxy groups.
2. Compare every entry with every entry of the other families. Do not sample.
3. For each pair that you think is one pattern, write the merged obligation sentence and apply the merge test. List the pair only if the test passes.

## Output

`across_pairs.json`: a JSON array of objects:

```
{"a": "<entry id>", "b": "<entry id>", "label": "SAME | HIGHLY SIMILAR", "broader": "<entry id or empty>",
 "merged_invariant": "the one sentence that covers both",
 "reason": "one or two sentences that state the two obligations and why they are one"}
```

List only SAME and HIGHLY SIMILAR pairs. Do not put DISTINCT pairs in this file. Write each reason for that pair; do not use one sentence form for all pairs.

Also write `run_info.json`: role, the model identifier that the system reports, effort setting, date, tools used. Do not delegate the work.
