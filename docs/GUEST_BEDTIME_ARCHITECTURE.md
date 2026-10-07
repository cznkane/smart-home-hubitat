# Guest / Bedtime Architecture

**Status:** Canonical architecture record; design partially unresolved  
**Scope:** WebCoRE guest-aware Evening/Fade/Night/Bedtime behavior  
**Canonical repository:** `cznkane/smart-home-hubitat`  
**Last reconciled:** 2026-10-07

## Purpose

Guest/Bedtime behavior is a cross-piston architecture problem, not a small Modes patch. This record preserves the durable decisions, boundaries, known behavior, and unresolved design questions so future work does not collapse distinct late-night scenarios into one path.

This document is architecture/history, not proof of live state. Before a consequential change, inspect live WebCoRE plus the newest archived piston records for Modes, Bedtime, Fade, Scheduled Actions, All Lights Off, and any other affected dependencies.

## Ownership and separation of concerns

- **Modes** owns mode-selection policy.
- **Fade** owns the lighting fade/service behavior; it should not become the owner of guest scheduling policy.
- **Scheduled Actions** owns time/environment scheduling policy where applicable.
- **VB-Bedtime / Bedtime** owns bedtime service behavior, including the established late-arrival service path.
- **All Lights Off** remains the canonical whole-house off service rather than duplicating off logic.
- `@GuestsPresent` is guest state and must not be conflated with normal family occupancy.
- Guest/bedtime policy must be coordinated across these owners rather than duplicated independently in each piston.

## Relevant retained state

Observed project variables/globals relevant to this architecture include:
- `@GuestsPresent`
- `@KidsPresent`
- `@School`
- `@LastEvening`
- `@LastGoodnight`
- `@LastFade`

The current retained Modes architecture suppresses the normal 11:30 PM Night transition while guests are present. The archived Modes build 57 also requires `GuestsPresent = false` for Dusk -> Evening.

Archived piston identities at the 2026-10-07 reconciliation:
- Modes: build 57, import `xtp9`
- Bedtime: build 16, import `s6cx`
- Fade: build 66, import `vtyo`
- Scheduled Actions: build 46, import `r6em`
- All Lights Off: build 36, import `wbwwo`

These are archive references only. Live WebCoRE is runtime truth.

## Core architectural distinction

Two late-night situations must remain separate.

### 1. Late guest departure

A guest departure after the normal bedtime boundary is a **delayed bedtime transition**.

The intended working model is:

```text
Guests present at normal transition
    -> hold/suppress normal Evening/Fade/Night progression as policy requires
Guests clear
    -> immediately reevaluate late-evening/bedtime policy
    -> provide an appropriate landing/Fade period when still reasonable
    -> Night
    -> canonical All Lights Off
```

Historical design discussion targeted roughly **30 minutes** of Evening/Fade landing time before Night + All Off when guests leave after bedtime. That duration is a design target from the working architecture, not a verified live implementation.

The guest-clear event should cause reevaluation rather than waiting for an unrelated later clock event.

### 2. Arrival while already Night

A late arrival is a **temporary exception inside Night**, not a delayed mode transition.

The retained design is:

```text
Mode = Night
    -> arrival occurs in the late-night window
    -> keep Mode = Night
    -> invoke VB-Bedtime late-arrival behavior
    -> provide temporary entry lighting
    -> timed cleanup/failsafe
```

Do not change Night back to Home or Evening merely to support entry lighting.

The project has used approximately 11:30 PM to 4:50 AM as the late-arrival Night window. Treat exact current times as live/archive state to verify before editing.

Historical late-arrival lighting discussion included L-Kitchen and Patio String, with broader outdoor/pool-light cleanup/failsafe work still needing verification against current Bedtime state. Do not treat that device list as certified current behavior without inspecting the live piston.

## Guest suppression behavior

Durable policy direction:
- Guests suppress the normal transition that would prematurely put the house into bedtime behavior while people are still present.
- The retained Modes design suppresses the 11:30 PM Night transition when guests are present.
- The retained Modes design also gates Dusk -> Evening on guests not being present.
- When guest state clears, the system should reevaluate immediately and choose the appropriate late-evening/bedtime path.

This avoids two bad outcomes:
1. dimming/shutting down the house around active guests;
2. leaving the house stranded indefinitely in a pre-Night state after guests depart.

## Inputs that matter on guest-clear reevaluation

The late guest-departure decision should consider, at minimum:
- `@GuestsPresent`
- `@KidsPresent`
- `@School`
- current mode/time
- whether normal Evening/Fade timing has already passed
- relevant last-run markers such as `@LastEvening`, `@LastFade`, and/or `@LastGoodnight` where the live design actually uses them
- a latest cutoff beyond which starting a full Fade sequence is no longer sensible

Do not invent new globals merely to implement this list. Inspect the current pistons and reuse observed state where appropriate.

## Unresolved architecture

The following remain intentionally unresolved until current live/archive logic is inspected and a bounded design is approved:

1. **Very-late guest departure cutoff.** At some point a full ~30-minute Fade is unreasonable. The cutoff and abbreviated/direct Night behavior are TBD.
2. **Exact landing sequence.** The intended shape is late Evening/Fade -> ~30 minutes -> Night -> All Off, but ownership, timing primitive, and exact transition mechanics require current-state review.
3. **Interaction with normal/manual VB-Bedtime.** Late-arrival behavior must coexist with existing bedtime behavior without turning VB-Bedtime into the owner of all guest policy.
4. **Outdoor/pool-light late-arrival cleanup.** Historical discussion included temporary outdoor lighting and a failsafe-off requirement; current implementation status must be verified.
5. **Sadie Noise interaction.** Guest-delayed Fade should be tested to ensure it does not produce an unintended Sadie Noise outcome. Do not reopen already-separated scheduling work unless live evidence shows a defect.

## Sadie Noise historical context

Earlier Fade behavior used school/non-school overnight timing for Sadie Noise, historically described as:
- School: until 5:30 AM
- Non-school: until 8:30 AM

Later project architecture moved scheduling responsibility into Scheduled Actions. Therefore Sadie Noise is relevant here primarily as an **interaction/test case**, not as a reason to put long overnight waits back into Fade.

Verify current Scheduled Actions/Fade state before relying on the historical times.

## Design lessons

- Guest presence is not occupancy. Keep the concepts separate.
- A late guest departure and a late arrival can happen after the same clock boundary but are different state-machine events.
- Preserve Night during late arrival; use a service path for temporary lighting.
- Guest-clear should be an event that triggers policy reevaluation.
- Do not solve cross-piston architecture by adding one convenient condition to Modes.
- Do not add scheduling triggers to service/action pistons merely because they are nearby.
- Avoid long queued waits when a schedulable state transition can be owned explicitly.
- Reuse canonical service pistons such as All Lights Off rather than duplicating whole-house actions.

## Verification requirements before implementation is declared complete

A future implementation should test at least:
- guests present through normal Evening time
- guests present through 11:30 PM
- guests leave shortly after the normal bedtime boundary
- guests leave very late, beyond the chosen cutoff
- guest state clears and reevaluation occurs without waiting for another clock trigger
- arrival while Mode is already Night
- late-arrival temporary lights clean up correctly
- normal/manual Bedtime behavior still works
- Fade is not duplicated or invoked twice
- Night eventually reaches canonical All Lights Off
- Sadie Noise behavior remains correct on school and non-school nights
- persistence/read-back and real behavioral verification are both completed

## Historical provenance

This record was created from the dedicated **Guest / Bedtime** Smart Home chat and reconciled against the canonical retained context on 2026-10-07. Statements that were discussion targets rather than proven live behavior are deliberately labeled as historical, intended, or unresolved rather than promoted to current-state fact.
