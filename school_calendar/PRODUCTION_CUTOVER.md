# Controlled native school-calendar cutover

Status: prepared, not deployed (2026-10-14).

## Exact scope

- Variables: preserve baseline sections 1, 4, 13, 16 and 20; retire only sections 7 and 10. Add one constant closure lookup, one captured local timestamp, and 00:05/04:50/17:00/sunset refreshes.
- School Mornings: retain both restrictions and every device command/schedule; append the date-freshness restriction.
- Modes: replace exactly two @School operands with @SchoolTomorrow; no other logic changes.
- Scheduled Actions: no change.
- TEST: temporarily replace its paused, device-free baseline with seven approved local-only validation bodies; execute 64 calendar/time cases and 16 native freshness-restriction cases. Restore the original body and paused state after testing/cutover.

## Gates and sequence after approval

1. Recheck identities, active states and original remote hashes. Stop on any intervening change; do not silently regenerate approval payloads.
2. Inspect the four native global names and types through the supported dashboard. The currently exposed MCP tools do not expose a global inventory/create method; prepare success is not evidence that globals exist. Dashboard fallback requires authorization. Preserve existing values/types, and create only missing @SchoolTomorrow boolean (false), @SchoolDate string (empty) and @SchoolTomorrowDate string (empty). Existing @School must be boolean. Do not replace a type mismatch without a fresh review.
3. Apply/run each approved TEST batch, using fresh remote hashes for each sequential transition and its original proposed body/payload hashes. Resume TEST temporarily only if required to execute; no devices, globals, other pistons, HTTP or schedules occur in these seven bodies. Require every expected PASS, no FAIL, no expression/type errors, and US/Central timezone. Missing logs are a failed gate, not a pass. Restore its original definition and paused state on failure.
4. Only after the matrix passes, finalize runtime evidence and merge reviewed source to main. Keep the prepared production bodies byte/logic-equivalent; changed logic requires fresh approval.
5. Apply School Mornings freshness guard first and verify persistence/activation.
6. Apply Variables writer and verify persistence, activation, retired competing writers and scheduled refreshes.
7. Use the separately prepared TEST_seed body for a single explicit initialization of the four school globals from a captured real current timestamp. This writes globals and may cause normal subscribed automation reevaluation; it is part of the production approval, not an isolated local-only test. It has no device commands. Never test the full Variables piston: that could force unrelated holiday/guest/late-arrival blocks.
8. Read all four global types/values back through the approved dashboard and compare to the pure calendar evaluator for the current local date. Stop before Modes if initialization is missing or wrong.
9. Apply Modes' exact two substitutions and verify persistence/activation. Reconfirm Scheduled Actions stayed unchanged. Restore TEST's original body and paused state, record all hashes/builds/log evidence, update retained context, and retire temporary testing state.
10. Verify the next natural daily refresh and the next scheduled School Mornings/Modes behavior through read-only logs. No live lighting test is included.

## Dusk ordering

Modes can calculate dusk after 17:30 based on sustained lux, before solar sunset. A sunset-only initialization is therefore insufficient after missed morning refreshes. The new 17:00 refresh precedes that earliest calculation by 30 minutes; 00:05 and 04:50 normally already publish identical school values. Sunset is an idempotent refresh. Cutover initializes and verifies the pair before changing Modes. No cross-piston wait or external scheduler is introduced. A complete hub/runtime failure can still prevent all refreshes; this schedule is not a claim of transactional or outage-proof global delivery. School Mornings fails closed on a stale date.

## Rollback

Native pre-change bodies for all five pistons are in cutover/2026-10-14/baselines. Restore Modes before removing its producer. Keep the School Mornings freshness guard until the restored writer's safety policy is reviewed; restoring the original unguarded morning body is a separate deliberate rollback action. Preserve any newly created globals until consumers no longer reference them; do not invent a delete API. Restore TEST and its paused state in all outcomes. Use prepare/apply/readback and approved intended hashes for rollback; never replay an accepted write.
