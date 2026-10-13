# Leander ISD academic-calendar engine (draft)

**No production integration is installed.** This is an isolated, read-only calculation library.
The supplied 2026–27 dataset is deliberately marked `provisional`: `load_calendar`
rejects it until the official approved academic-calendar PDF is independently
verified date by date. No source extraction has been claimed.

Source: https://www.leanderisd.org/calendar/
Use the approved academic-calendar PDF linked from the district page; verify its URL before recording it.

Run from repository root:
`python -m unittest school_calendar.test_calendar`

## Architecture and release gates
- Academic calendar only. Do not ingest district event calendars.
- `@School` means **students attend school today**, not merely that the school year is active.
- Weekend, outside school year, and student closure -> false.
- Early-release days remain true.
- Explicit manual date override (future work) wins over calendar.
- Compute in America/Chicago, publish ahead of 5 AM.
- A successful read must be paired with a **date-stamped** result. Never reuse yesterday's boolean for today's date.
- If calendar missing, stale, invalid, or not verified: fail closed **at the publisher** (no write); raise alert and preserve current state. Note: preserving an old global alone does not safely suppress School Mornings; a separate freshness guard is required before production.
- Audit every consumer of `@School` (especially Modes, Scheduled Actions, Variables and School Mornings) before changing its meaning.
- Retire the legacy Variables piston seasonal `@School` writes only after the new publisher has been validated and cut over; never allow competing writers.
- Production publisher needs supported authenticated WebCoRE API access, protected secrets, idempotent writes, retry/backoff, health monitoring, readback, recovery and rollback. **Not implemented here.**
- Do not resume paused School Mornings or trigger lighting tests without separate approval.
- Monthly ChatGPT task is informational and does not change this repository or production.
- Update/verify the academic dataset annually, and compare official revisions before merging.
- Source inspection, test execution and production integration are separate evidence gates.

## Status
Draft PR for review; no live writes.
