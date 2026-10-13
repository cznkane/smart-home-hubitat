# WebCoRE Variables array payload — 2026–27

Generated from `academic_2026_2027.json` on the PR branch. **Draft data, not validated native piston syntax. Do not paste into live WebCoRE.**

School-year inclusive: 2026-08-12 through 2027-05-27. Weekends are not school days. Early-release days remain school days.

## Closure lookup (35 weekday dates)

```text
2026-09-07,2026-09-21,2026-10-09,2026-10-12,2026-10-13,2026-11-02,2026-11-03,2026-11-23,2026-11-24,2026-11-25,2026-11-26,2026-11-27,2026-12-21,2026-12-22,2026-12-23,2026-12-24,2026-12-25,2026-12-28,2026-12-29,2026-12-30,2026-12-31,2027-01-01,2027-01-04,2027-01-18,2027-02-12,2027-02-15,2027-02-16,2027-03-15,2027-03-16,2027-03-17,2027-03-18,2027-03-19,2027-03-26,2027-03-29,2027-04-26
```

## Intended daily evaluation

- Local timezone: America/Chicago.
- Today = local date; tomorrow = next local date.
- For each date: school = within school-year bounds AND weekday AND NOT contained in closure lookup.
- Publish today status and date to `@School` and `@SchoolDate`; tomorrow to `@SchoolTomorrow` and `@SchoolTomorrowDate`.
- Schedule update before School Mornings' 05:00 trigger and at dusk for evening Modes.
- Protect School Mornings with a same-date freshness check before retiring the seasonal writers.
- Preserve all unrelated Variables logic. Prepare native AST, validate expressions and inspect diff before any apply.

## Native AST verification outstanding

This file records the exact array input and algorithm; it does **not** assert that a comma-separated string is a WebCoRE array or that `contains` uses safe token-boundary semantics. Test exact membership (no substring collisions), native expression parse, date formatting, and full body validation before proposing an apply.
