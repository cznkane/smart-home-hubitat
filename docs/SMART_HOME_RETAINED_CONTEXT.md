# Smart Home Retained Context

**Status:** Canonical retained project context  
**Scope:** Durable Smart Home knowledge that new technical chats need in addition to operating rules and deployment procedure  
**Canonical repository:** `cznkane/smart-home-hubitat`  
**Last reconciled:** 2026-10-07

## Purpose

This document captures durable project knowledge, decisions, current architecture, known state, and important historical lessons so Smart Home chats do not depend on conversational memory.

It is not a substitute for live evidence. Live WebCoRE/Hubitat/runtime state wins when it conflicts with this record. Git is the durable engineering record; live systems are runtime truth.

Do not store secrets here.

## Smart Home stack

- Hubitat is the device/platform layer.
- WebCoRE is the automation engine and source of truth for effective automation logic.
- SharpTools is the presentation/dashboard layer.
- UniFi provides network infrastructure.
- WeatherFlow provides outdoor illuminance/lux used by automation logic.
- ChatGPT Business can reach WebCoRE and selected Hubitat devices through the private MCP/tunnel architecture.
- GitHub is the engineering system of record.

## ChatGPT / MCP architecture

Target and now-proven read architecture:

```text
ChatGPT Business
  -> private WebCoRE MCP plugin
  -> OpenAI secure MCP tunnel
  -> bridge Mac
  -> webcore-CLI MCP
  -> WebCoRE and bounded Hubitat Maker API
```

Direct Hubitat Maker API inventory, WebCoRE-authorized device inventory, and ChatGPT-visible MCP tool inventory are distinct concepts and must never be conflated.

As of webcore-CLI 0.4.9 acceptance:
- direct Maker API path returned 5 explicitly authorized devices
- WebCoRE inventory was 95 authorized devices
- MCP advertised 18 tools
- the two direct Hubitat tools are `hubitat_list_devices` and `hubitat_get_device`
- Business Admin could show the correct 18-tool inventory while an older Business chat still lacked a newly added tool
- fresh Business chat acceptance is therefore a separate deployment gate

Production webcore-CLI payload root:
`~/Library/Application Support/WebCoRE-MCP/webcore-cli`

Current retained production payload classification after 0.4.9 acceptance:
- 0.4.9 ACTIVE
- 0.4.8 ROLLBACK
- 0.4.7 RETIRED

The tunnel remains foreground-managed pending separate reboot/recovery commissioning. Interim terminal-role operations are canonicalized in `docs/WEBCORE_MCP_FOREGROUND_RUNTIME_OPERATIONS.md`; managed recovery is tracked in #23.


### Workspace availability boundary

Tracked follow-up: #24.

The proven 0.4.9 end-to-end acceptance is for 🔵 ChatGPT Business. The desired architecture is for both 🔵 Business and 🟢 Personal Smart Home chats to reach the same bounded WebCoRE + Hubitat MCP capability without maintaining divergent local implementations.

As of the retained evidence from the 2026-10-07 integration work:
- Business access is proven through the private plugin/tunnel path.
- Personal Smart Home chat exposure is a separate workspace/product availability gate and was not proven in the earlier investigation.
- Do not infer Personal availability from Business Admin discovery or Business fresh-chat acceptance.
- Prefer one canonical local MCP implementation/tool family for both workspaces if the product surface permits it; avoid parallel forks merely to work around workspace exposure.


## WebCoRE / Hubitat change philosophy

- Prefer read-only inspection.
- Writes require explicit approval unless a bounded change was already explicitly authorized.
- Live device-affecting tests are separately sensitive.
- Prepare/diff is not a write.
- Persistence verification is not behavioral verification.
- Diagnose upstream defects upstream instead of adding compensating logic to every consumer.
- Do not casually put triggers in action/service pistons when scheduling belongs in Scheduled Actions.
- Modes owns mode-selection logic.
- WebCoRE is the source of truth for effective presence.
- Guest/bedtime behavior is an architecture area, not a tiny isolated Modes patch.
- Always consult the newest archived/current piston record before analyzing or changing piston logic.
- Do not invent global variable names.

## Mode Engine current design

Target modes:
- Vacation
- Away
- Night
- Evening
- Dusk
- Home

Known current-state concepts:
- Dusk is driven by WeatherFlow illuminance with a sustained-low-lux requirement.
- The archived Modes build updated 2026-10-04 uses WeatherFlow illuminance below 15,000 lux for 5 minutes between 5:30 PM and 11:30 PM to record dusk.
- Evening timing depends on KidsPresent/School and is capped according to the current Modes logic.
- Dusk -> Evening requires GuestsPresent false and very low WeatherFlow lux in the archived build.
- 11:30 PM Night transition is suppressed when guests are present.
- Night ends around the early-morning reset window; late-night arrival behavior is handled separately through Bedtime logic while preserving Night mode.
- Noon/reset logic clears dusk tracking.
- Dusk recovery/hysteresis remains an architectural concern when lux rises after dusk is recorded but before Evening.
- Historical diagnostic evidence during Occupancy testing showed an older Modes snapshot with `duskStarted = 3:00:12 PM`, `eveningDue = 6:30:12 PM`, and `duskRecorded = true`, while Evening was observed to transition around 7:22 PM. This suggests the calculated due time can pass without an execution waking the Evening transition, with a later unrelated reevaluation applying the overdue transition. Treat this as an unresolved Modes/Scheduled Actions wakeup/scheduling issue, not an Occupancy responsibility. That screenshot was an older Modes build and does not supersede archived Modes build 57. This concern is tracked in Git issue #29; that issue also carries dusk-recovery/hysteresis as a related follow-up without assuming the two concerns share one root cause.

Relevant globals/variables observed in the project include:
- `@Occupied`
- `@KidsPresent`
- `@School`
- `@GuestsPresent`
- `@LastEvening`
- `@LastGoodnight`
- `@LastFade`
- `duskRecorded`
- `duskStarted`
- `eveningDue`

Use observed live/archive names rather than extrapolating additional globals.

## Presence / occupancy / guests / kids

- WebCoRE is the source of truth for effective presence and occupancy policy. Raw Hubitat/SharpTools device display can disagree with WebCoRE-derived truth; correct the upstream WebCoRE model rather than making dashboards authoritative.
- Family presence inputs are the Geofency-backed `P-Rick`, `P-Andie`, `P-Everly`, and `P-Sadie` devices. UniFi family-presence references were deliberately removed from Occupancy because they created conflicting presence authorities.
- `@GuestsPresent` is the canonical global guest-presence signal. It participates directly in occupancy, and changes to the global trigger Occupancy reevaluation.
- `KidsAway` is a manual override for forgotten/incorrect kid-phone presence. When `KidsAway` is on, each kid's effective presence is false even if the corresponding raw Geofency device says present.
- Current Occupancy derivation: `@RickEffective` follows `P-Rick`; each kid-effective boolean is true only when that kid's P-* device is present and `KidsAway` is off. As of verified build 49, the aggregate has its own fail-safe gate: `@KidsPresent = KidsAway OFF AND (andieEffective OR everlyEffective OR sadieEffective)`. `@Occupied` is true when `@RickEffective`, `@KidsPresent`, or `@GuestsPresent` is true.
- Occupancy reevaluates on any family P-* presence change, `@GuestsPresent` change, or `KidsAway` switch change.
- A naive KidsAway auto-reset based only on “any two kid devices are present” was behaviorally rejected: phones already left at home satisfied the condition and immediately defeated the manual override.
- The proven auto-reset is event-based. While `KidsAway` is on, turn it off only when a kid **changes to present** while at least one different kid is already present: Andie arrival + Everly/Sadie present; Everly arrival + Andie/Sadie present; Sadie arrival + Andie/Everly present. This was verified with Geofency test hooks. A device already present must transition away/not-present before another present hook can exercise `changes to present`.
- The old school-departure suppression machinery (`SchoolDepartureSeen`, school-hours gating, and garage-departure timestamp/logic) was removed from Occupancy. The manual KidsAway override replaces its forgotten-phone purpose with simpler explicit policy.
- Historical naming warning: do not infer current guest/KidsAway semantics from legacy `P-Guest` naming; use observed live/global names.
- Git issue ownership is deliberately split: closed #2 records the resolved `KidsAway ON => @KidsPresent false` safety invariant and verified build-49 hard gate; closed #3 records the intentional event-based KidsAway auto-clear design. Do not reopen either merely because the historical chat first observed KidsAway clearing unexpectedly.

### Occupancy piston current known state

The “occupied piston” cleanup superseded the older retained Occupancy archive reference.

Latest screenshot-observed working state from that workstream:
- piston: Occupancy
- import code: `7dxps`
- build 48 was observed after the KidsAway arrival-reset implementation; build 49 was subsequently saved/read back after adding the aggregate KidsAway hard gate
- local booleans: `andieEffective`, `everlyEffective`, `sadieEffective`
- no remaining school-hours or `SchoolDepartureSeen` logic in the cleaned body
- no UniFi family-presence inputs in the cleaned body

The earlier `Occupancy build 24 / import 3q1s` record is superseded as a current reference. Build 49 is the latest verified saved definition from this workstream; its stored definition exactly matched the approved hard-gate update, Occupancy remained active, and no other piston was changed. Inspect live WebCoRE or the newest archive before future consequential changes.

## Lighting architecture

### All Lights On

All Lights On is a service/action piston. Environmental/time scheduling policy should generally live in Scheduled Actions and invoke All On rather than turning All On itself into a trigger-heavy policy piston.

Durable design established during the 2026-10-01 cleanup:
- `VB-AllLightsOn switch changes to on` is the service piston's outer invocation gate.
- Illuminance is a decision inside that invocation, not an independent trigger.
- The lux decision selects between a brighter/day-oriented device set and a darker/exterior-inclusive device set.
- Both branches converge before a single `VB-AllLightsOn -> off` reset, avoiding duplicate reset logic and preventing the reset event from becoming lighting policy.
- The darker branch includes exterior loads such as Deck, porch/walkway, FlagLight, Patio String Light, and Pool Light; the brighter branch is primarily interior.
- Main interior groups are driven to 2500 K / 100%, can lights to 20%, and the associated switched lamps are turned on in the observed build-39 design.
- Build 39 was the cleaned-up implementation observed in this chat. The canonical archive subsequently records build 40, so build 39 is historical design evidence and does **not** supersede the newer archive.

Archived reference as of this retained-context reconciliation:
- All Lights On
- build 40
- import code `gjiyv`

### Scheduled Actions

Scheduled Actions owns time/environment policy that invokes service/action pistons. The low-lux All On policy belongs here under the established separation of concerns.

The low-lux daytime policy was implemented in Scheduled Actions and observed in build 46 as:
- WeatherFlow illuminance is less than 10,000 lux and stays below 10,000 lux for 30 minutes
- AND time is between 9:30 AM and 4:30 PM
- AND Hubitat location mode is Home
- THEN turn on `VB-AllLightsOn`

This deliberately keeps environmental/time policy out of the All Lights On service piston. The sustained-lux timer belongs syntactically to the lux condition, not to the 9:30 AM window. The intended behavior is that if lux has already been continuously below threshold for at least 30 minutes when the time window becomes valid, 9:30 AM is the earliest eligible activation. However, this chat did not capture a live execution proving WebCoRE's compound-condition scheduling semantics at the 9:30 boundary. Treat 9:30 versus 10:00 earliest activation as a field-validation item, not as established runtime truth.

The 10,000-lux threshold for this gloomy-day policy is distinct from dusk/mode lux thresholds. Do not infer that all lux-based automations share one threshold; use the archived/live piston for the specific policy being changed.

Archived reference:
- build 46
- import code `r6em`
- modified 2026-10-02 in the archived project record

Other durable Scheduled Actions responsibilities visible in the build-46 archive from this chat:
- Pool Chlorinator: on daily at 7:30 PM and off daily at 4:00 AM.
- BugLamp: on when location mode changes to Night; a separate sustained-on rule turns it off after it has remained on for 3 hours.
- After location mode has remained Night for 60 minutes: pause Sadie Sonos and Twins Sonos, and turn Pool Light off.
- Holiday lighting when `@Holidays` is true: Christmas Lights off at midnight, on at 5:00 AM, off at sunrise, and on one hour before sunset.
- Sadie Noise: on when location mode changes to Evening while `@KidsPresent` is true; off at 5:30 AM on school days and 8:30 AM on non-school days.
- Jackery: off daily at 1:00 AM and on daily at 11:00 AM.

These are retained ownership/current-archive facts, not proof that each scheduled behavior has been field-validated. Inspect live WebCoRE before consequential changes.

### Fade

Fade remains a focused lighting-look/service piston. Timing, guest, school, occupancy, and scheduling policy remain outside it.

Canonical detailed design/troubleshooting record:
- `docs/FADE_LIGHTING_ENGINE.md`

Key retained findings:
- central curated comma-delimited palette; current field-test set: `0,20,110,150,190,220,250,280,310,335`
- ten entries use `arrayItem(random(9), fadeColors)`; correcting the stale 13-color bound fixed the observed evaluation problem
- WebCoRE Set Hue uses 0-360 degree input and converts to Hubitat's 0-100 hue scale
- independent zone blocks provide independent color picks while sharing one palette
- 20 degrees / Hubitat hue about 6 is a Deck keeper but poor indoors; possible indoor/outdoor palette separation is deferred pending field experience
- G-Master physical bulbs reached the commanded 20% even when individual Hubitat Govee member attributes remained at 100%; treat this as state synchronization/reporting, not failed Fade command delivery
- Kasa was not proven to cause the G-Master symptom
- long waits are not justified merely to compensate for stale Hubitat member state
- SharpTools can independently show stale `VB-Fade` state
- scene/text-driven selection remains future redesign scope
- Fade must preserve Evening behavior

Archived Fade reference:
- build 66
- import code `vtyo`

The archived build is newer than several experimental screenshots from the redesign chronology. Inspect the newest archive/live piston before consequential changes.

### Door Lights

Door Lights V2 is a deliberately simplified, group-based design. Full durable architecture, validation evidence, history, and remaining acceptance work are maintained in [DOOR_LIGHTS_V2.md](DOOR_LIGHTS_V2.md).

Current retained direction:
- use G-* lighting groups as the capture/restore boundary where practical rather than stale-prone individual Govee member telemetry
- tested path is G-DiningKitchen; G-Deck is intended to participate when available; L-Flood and Patio String Light remain direct switch devices
- one `lockout` datetime defines the active session; a second door opening while lockout is in the future must not restart or extend the timer
- the two-minute lockout is a field-test duration, not a final production-duration decision
- G-group capture/restore uses hue, saturation, level, and switch; V2 intentionally avoids generic `color` / `colorMode` restore
- V2 intentionally removed manual-interaction suppression, `doorActive`, `watchStart`, `watchChanges`, and per-device restore flags
- controlled validation proved G-DiningKitchen could capture RGB H0/S100/L20, raise to temporary 2500 K / 100%, and restore to RGB H0/S100/L20
- WebCoRE/device restore work may settle asynchronously just after the lockout event; check logs and pending device commands before declaring failure
- current decision is to freeze V2 and field-test it over multiple nights before adding features

The archived DoorLights build 10 / import `0xia` is historical V1 reference, not the simplified V2. A captured V2 editing screenshot reached build 8 while retaining the same visible import code; neither screenshot identity proves current live state. Promote the accepted V2 into the canonical piston archive only after field validation.

### Scene interaction

Detailed canonical subsystem record: `docs/GOVEE_LIGHTING_INTEGRATION.md`.

Govee scene behavior observed:
- Fade successfully moves scene-driven lights from their native Govee scene to the randomized Fade RGB palette.
- When Door Lights then attempts its temporary CT 2700 K / 100% raise, affected devices can reassert the prior native scene instead of showing the intended white.
- On timeout, Door Lights correctly restores the Fade RGB color that was active before the door-open override.
- This localizes the observed defect to the temporary Door Lights override rather than the final Fade-state restoration.
- The scene reappearance may be desirable in some scenarios; future design may intentionally support both functional-white and ambient-scene raise behavior.
- Native Govee scene/effect invocation from WebCoRE remains unresolved and must be based on the observed Hubitat driver command surface rather than invented command names.

Tracked in Git issues #8 and #11.

## Guest / Bedtime architecture

Guest/Bedtime is intentionally isolated as a cross-piston architecture problem. Detailed canonical architecture and verification requirements are maintained in `docs/GUEST_BEDTIME_ARCHITECTURE.md`; actionable completion work is tracked in Issue #14.

Durable boundaries:
- `@GuestsPresent` is guest state and must not be conflated with normal family presence semantics, even though current Occupancy includes guest presence in `@Occupied`.
- Current retained Modes policy gates normal Dusk -> Evening and the 11:30 PM Night transition when guests are present.
- Guest-clear should cause immediate policy reevaluation rather than waiting for another unrelated clock event.
- A **late guest departure** is a delayed bedtime transition. The working design target is an appropriate late Evening/Fade landing period, historically about 30 minutes when still reasonable, followed by Night and canonical All Lights Off. This duration is a design target, not verified live implementation.
- A **late arrival while already Night** is a temporary exception inside Night. Preserve Mode = Night and use the established VB-Bedtime late-arrival service path with temporary lighting and cleanup/failsafe.
- Do not conflate late guest departure with late arrival merely because both occur after the same clock boundary.
- The very-late guest-departure cutoff and abbreviated/direct-Night behavior remain unresolved.
- Sadie Noise is primarily an interaction/test case here. Historical scheduling moved toward Scheduled Actions; do not casually reintroduce long overnight waits into Fade.

Ownership remains separated: Modes owns mode selection; Fade owns fade/look behavior; Scheduled Actions owns applicable scheduling policy; Bedtime owns bedtime service behavior; All Lights Off remains the canonical whole-house off service.

Do not reduce this to a one-line Modes patch or duplicate policy across Modes, Fade, Bedtime, Scheduled Actions, and All Lights Off. Inspect current live/archive state before implementation.

## Automation control / maintenance hold architecture

A broader operational control requirement was approved after the School Mornings incident: provide a deliberate global automation maintenance/kill control plus selective function-level holds where justified.

Canonical design record: `docs/AUTOMATION_CONTROL_ARCHITECTURE.md`.

Important boundaries:
- this requirement remains valid even though later forensics proved that WebCoRE Pause **did** stop the investigated School Mornings `fadeLevel` progression;
- School Mornings-specific abort remains tracked in #13 and `docs/SCHOOL_MORNINGS_ABORT_ARCHITECTURE.md`;
- do not assume a generic whole-house `cancelTasks` operation is safe; pending work must be classified by owner/function and blast radius;
- global control must not blindly clear durable occupancy/presence/mode truth;
- future pending-intent designs should revalidate authorization/current conditions at execution time so stale work cannot fire merely because it was scheduled earlier;
- Hubitat/SharpTools should ultimately expose clear master/function control state;
- names such as `AutomationHold` and `SchoolMorningEnabled` are conceptual only until an implementation defines and verifies canonical names.

Implementation remains open and must define active-work abort semantics, pending-work handling, safe resume, persistence, observability, and failure recovery before commissioning.

## School Mornings cancellation / abort findings

The earlier interpretation that pausing School Mornings failed to stop already queued fade work is **superseded by forensic evidence**.

The 5:00 AM `fadeLevel(1, 50, 45 minutes)` is implemented through repeated scheduled wakeups and incremental `setLevel()` passes, not a WebCoRE `WAIT`.

For the 2026-10-05 incident on WebCoRE HE `v0.3.114.20240115_HE`:
- final recorded fade command: `Twins.setLevel(32)` at 5:28:43.506 AM CDT
- pause: 5:28:57.548 AM
- the expected next level-33 pass around 5:29:32–5:29:38 AM never occurred
- no later School Mornings lighting command was found
- no inspected overlapping WebCoRE piston took over those lights immediately after pause

Conclusion: **Pause stopped the investigated School Mornings fade progression.** The post-pause visual behavior is best explained by the lights remaining at the just-commanded level 32; a short device-native ramp is possible but unproven.

The live WebCoRE language surface exposes targeted `pausePiston` and `resumePiston`. Resume in the investigated event rebuilt future 6:00 AM and 8:00 AM schedules without replaying the already-passed 5:00 AM run.

`cancelTasks` is not the preferred primitive because it has no target piston/task/statement parameter and its broad pending-task scope creates unnecessary uncertainty around legitimate future schedules.

Leading design for a future user-facing School Mornings abort control:

`Pause School Mornings -> Resume School Mornings`

This is not yet commissioned. See `docs/SCHOOL_MORNINGS_ABORT_ARCHITECTURE.md` for the forensic record, design constraints, and acceptance requirements.

Archived School Mornings reference:
- build 29
- import code `3co00`

## Deferred observability / historical logging

Tracked follow-up: #25.

A robust local historical logging/observability path is intentionally deferred until the Hubitat/MCP integration is stable. The retained design direction is:
- collect Hubitat `/logsocket` and `/eventsocket` locally on an always-on Windows VM on the trusted LAN
- write structured rotating local logs, with JSONL/day rotation as the lightweight starting point
- use an explicit retention policy rather than unbounded growth
- consider Loki/Grafana later if richer querying/visualization is justified
- consider structured WebCoRE logging as a separate enhancement

This is a pinned future architecture item, not a commissioned service. Do not treat it as current production state.

## Status bridge / SharpTools

Direct ChatGPT/SharpTools integration is a separate post-Hubitat architecture evaluation tracked in #27. Existing dashboard/status-bridge completion remains tracked in #15.

A Hubitat/WebCoRE status bridge is used to expose automation state to SharpTools.

Known displayed/bridged concepts include:
- Occupied
- KidsPresent
- School
- GuestsPresent
- mode reason/status
- dusk/evening timing
- family/guest presence

Known command/status concepts include:
- `TIME_Evening`
- `TIME_Dusk`
- `PRES_*`

SharpTools design language:
- Material Design Icons / Pictogrammers preferred
- state/color communicates status
- icon communicates device/function
- dark translucent/glass-like tiles with defined bezels over rotating backgrounds
- combined presence tile replaces many individual presence tiles
- family members passive in corners, center Guest control actionable
- status bridge custom attributes support Attribute Tiles

## Govee / plug migration

Detailed canonical subsystem record: `docs/GOVEE_LIGHTING_INTEGRATION.md`. It is the authoritative retained record for Govee model identities, grouping/DreamView capability boundaries, music-sync requirements, UpperDeck discovery/IP behavior, and Govee scene interaction with Fade/Door Lights.

Project direction:
- avoid returning to flaky Kasa where practical
- H5080 was selected/tested as a candidate Govee plug
- H5083 Matter plugs were targeted for replacement/return
- avoid Govee V2 integration where it conflicts with native integration
- Govee integration/device IP discovery behavior has caused an UpperDeck IP to revert unexpectedly
- “Send discovery broadcast every hour” was turned off during investigation; this is a mitigation pending persistence verification, not proof that the wrong-subnet discovery root cause is solved.
- UpperDeck is Govee H6176; the primary indoor bulbs observed in this work are H6008, with H619D Kitchen separately observed as Desktop Music DreamView eligible.
- Windows Govee Desktop Scenic DreamView saw the approximately 15-device lighting set, including H6008 bulbs and UpperDeck H6176, while Music DreamView exposed only H619D Kitchen. Music DreamView eligibility is therefore a separate capability gate from basic LAN/device visibility.
- Whole-installation music sync requires all desired Govees, including UpperDeck and indoor bulbs, over non-Bluetooth transport. No production architecture satisfying that requirement has been selected.
- Related open work is tracked in Git issues #18 and #19.

Recommission targets have included:
- Big lamp
- the k
- salt lamp
- fireplace fan
- Jackery
- flag light
- Sadie star

## Network / Sonos

- UniFi network is part of the Smart Home platform.
- Sonos uses a dedicated SSID named Sonos.
- Sonos has experienced glitchy/cutting audio after layout/network changes and remains an area where topology/current UniFi state should be inspected rather than guessed.

## Canonical piston archive references

Newest retained archive identities known from project context at this reconciliation:

- Modes: build 57, import `xtp9`
- Occupancy: build 49 (saved/read-back verified after aggregate KidsAway hard gate); import `7dxps` is the latest retained import identity from the preceding build-48 cleanup and should not be assumed to identify build 49 without a newer archive
- Variables: build 15, import `rep9g`
- Bedtime: build 16, import `s6cx`
- DoorLights: build 10, import `0xia` (historical V1 reference; V2 not yet promoted to canonical archive)
- Fade: build 66, import `vtyo`
- Manual Chlorinator: build 8, import `p0cih`
- Mode Actions: build 37, import `n82s`
- Rick Presence: build 6, import `s7tk`
- Scheduled Actions: build 46, import `r6em`
- School Mornings: build 29, import `3co00`
- All Lights Off: build 36, import `wbwwo`
- All Lights On: build 40, import `gjiyv`
- Fridge: build 6, import `27ed9`
- Living Room: build 10, import `co995`
- Master Bedroom: archived build 45, import `r8x2`; later Git issue #4 records build 47 and therefore supersedes the screenshot archive for current logic

These identities are reference/archive context, not proof of the current live piston body. Inspect live WebCoRE before consequential diagnosis/change.

## MCP release/deployment lessons retained

Permanent lessons from 0.4.8/0.4.9 work:
- all version-bearing manifests must agree, including `.codex-plugin/plugin.json`
- complete tests must pass
- local branch state and GitHub canonical state are separate gates
- never mistake a Git pager for a shell prompt
- never issue a new shell command while the pager is still active
- normal red/green Git diff lines are not themselves errors
- source correctness does not prove installed payload correctness
- installed payload correctness does not prove running-runtime correctness
- running runtime does not prove MCP-advertised identity/tool inventory
- MCP inventory does not prove Business Admin discovery
- Business Admin discovery does not prove an existing chat exposes newly added tools
- fresh-chat acceptance is required for new ChatGPT-visible capabilities
- once a layer is exonerated, do not disturb it without new evidence
- finish with rollback classification, cleanup, and documentation
- Business read-tool approval anomaly is tracked in #26 and must not be "fixed" by weakening the workspace to Allow all tools

## Git issue tracking for retained work

As of the 2026-10-07 To Do migration, durable open work from that thread is tracked in Git rather than only in conversational TODO state:
- #6 Govee member-state synchronization after Hubitat group commands
- #7 SharpTools Fade tile stale-state behavior
- #8 Fade text/scene selection enhancement; curated build-66 palette itself is complete
- #11 Door Lights scene behavior while Fade is active
- #13 School Mornings user-facing abort control; later forensics disproved the earlier claim that Pause failed to stop the investigated fade progression
- #14 guest-aware Evening/Bedtime architecture
- #15 SharpTools status bridge and dashboard cleanup
- #16 DoorLights V2 ordinary field validation
- #17 smart-plug migration/recommissioning
- #18 Govee whole-device music synchronization
- #19 UpperDeck IP stability and UniFi reservation cleanup
- #20 outdoor UniFi AP deployment
- #21 publication of the verified canonical piston screenshot package to Git
- #23 managed reboot/recovery for the foreground WebCoRE MCP tunnel runtime
- #24 expose the canonical WebCoRE + Hubitat MCP capability to Personal ChatGPT without forking the runtime
- #25 local historical Hubitat/WebCoRE event/log observability archive
- #26 ChatGPT Business read-tool approval anomaly
- #27 evaluate direct SharpTools access only after Hubitat/WebCoRE MCP stabilization
- #28 certify the approval-gated WebCoRE persistent write path with rollback/read-back evidence

Closed issues #2 and #3 retain the later Occupancy/KidsAway correction and intentional auto-clear design. Closed issue #4 records a later Master Bedroom build than the screenshot archive. These later Git records supersede older archive-era identities where they conflict.

## Piston archive governance

Detailed To Do/archive governance, screenshot-era piston identities, supersession rules, completed-work anti-resurrection rules, and the local screenshot-package history are maintained in `docs/WEBCORE_PISTON_ARCHIVE_GOVERNANCE.md`.

Important rule: archived screenshots are reference baselines, not immutable live truth. Newer live/Git evidence wins. In particular, later Git records supersede the archived Occupancy build 48 and Master Bedroom build 45 identities.

## Initialization / knowledge policy

This retained context should be loaded during Smart Home technical initialization so a new chat begins with durable project knowledge rather than conversational memory.

However:
- loading this file does not certify live state
- task-specific current evidence must still be retrieved
- newer canonical documentation supersedes stale statements here
- when durable project knowledge changes, update this file as part of the documentation/cleanup gate
- avoid copying transient troubleshooting noise here unless it creates a durable lesson, decision, or known state

## Update discipline

When material Smart Home work changes durable knowledge, ask:
1. Did architecture change?
2. Did a source-of-truth boundary change?
3. Did a current retained version/build/rollback state change?
4. Did we discover a durable operational lesson?
5. Did a known issue become resolved or change shape?

If yes, update the appropriate canonical document and this retained-context file where it materially affects future initialization.


## ChatGPT ↔ WebCoRE integration provenance

The direct integration was motivated by eliminating screenshot/manual-relay troubleshooting. Durable design intent is for ChatGPT to inspect live piston definitions, variables, logs, and deliberately authorized device state directly; begin with read-only observability; keep Hubitat/WebCoRE private; and place live tests plus persistent writes behind explicit approval/change control.

The original proposal considered a bespoke LAN bridge and direct WebCoRE external-execution integration. That implementation concept is superseded by the commissioned `webcore-CLI` + OpenAI secure MCP tunnel architecture. Credential-bearing external execute URLs remain secrets, not a ChatGPT integration surface.

Current staged state:
- read-only WebCoRE inspection is commissioned
- bounded direct Hubitat Maker API reads are commissioned in webcore-CLI 0.4.9
- persistent WebCoRE write-path certification remains open in #28
- write certification must prove recoverable pre-change state, prepare/diff approval, remote-change protection, apply, stored read-back, rollback, and separate behavioral verification

See `docs/CHATGPT_WEBCORE_MCP_ARCHITECTURE.md` for the detailed architecture and design history.
