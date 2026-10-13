# Production cutover plan (not yet deployed)

## Confirmed live state, 2026-10-13
- `Variables` is an active piston and writes `@School` seasonally at April 27 and July 11 sunsets. Its holiday and guest logic must be retained.
- `School Mornings` is active and gates on `@School == true` and `@KidsPresent == true`; it runs weekday actions at 05:00, 06:00, and 08:00. No freshness guard exists.
- 16 pistons active, none paused when last checked.

## Required before production
1. Establish a supported authenticated Hubitat/WebCoRE daily writer, with secrets stored outside Git. The current WebCoRE MCP connector cannot directly set global variables.
2. Publish `@School`, `@SchoolDate`, `@SchoolTomorrow`, and `@SchoolTomorrowDate` from one calendar snapshot in America/Chicago. Make writes idempotent; confirm readback and report failure.
3. Change School Mornings to require `@SchoolDate == local today` as well as `@School == true` and `@KidsPresent == true`. If the writer fails, a stale date must block all morning actions.
4. Update evening logic in `Modes` to use `@SchoolTomorrow` with a matching tomorrow date, and assess `Scheduled Actions` independently for whether it should use today or tomorrow.
5. Retire only the two competing `@School` writes in `Variables`, leaving holiday, guest, and late-arrival logic untouched.
6. Validate normal school weekday, weekend, school closure, early release, stale-date, missing-file, and year-end cases. Use no live lighting tests unless separately approved.
7. Backup all four piston definitions, prepare reviewable diffs and remote hashes, apply only through the approved WebCoRE update workflow, then verify persistence and readback.

## Rollback
Restore the four pre-cutover piston definitions and the old Variables writer if needed; preserve captured hashes and verify the restoration. Do not use an unguarded `@School=true` as a fallback on publisher failure.

## Annual operations
Interpret the official district academic calendar once per year and commit the verified snapshot. Daily evaluation is local and does not depend on ChatGPT task execution. The monthly report-only task is optional.

## Status
Blocked on supported daily variable delivery and freshness-guard implementation. No live piston modification is authorized by this document.
