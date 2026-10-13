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

## Approved policy decisions — 2026-10-13
- User-approved semantics: `@School` = students attend school **today**.
- Evening/Modes timing must use **tomorrow's** student attendance, not today's `@School`. The read-only evaluator now exposes `tomorrow_status`; the WebCoRE consumer change is NOT implemented.
- User accepts scraping the district's published academic calendar as authoritative, without requiring manual approval of each routine calendar update.
- Academic calendar only; ignore events calendars.
- District page exposes the academic calendar as a linked interactive app and official PDF; the main page itself does **not** list all closure dates. A scraper must fetch and parse the actual academic calendar, not infer days from page headings or events.
- Source extraction is not implemented or tested yet. The provisional dataset remains blocked until a scraper with validation, source provenance and regression fixtures is implemented.
- Scraper acceptance: reject missing year boundaries, missing/ambiguous closure labels, implausibly sparse data, unexpected structural changes, or contradictory dates. Retain last-known-good verified snapshot and alert on rejection; do not promote unverified content.
- Distinguish daily runtime freshness checks from monthly content-change monitoring. Monthly ChatGPT report alone cannot guarantee a same-day closure update.

## ChatGPT publishing architecture
See CHATGPT_HANDOFF.md. The monthly ChatGPT task currently reports changes; unattended GitHub publishing remains unverified. The new intake.py and validate.py validate a proposed verified calendar JSON but do not scrape the district website or write to WebCoRE. Run tests with `python -m unittest discover -s school_calendar -p 'test_*.py'` from the repository root. Do not merge before tests and the academic source are verified.
