# School Mornings Cancellation and Abort Architecture

**Status:** Canonical design / forensic record  
**Last reconciled:** 2026-10-07  
**Scope:** School Mornings cancellation behavior and the reusable lessons for WebCoRE delayed/scheduled work

## Purpose

Preserve the evidence from the School Mornings pause investigation and define the current abort-control direction without carrying forward the disproven theory that pausing the piston failed to stop its active fade.

Live WebCoRE remains runtime truth. Re-inspect current piston state before a production change.

## School Mornings execution model

The investigated School Mornings piston has piston-level restrictions:
- `@School == true`
- `@KidsPresent == true`

Its retained schedule includes:
- 5:00 AM: turn on three devices, set 14 lights to 2500 K, then `fadeLevel(1, 50, 45 minutes)`
- 6:00 AM: turn on one additional device
- 8:00 AM: turn on one device, set another light to 2500 K and 100%

The 45-minute fade is not a WebCoRE `WAIT`. On the observed WebCoRE HE runtime, `fadeLevel` was implemented through repeated scheduled wakeups and incremental `setLevel()` commands.

## 2026-10-05 incident reconstruction

Runtime observed:
- WebCoRE HE `v0.3.114.20240115_HE`

Retained evidence:
- approximately 5:27:42–5:27:48 AM CDT: level-31 pass
- approximately 5:28:36–5:28:43 AM: level-32 pass
- 5:28:43.506 AM: final recorded School Mornings lighting command, `Twins.setLevel(32)`
- 5:28:57.548 AM: recorded pause event
- WebCoRE then reported the piston inactive/paused and stopped
- the next expected fade pass around 5:29:32–5:29:38 AM would have advanced toward level 33
- no level-33 pass and no later School Mornings lighting command was found
- no other inspected overlapping WebCoRE piston showed activity taking over those lights in the immediate post-pause window

### Corrected conclusion

The earlier statement that “pausing School Mornings did not stop already queued fade work” is **superseded**.

The retained WebCoRE evidence shows that Pause stopped the active School Mornings fade progression. The observed post-pause visual behavior is best explained by the lights remaining at the just-commanded level 32. A short device-native ramp is possible but was not proven.

Do not use this incident as evidence that WebCoRE Pause fails to stop `fadeLevel`.

## Pause / resume behavior

The live WebCoRE language surface exposes targeted:
- `pausePiston`
- `resumePiston`

Observed behavior supports:
1. Pause stopped the active School Mornings fade progression.
2. Pausing left School Mornings with no pending schedules.
3. Resume rebuilt legitimate future School Mornings schedules.
4. Resume at approximately 5:28 AM did not replay the already-passed 5:00 AM run; it rebuilt future schedules including 6:00 AM and 8:00 AM.

Therefore the leading School Mornings abort primitive is:

`Pause School Mornings -> Resume School Mornings`

This is a design decision, not yet a commissioned user-facing abort control.

## cancelTasks findings

The live language database exposes `cancelTasks` as “Cancel all pending tasks.”

Durable findings:
- it accepts no piston/device/task/statement parameter
- it is strongly indicated to operate on pending scheduled work belonging to the piston executing it
- it could plausibly cancel scheduled `fadeLevel` repeat work
- its broad “all pending tasks/timers” scope creates unnecessary risk for School Mornings' legitimate 6:00 AM and 8:00 AM schedules
- no exposed arbitrary task/statement cancellation API was found for selectively targeting only the fade repeat work
- another control piston cannot directly call `cancelTasks(School Mornings)` because no target-piston parameter exists

Decision: **do not use `cancelTasks` as the first-choice School Mornings abort primitive.**

## Current design direction

Create a dependable user-facing control that performs ordered:

`PAUSE School Mornings -> RESUME School Mornings`

Requirements:
- current School Mornings run/fade stops
- School Mornings ends active
- already-passed schedule does not replay
- future schedules are rebuilt
- control returns to a sensible idle state
- usable from Hubitat and eventually SharpTools
- ordering and failure behavior are defined before implementation

A momentary control plus a small controller are candidates. Keep the first implementation proportional and School-Mornings-focused, while avoiding a design that is unnecessarily difficult to extend later.

## Related delayed/scheduled behavior

Other current pistons with relevant behavior:
- Fade contains an actual `wait(10)`
- DoorLights uses delayed/scheduled work
- Scheduled Actions owns many unrelated schedules, making indiscriminate cancellation high-blast-radius
- Bedtime has scheduled/time-driven behavior

This is why a whole-house “cancel all tasks” mechanism should not be assumed safe.

## Verification status

Proven:
- Pause stopped the investigated School Mornings fade progression.
- No School Mornings lighting command was retained after the pause.
- Resume rebuilt future School Mornings schedules in the investigated event.
- The live language surface supports targeted pause/resume commands.

Not yet proven/commissioned:
- final user-facing abort device/interface
- exact ordering mechanism for programmatic pause then resume
- failure recovery if pause succeeds but resume fails
- behavioral acceptance of a completed abort control
- generalized abort behavior for other pistons
