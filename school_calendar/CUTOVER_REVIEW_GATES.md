# School-calendar cutover: review gates (October 2026)

## Verified

- Canonical academic calendar is marked verified; 35 weekday closure dates are generated.
- The isolated TEST piston supplies native parsed shapes for `contains`, `concat`, `formatdatetime`, and `$now`.
- A review-only four-assignment Variables draft passed structural preparation (`ok:true`); this is **not** runtime verification.
- CLI validator fix [webcore-CLI PR #6](https://github.com/cznkane/webcore-CLI/pull/6) passes GitHub CI, but is **not yet deployed**. It accepts native optional placeholders in School Mornings restrictions.

## Required before production approval

1. Verify native editor parsing and actual evaluation semantics for `addDays`, `weekDayName`, `isBetween`, nested `if`, string comparisons and boolean return types. Do not treat a manually constructed `exp` tree with `ok:true` as parser verification. Check that `formatDateTime` uses the Hubitat local timezone; test midnight and DST boundaries.
2. Produce complete native Variables body with safe midnight-before-05:00 refresh and dusk refresh, or another verified schedule that covers both consumers. Remove April 27 and July 11 seasonal `@School` writers only in the final cutover body. Preserve holiday, late-arrival and guest sections unchanged.
3. Produce School Mornings body with `@SchoolDate == formatDateTime($now, 'yyyy-MM-dd')` fail-closed restriction. Verify it protects all 05:00, 06:00 and 08:00 lighting sequences.
4. Modes currently references `@School` for its evening scheduling branch. Change to `@SchoolTomorrow` for evening logic only; keep today's semantics in Scheduled Actions unless inspection shows otherwise. Prepare both for review.
5. Re-run tests on all affected repos, deploy approved CLI fix to Windows VM, and use the updated live prepare validator. Review full diffs, stale remote hashes, rollback snapshots and all four piston dependencies.
6. Request explicit approval for exact production piston updates. Apply in fail-safe order, verify persisted bodies and variables, without executing live lighting tests.

**Current status:** not production-ready; no live pistons changed. The unresolved items are implementation and runtime semantics, not missing calendar data or user action.
