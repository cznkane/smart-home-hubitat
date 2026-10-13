# School Mornings: native freshness-guard proposal

Live piston: `:917583854fbc49e5610e0ef27c2aa6d0:`. Read-only baseline has two top-level restrictions: `@School is true` and `@KidsPresent is true`. These gate the 05:00, 06:00 and 08:00 scheduled lighting actions.

## Proposed native restriction

Append a third top-level restriction (`rop: and`):

- `co: is`
- `lo: expression formatDateTime($now, "yyyy-MM-dd")`, with the native parsed `formatdatetime` function shape observed in TEST
- `ro: variable @SchoolDate`
- `ro2`, `to`, `to2`: native optional placeholders `{"g":"any","t":"c"}`

This compares local calendar date to the published date stamp; mismatches must block all three schedules. Preserve all existing device commands, brightness, temperatures, schedules and `@KidsPresent` restriction. The guard's function AST was extracted from TEST; the restriction itself has not been runtime evaluated.

## Preparation result

An in-memory native draft with the above third restriction was sent to `webcore_prepare_piston_update`. The currently deployed CLI 0.4.10 returned `ok:false`, solely reporting optional operand placeholders in the existing and proposed restrictions. [CLI PR #6](https://github.com/cznkane/webcore-CLI/pull/6) addresses this and passes CI, but the connector still reports deployed 0.4.10. Do not remove or fabricate optional operands to make the validator pass. Deploy the reviewed fix first, then rerun prepare and inspect the diff.

**No production piston modified.**
