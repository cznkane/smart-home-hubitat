# Door Lights V2

**Status:** Active field-test design record  
**Last reconciled:** 2026-10-07  
**Platform:** Hubitat + WebCoRE  
**Purpose:** Durable architecture, test evidence, and lessons for Door Lights automation.

## Why V2 exists

The original DoorLights piston accumulated per-device state capture, six restore flags, manual-interaction detection, a two-second watch window, and scheduled restore logic. Debugging showed that some individual Govee device attributes reported by Hubitat could be stale or misleading after Fade. That made otherwise-correct capture/restore behavior difficult to reason about.

The V2 direction is deliberately simpler: use the authoritative G-* lighting groups already used by Fade, remove manual-interaction suppression for now, and prove the basic capture -> temporary raise -> timed restore cycle before adding complexity.

The original DoorLights piston remains historical/reference context. Do not infer current V2 behavior from its old per-device restore flags.

## Source-of-truth and group decision

Fade and Door Lights should operate on the same G-* group abstraction where practical rather than capturing individual Govee members whose Hubitat attributes may be stale.

Relevant mapping/context established during redesign:
- G-DiningKitchen replaces direct Slider-style lighting control for the tested Door Lights path.
- G-Deck is intended to participate when available.
- L-Flood and Patio String Light remain direct switch devices rather than G-groups.

A key diagnostic observation was that post-Fade individual-device values looked wrong, while the G-DiningKitchen group correctly reported the expected Fade state. In the controlled validation state, G-DiningKitchen reported:
- colorMode: RGB
- hue: 0
- saturation: 100
- level: 20
- switch: on
- colorTemperature: 2500, but inactive/stale while RGB was the active mode

This supports using the G-group as the capture/restore boundary.

## V2 architecture

Current simplified design uses one datetime variable:
- `lockout`

Top restriction:
- Location mode is Evening or Night.

Door-open entry condition:
- any of D-Front, D-Garage, or D-Slider contact changes to open
- AND `$now` is after `lockout`

On a valid door-open event:
1. Set `lockout = addMinutes($now, 2)` for the current field-test duration.
2. Capture G-group state to WebCoRE local state.
3. Temporarily set participating G-groups to 2500 K.
4. Set group level to 100% in Evening; 25% in Night.
5. Capture L-Flood and Patio String Light switch state.
6. Turn L-Flood and Patio String Light on.

At `lockout`:
1. Restore the captured G-group attributes.
2. Restore L-Flood and Patio String Light switch state.

The tested G-group capture/restore attribute set is:
- hue
- level
- saturation
- switch

The piston intentionally does not restore generic `color` or `colorMode` in V2. The working RGB restore was emitted by WebCoRE as a concrete `setColor([hue, saturation, level])` command.

## Deliberately removed from V2

The following V1 machinery was intentionally removed to make the core behavior reliable and understandable:
- `doorActive`
- `watchStart`
- `watchChanges`
- per-device `restoreConsole`, `restoreSlider`, `restoreUpperDeck`, `restoreKitchen`, `restoreFlood`, and `restorePatio` flags
- all manual-interaction detection blocks
- the two-second manual-change arming window
- individual Console / Slider / UpperDeck / Kitchen restore paths

This is a product decision, not accidental loss of functionality. V2 currently restores the captured state unconditionally when the timeout expires. Manual user changes made during the active Door Lights window can therefore be overwritten by the timed restore. Reintroduce manual-interaction protection only after the simplified V2 has proven stable and only if the behavior is still desired.

`doorActive` became redundant once manual-interaction/watch logic was removed because the scheduled `lockout` event itself defines the active session.

## Timer behavior

A second door opening during the active two-minute window must not restart or extend the timer. The `$now is after lockout` gate prevents a new session while the existing lockout is in the future.

The two-minute duration is a debugging/field-test value, not necessarily the final production duration.

## Controlled validation evidence

A clean test established the following sequence for G-DiningKitchen:

Pre-door Fade baseline:
- RGB
- hue 0
- saturation 100
- level 20
- switch on

Door-open execution:
- WebCoRE saved G-DiningKitchen local state before changing it.
- WebCoRE issued `setColorTemperature(2500)`.
- WebCoRE issued `setLevel(100)`.
- The restore event was scheduled for two minutes later.

Expiration:
- WebCoRE issued `setColor([hue:0, saturation:100, level:20])`.
- WebCoRE loaded the saved switch state for L-Flood and Patio String Light.
- L-Flood restoration completed shortly afterward as a deferred device command.

The user initially believed restoration had failed because it was not visually immediate, then observed that it did restore correctly. This is important: WebCoRE/device restore work may complete asynchronously over a short interval after the lockout event. Do not declare restore failure immediately at the timestamp boundary without checking the log and allowing pending device commands to settle.

## Lessons from V1 debugging

### Capture ordering was not the original defect

Earlier logging proved that `saveStateLocally` executed before DoorLights issued temporary CT/level commands. The capture ordering was therefore correct.

### Individual-device telemetry could be misleading

After Fade, individual device attributes could show levels/hues inconsistent with the actual intended Govee state. The Govee app and G-* group state could show the intended dim level while individual Hubitat device state remained stale or inconsistent.

Therefore:
- do not use stale individual-member telemetry as proof that Fade or restore failed
- prefer the G-group state when the automation is designed around that group
- compare pre-event and post-event state at the same abstraction layer

### Generic color restoration was noisy

V1 logs included attempts to restore generic `color` / `colorMode` values, including empty color values and unsupported colorMode restoration warnings. V2 avoids that path and captures/restores concrete hue, saturation, level, and switch attributes.

### Medium logging was sufficient for ordering

Medium logging was enough to prove capture-before-command ordering and scheduled restore behavior. Full logging was excessively noisy and should not be the default merely to inspect this flow.

## Clean test procedure

For a controlled Fade -> Door Lights validation:
1. Keep DoorLights2 paused while establishing the lighting baseline.
2. Drive the normal Home -> Dusk -> Evening sequence so Fade runs.
3. Let Fade complete.
4. Record the participating G-group Current States before opening a door.
5. Resume DoorLights2 and clear its log.
6. Open one door.
7. Touch nothing during the active window.
8. Allow the two-minute cycle and any immediately deferred restore commands to complete.
9. Compare post-restore group state with the recorded pre-door group state.

There are no boolean working variables to reset in V2. Do not reset the `lockout` datetime as part of the test ritual.

## Current field-test status

The simplified V2 completed one controlled G-DiningKitchen round trip successfully:
- captured RGB H0/S100/L20
- raised to temporary 2500 K / 100%
- restored to RGB H0/S100/L20

The decision after that successful test was to freeze the design and run it for several nights before adding features.

Remaining validation:
- multi-night real-world reliability
- repeated-door behavior during an active lockout, confirming the original timer is not extended
- G-Deck behavior once it is available for testing
- final production timeout decision
- decide whether manual-interaction protection is worth reintroducing
- update the canonical piston archive once V2 is accepted as the authoritative Door Lights piston

## Historical V1 reference

The previously archived DoorLights reference was build 10, import code `0xia`. It represents the older manual-interaction architecture and should remain historical until the V2 archive is formally promoted.

The V2 duplicate retained the same visible import code during editing and reached build 8 in the captured redesign screenshot. Treat screenshot/build metadata as historical evidence only; inspect live WebCoRE before consequential work.


## Git issue tracking

- #16 — primary DoorLights V2 field validation, including multi-night reliability, repeated-door lockout behavior, G-Deck validation, final production timeout, manual-interaction policy, and archive promotion.
- #11 — native Govee scene behavior while Fade is active; remains separate from ordinary V2 restoration until the scene-capable G-Deck/UpperDeck path is tested under V2.
- #6 — underlying stale Govee individual-member telemetry. V2's group-based source-of-truth decision contains this risk for Door Lights but does not resolve the integration/reporting defect.
