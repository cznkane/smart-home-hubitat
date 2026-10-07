# Automation Control and Maintenance Hold Architecture

**Status:** Approved requirement / architecture direction; implementation pending  
**Last reconciled:** 2026-10-07  
**Scope:** Global automation maintenance/kill control and selective function-level holds

## Purpose

Provide a deliberate operational control layer for temporarily suppressing Smart Home automation behavior without depending on ad hoc manual piston pausing or unsafe indiscriminate task cancellation.

This requirement arose during the School Mornings incident. The incident itself has since been forensically corrected: WebCoRE Pause **did** stop the investigated School Mornings `fadeLevel` progression. See `docs/SCHOOL_MORNINGS_ABORT_ARCHITECTURE.md` and Git issue #13.

The broader requirement remains valid independently of that corrected finding: Rick needs a dependable way to place automation globally or selectively into a maintenance/abort state.

## Architectural requirements

### Global control

Provide a clearly observable global automation hold/kill mechanism for managed automation.

The final design must define:
- what "global hold" suppresses;
- whether it blocks only new automation decisions or also aborts active work;
- how already-scheduled/delayed work is handled;
- what state survives the hold;
- what is cleared or invalidated;
- how normal operation resumes without releasing stale work.

A global control must fail safely and must not blindly erase durable truth such as occupancy, presence, or mode state.

### Function-level control

Support selective holds/abort controls where operationally valuable rather than requiring the entire automation system to be disabled.

School Mornings is the first demonstrated case and is tracked separately in #13. Other candidates such as Fade, DoorLights, Bedtime, or Scheduled Actions require their own blast-radius analysis before being included.

Prefer controls over logical automation functions. Do not assume WebCoRE piston Pause itself is the final user-facing abstraction.

### Pending/delayed work

Do **not** assume a generic "cancel all tasks" primitive is safe.

Current retained evidence shows:
- School Mornings `fadeLevel` uses repeated scheduled wakeups and can be stopped by targeted piston Pause.
- `cancelTasks` has broad per-piston pending-task semantics and no target task/statement parameter.
- Scheduled Actions owns many unrelated legitimate schedules.
- Fade, DoorLights, Bedtime, and other pistons also contain delayed/scheduled behavior.

For each controlled function, classify pending work before deciding whether to pause, cancel, invalidate, or allow it to complete.

Where future designs use a recorded pending intent/due time, revalidate authorization and current conditions at execution time so stale intent does not gain unconditional authority merely because it was once scheduled. This is a design principle, not a claim that existing School Mornings currently uses that pattern.

## Separation of concerns

- Keep effective-presence correctness upstream in Occupancy. The KidsAway / `@KidsPresent` defect was fixed there in Occupancy build 49 and must not be reintroduced as School Mornings-local policy.
- Keep School Mornings-specific abort mechanics in `docs/SCHOOL_MORNINGS_ABORT_ARCHITECTURE.md` / #13.
- Keep scheduling policy with the appropriate scheduling owner.
- Do not add duplicated global override checks across every piston without first defining a maintainable control contract.
- Do not use whole-house task cancellation until its blast radius is explicitly understood.

## User interface / observability direction

The control layer should ultimately be visible and operable from Hubitat and SharpTools.

Desired direction:
- prominent master automation hold/maintenance control;
- selected function-level controls where justified;
- clear current state so a forgotten hold is obvious;
- status-bridge exposure where appropriate.

Exact virtual-device, global-variable, attribute, naming, reset, and UI implementation is not yet selected. Names previously discussed such as `AutomationHold` or `SchoolMorningEnabled` are conceptual only and must not be treated as observed live variables.

## Recovery / safety requirements

The commissioned design must address:
- active work when hold is asserted;
- already-pending delayed/scheduled work;
- future recurring schedules;
- partial failure while aborting a function;
- reboot/restart persistence as appropriate;
- safe resume behavior;
- stale pending intent after resume;
- accidental long-term disablement;
- observability and operator feedback.

## Acceptance criteria for the architecture

1. Inventory candidate pistons/functions affected by a global hold and classify their active/pending work.
2. Define explicit semantics for global hold, global emergency abort, and function-level hold/abort.
3. Prove that asserting a control produces no unintended cross-piston cancellation.
4. Prove future legitimate recurring schedules recover correctly after release.
5. Prove stale disposable work cannot unexpectedly execute after release.
6. Preserve occupancy/presence/mode truth unless a separately approved design requires otherwise.
7. Expose clear control state in Hubitat and, when commissioned, SharpTools.
8. Document failure recovery and operator reset behavior.
9. Keep School Mornings-specific acceptance aligned with #13 rather than duplicating it.
10. Update canonical piston/archive state for any piston changes.

## Current status

Requirement approved; implementation not commissioned. No global control, virtual device, global variable, or generalized cancellation behavior is claimed to exist yet.
