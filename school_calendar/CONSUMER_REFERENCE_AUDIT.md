> Historical October 13 preparation record. Current implementation, validator state and gates are in README.md and PRODUCTION_CUTOVER.md.

# Modes and Scheduled Actions: inspected live references

Read-only inspection of current native WebCoRE bodies (2026-10-13).

## Modes

Piston `:610151aa2ec89c411b197dcad7666d44:` contains exactly two `@School` operands, both in the dusk/evening scheduling decision:

- `$.s[0].s[0].s[2].c[1].lo` (school true)
- `$.s[0].s[0].s[2].ei[0].c[1].lo` (school false)

Both should become `@SchoolTomorrow` together. A **prepare-only** native draft was submitted with exactly these substitutions. It returned `ok:false` because the currently deployed validator rejects native optional placeholders in an unrelated restriction (`$.s[2].s[0].r[0]`); the CLI source fix in webcore-CLI PR #6 passed CI but is not deployed. No live change was applied.

## Scheduled Actions

Piston `:a470dd843787f6eec783ff7f9c1a96f5:` contains exactly two `@School` operands:

- `$.s[10].s[0].c[0].lo`
- `$.s[11].s[0].c[0].lo`

These remain **today** semantics and must not be replaced by `@SchoolTomorrow` without separately reviewing their scheduled actions. No change proposed for this piston.

## Cutover dependencies

Deploy the approved validator fix first, then prepare full native diffs and check expected hashes. The Variables writer must publish `@SchoolTomorrow` with tomorrow's date stamp before Modes reads it. Do not change the live Modes operands in isolation. Explicit approval is required for all production piston writes.

