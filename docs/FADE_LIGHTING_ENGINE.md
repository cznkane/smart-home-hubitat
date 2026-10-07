# Fade Lighting Engine

**Status:** Canonical durable design and troubleshooting record  
**Scope:** WebCoRE Fade piston, Govee/Hubitat zone behavior, curated hue palette, and known reporting limitations  
**Last reconciled:** 2026-10-07

## Ownership and architecture

Fade is a focused lighting-look/service piston. Callers decide when Fade runs; Fade decides what lighting look to apply. Guest, school, occupancy, elapsed-time, and scheduling policy remain outside Fade.

Flow: policy piston -> `VB-Fade` -> Fade -> location groups / standalone lights.

Hubitat Groups and Scenes devices use the `G-*` naming convention. Fade redesign targets observed here include `G-Deck`, `G-DiningKitchen`, `G-LivingRoom`, `G-Master`, `G-Playroom`, `G-Twins`, and standalone `Sadie`.

The grouped architecture remains valid for command delivery based on physical/app observations. Command propagation and Hubitat member-state synchronization are separate concerns.

## Hue scale

Controlled tests established that WebCoRE Set Hue accepts 0-360 degree hue-wheel values and converts them to Hubitat's 0-100 hue scale before issuing the device command.

Observed: 75->21, 80->22, 180->50, and 240 degrees -> about Hubitat 67.

This supersedes the earlier theory that Govee itself was unexpectedly translating values.

## Curated palette

Unrestricted random hue produced undesirable yellow/chartreuse colors and too many visually adjacent choices. Fade moved to a curated palette.

Working WebCoRE representation:

```text
fadeColors = '0,20,110,150,190,220,250,280,310,335'
arrayItem(random(9), fadeColors)
```

Ten entries are indexed 0-9. Changing the stale `random(12)` bound from the earlier 13-color palette to `random(9)` fixed the observed 240/evaluation problem.

Implementation lessons:
- `arrayItem()` is not broken.
- A typed integer-array variable did not work for this access pattern.
- `fadeColors[index]` was not accepted for the needed WebCoRE expression.
- The working variable is String (text), initial-value type Value, containing comma-separated degree values.
- One central palette avoids duplicating literals across zone blocks.

## Zone independence

Different locations can choose different colors while sharing the central palette. Each independently evaluated zone hue block uses its own `arrayItem(random(9), fadeColors)`.

Do not add collision-avoidance complexity unless normal field use demonstrates a real need.

## Field observations

- Hubitat hue 67, about 240 degrees, was a strong keeper.
- 20 degrees / Hubitat hue about 6 looked excellent on Deck but poor indoors.
- Around 89 degrees was already getting undesirably yellow-green.

Possible future refinement: separate indoor and outdoor palettes. This was deliberately deferred while the current design is field-tested.

## Brightness and Hubitat/Govee state synchronization

During development, G-Master members appeared in Hubitat to remain at 100% after Fade.

Evidence:
- WebCoRE logged `G-Master.setLevel(20)`.
- The G-Master group device could report level 20.
- Individual Hubitat Govee member attributes could still report level 100.
- The Govee app reported the physical bulbs at the intended 20%.

Conclusion: command delivery succeeded; individual Hubitat member attributes were stale. This is a Hubitat/Govee state synchronization/reporting concern, not evidence that Fade failed to deliver the level command.

A Kasa string member was removed during diagnosis and the Hubitat display symptom persisted. Kasa was not proven to be the root cause.

A 10-second hue-to-level wait did not correct stale member reporting and should not be retained merely to compensate for that symptom.

Operational rule: when Hubitat attributes disagree with physical/Govee-app behavior, compare WebCoRE command logs with physical/app state before redesigning automation. Stale attributes may also affect command optimization if an automation suppresses commands based on incorrect reported state.

## Rapid-fire testing

Repeated Fade invocations only a few seconds apart produced confusing behavior. Roughly 15 seconds between manual tests behaved more reliably. Production Fade normally runs once; do not infer a production defect solely from rapid-fire torture testing.

## SharpTools VB-Fade state

SharpTools has sometimes shown the Fade tile ON/spinning after Hubitat showed `VB-Fade` OFF and WebCoRE logged the `off()` command. Treat this as a separate dashboard/state-synchronization concern.

## Scene interaction

Fade moves scene-driven lights into the curated Fade color. During Door Lights temporary raise, some scene-driven strips can return to their prior scene instead of the intended CT 2700 / 100%; on timeout/restore they return to the Fade color correctly.

This may be acceptable in some scenarios, but scene-mode/state capture remains an unresolved design concern. Text/string-driven scene selection also remains future Fade redesign scope.

## Current-state boundary

Fade must preserve existing Evening behavior. Exact device membership and non-color levels must come from the newest archived/live piston.

Canonical retained archive reference at this reconciliation:
- Fade build 66
- import `vtyo`

That archive is newer than several experimental screenshots in this chronology. This document records durable architecture and lessons, not proof of the current live piston body.

## Superseded debugging theories

Do not revive these as canonical conclusions:
- `random()` is defective because early samples clustered
- Govee is the layer translating 80 to 22
- `arrayItem()` itself is broken
- every zone needs a duplicated literal palette
- long per-zone waits are required
- the Kasa member of G-Master was proven to break level propagation
- Hubitat individual-device 100% necessarily means the physical bulb ignored Fade
