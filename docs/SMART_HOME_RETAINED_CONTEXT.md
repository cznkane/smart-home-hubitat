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

The tunnel remains foreground-managed pending separate reboot/recovery commissioning.

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

- WebCoRE effective presence is authoritative.
- UniFi references were removed from the Occupied piston for family effective-presence truth.
- Guest presence is derived from the guest Wi-Fi/captive-portal presence path and exposed through `@GuestsPresent`.
- Legacy P-Guest was repurposed to a kid-home override role; do not assume its historical meaning from its name.
- Kids Away override behavior has required work because effective child presence could repopulate unexpectedly.
- School Departure Seen logic was identified for removal.
- Guest state should cause occupancy/mode reevaluation where appropriate.

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

This deliberately keeps environmental/time policy out of the All Lights On service piston. The sustained-lux timer belongs to the lux condition, not to the 9:30 AM window. Therefore, if lux has already been continuously below threshold for at least 30 minutes when the time condition becomes valid, 9:30 AM is the intended earliest eligible activation; the design does not inherently impose an additional 30-minute delay after 9:30.

The 10,000-lux threshold for this gloomy-day policy is distinct from dusk/mode lux thresholds. Do not infer that all lux-based automations share one threshold; use the archived/live piston for the specific policy being changed.

Archived reference:
- build 46
- import code `r6em`
- modified 2026-10-02 in the archived project record

### Fade

Goals/design:
- curated bold-color palette rather than unrestricted random hue
- zone independence for G-Deck, G-DiningKitchen, G-LivingRoom, G-Master
- Fade should preserve Evening behavior
- scene/text-driven selection is part of the redesign scope
- Kasa/Govee group state reporting has produced misleading Hubitat level/hue observations
- some Govee app state showed the intended dim level even when Hubitat group/individual state appeared stale

Archived Fade reference:
- build 66
- import code `vtyo`

### Door Lights

Door Lights was simplified toward a V2 focused on reliable temporary raise/restore behavior.

Observed working concept:
- capture state
- door open raises lights
- short watch delay
- lockout/timeout
- restore captured state

Manual-interaction complexity was deliberately removed from V2 to get the core behavior rock solid.

Archived DoorLights reference:
- build 10
- import code `0xia`

### Scene interaction

Govee scene behavior observed:
- Fade moves scene-driven lights to the randomized Fade palette.
- Door-open raise may cause scene-driven strips to return to their prior scene rather than the intended CT 2700 / 100%.
- On timeout, they restore to the Fade color correctly.
- This may be acceptable in some scenarios, but scene mode/state capture remains relevant to future design.

## Guest / Bedtime architecture

This is intentionally isolated as its own architecture problem.

It needs to account for:
- `@GuestsPresent`
- suppression of normal Evening transition
- suppression/handling of the 11:30 PM Night transition
- guests still present at bedtime
- Fade/Evening period
- eventual Night + All Off
- interaction with VB-Bedtime
- late-arrival behavior
- potentially Sadie Noise behavior

Do not reduce this to a one-line Modes patch without reviewing the cross-piston behavior.

## School Mornings known issues

Known incident:
- School Mornings fired while Kids Away was asserted and AndieEffective was true.
- Pausing the piston did not stop already queued 30-minute fade work.

This creates two distinct design problems:
1. effective-presence/Kids Away correctness and where the defect belongs
2. deliberate cancellation/kill behavior for already queued WebCoRE work

Investigation concluded that `cancelTasks` was not the preferred first-choice primitive for the School Mornings abort use case. A programmatic pause -> resume operation was identified as a simpler candidate abort primitive because the observed pause stopped active fade-level repeat work while resume preserves later scheduled executions. This still requires controlled implementation/verification before being treated as production behavior.

Archived School Mornings reference:
- build 29
- import code `3co00`

## Status bridge / SharpTools

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

Project direction:
- avoid returning to flaky Kasa where practical
- H5080 was selected/tested as a candidate Govee plug
- H5083 Matter plugs were targeted for replacement/return
- avoid Govee V2 integration where it conflicts with native integration
- Govee integration/device IP discovery behavior has caused an UpperDeck IP to revert unexpectedly
- “Send discovery broadcast every hour” was turned off during investigation

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
- Occupancy: build 24, import `3q1s`
- Variables: build 15, import `rep9g`
- Bedtime: build 16, import `s6cx`
- DoorLights: build 10, import `0xia`
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
- Master Bedroom: build 45, import `r8x2`

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
