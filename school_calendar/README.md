> **Historical engineering source preserved from PR #40.** Production is already deployed; see [authoritative production record](../docs/SCHOOL_CALENDAR_PRODUCTION_RECORD.md). Do not run historical candidate deployment procedures from this directory. Source/test preservation does not prove equivalence with current live pistons.

# Leander ISD native school-calendar engine

Status (2026-10-14): implementation and read-only preparation complete; on-hub TEST validation and production cutover require approval. No live pistons or globals have been changed by this engineering session.

The verified 2026–27 JSON is the annual source. Variables embeds one delimiter-safe closure lookup and derives today/tomorrow locally. No external API, publisher, or scheduler is required. Weekends, all 35 student closure dates, and dates outside August 12, 2026 through May 27, 2027 return false. Both early-release dates remain true.

Variables refreshes at 00:05, 04:50, 17:00, and sunset, using a captured timestamp for a consistent pair. It writes each boolean before its date stamp. Only the April 27 and July 11 seasonal school sections are retired; holiday, guest and late-arrival sections are retained exactly.

School Mornings retains @School and @KidsPresent, adding a current-local-date restriction. Modes changes exactly two evening operands to @SchoolTomorrow. Scheduled Actions remains unchanged and uses today.

Validation: 39 unit tests pass, Python syntax compilation passes, and 456 expression operands match the independently retrieved upstream dashboard parser after ignoring parser source-location annotations. All production candidates and seven device-free TEST batches pass live prepare at connector 0.4.14. These are not on-hub runtime results.

Run: `python -m unittest discover -s school_calendar -p 'test_*.py' -v`.

See [PRODUCTION_CUTOVER.md](PRODUCTION_CUTOVER.md), [NATIVE_RUNTIME_EVIDENCE.md](NATIVE_RUNTIME_EVIDENCE.md), and [APPROVAL_PACKAGE.md](APPROVAL_PACKAGE.md). The cutover directory contains native baselines, exact prepared candidates and hash manifests. Do not upload based on a unit test or `ok:true` alone.

Annual maintenance: interpret the official district academic calendar, validate and commit the next annual JSON, regenerate the native candidate, test boundaries/closures/early releases, and obtain the required production approval. A monthly reminder is informational and not a runtime dependency. After the final day, the native expression returns false until a new approved calendar is installed.
