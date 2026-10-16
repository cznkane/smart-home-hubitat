> Historical October 13 preparation record. Current implementation, validator state and gates are in README.md and PRODUCTION_CUTOVER.md.

# Live @School dependency audit — 2026-10-13

Read-only WebCoRE inventory: 16 pistons, **16 active, 0 paused**. This supersedes earlier conversation claims that School Mornings remained paused. No live changes were made.

All 16 piston definitions were retrieved and scanned for exact `@School` references; one batch experienced MCP initialization conflicts, and the affected pistons were retried individually.

| Piston | Role | Cutover risk |
|---|---|---|
| Variables | **Writer**; sets @School false/true on seasonal sunset dates | Must remove/retire competing seasonal writes at controlled cutover |
| School Mornings | Reader; @School true AND @KidsPresent true restriction | Live piston is active; daily freshness/suppression needed before rollout |
| Modes | Reader; tests @School true and false | Mode/evening timing will change on holidays and weekends; require behavior approval |
| Scheduled Actions | Reader; tests @School true and false | Sadie Noise school/non-school timing changes; require behavior approval |

The other 12 pistons returned no exact `@School` references in their retrieved definitions. This scan is a direct-reference audit, not a guarantee against indirect/global-dependent behavior.

## Release blockers
1. Validate every academic closure date against official approved district PDF. Provisional JSON is intentionally unusable by production evaluator.
2. Execute tests in a clean environment; expand boundary, invalid data, time zone, leap-year, and stale-data coverage.
3. Clarify Modes and Scheduled Actions school/non-school behavior with user, including weekends and holiday evenings.
4. Design secure, supported, authenticated WebCoRE global-variable write/readback path. The current MCP tools do not expose a direct global-variable writer.
5. Implement daily date-stamped freshness guard so a stale `@School=true` cannot fire School Mornings on an unsynced closure date.
6. Confirm approved runtime and recovery path before any scheduler deployment.
7. Preserve rollback and obtain separate approval for live piston/global changes and live tests.

No deployment authorized.

