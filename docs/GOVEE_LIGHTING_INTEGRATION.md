# Govee Lighting Integration and Scene Behavior

**Status:** Canonical Smart Home subsystem record  
**Scope:** Govee lighting, Hubitat/WebCoRE integration, DreamView/music-sync capability, scene behavior, and known network/discovery issues  
**Last reconciled:** 2026-10-07

## Purpose

This document retains durable Govee-specific Smart Home knowledge that is too detailed for `SMART_HOME_RETAINED_CONTEXT.md`.

Live Hubitat/Govee/WebCoRE state remains runtime truth. This document records architecture, observed behavior, decisions, limitations, and unresolved work. Do not store Govee account credentials, API keys, tokens, or other secrets here.

## Device context

### UpperDeck

- Hubitat device name: `UpperDeck`
- Govee model: **H6176**
- Outdoor RGBIC strip
- Govee app showed **LAN Control enabled**
- Hubitat exposes ordinary light controls including on/off, level, color temperature, hue/saturation/color, and state save/restore behavior through WebCoRE.
- During the IP investigation, the intended/current IoT-side address was `192.168.2.169`. Treat that address as historical configuration evidence, not a permanent reservation unless live UniFi/Hubitat state confirms it.

### Indoor bulbs

- Primary indoor Govee bulb model observed in this work: **H6008**
- Examples seen in Govee Desktop included Bed, Console, Couch, Desk, Dresser, Floor Lamp, Guitars, Piano, Rocker, Sadie, and other lights.
- A separate Govee H619D device named Kitchen was observed as eligible for Desktop Music DreamView.

## Hubitat grouping architecture

Hubitat Groups and Scenes is used to create command-oriented lighting groups for WebCoRE.

Known group names include:
- `G-LivingRoom`
- `G-DiningKitchen`
- `G-Deck`
- `G-Master`

For these groups, the design intent is a **command endpoint**, not an authoritative aggregate state device.

The working configuration direction established in this chat:
- group device type: bulb
- Zigbee group messaging: off for these Govee/non-Zigbee groups
- group state aggregation options: off
- on/off optimization: on
- metering/logging: off unless needed for diagnosis

Hubitat UI lesson: existing child groups may be hidden under the small expand control on the main Apps list next to **Groups and Scenes**. Expanding the parent app reveals the individual `G-*` child group apps for editing. Do not rely on Device -> In Use By to locate the group editor.

## Govee grouping and DreamView

Govee Home has a separate grouping/DreamView layer. It is not interchangeable with Hubitat Groups.

An existing Govee Universal Group named **UT all lamps** contained 13 devices during this investigation.

For synchronized music effects, the Govee-native path explored was:

Govee Home -> Feature Hub -> Group&DreamView -> Create -> Music DreamView

Music DreamView requires an eligible **Sync Center**. The mobile app reported **No supported devices yet** for the then-current device inventory.

### H6176 music behavior

The H6176 UpperDeck strip can react to music for its own native music mode, but the Govee app did not recognize it as a Music DreamView Sync Center.

Durable distinction:
- a device having its own microphone/music-reactive mode does **not** imply that it can act as a DreamView Sync Center for other devices.

## Music synchronization requirements and product limitations

Project requirement established in this work:
- synchronize **all** desired Govee lights, not only a small subset
- include UpperDeck and the indoor bulbs
- avoid Bluetooth as the transport
- prefer LAN/Wi-Fi/local-network control
- music source is associated with the Sonos/whole-home listening environment

### H1162 Music Sync Box

Rejected for this project direction because it uses Bluetooth and has a small-device-count limit relative to the whole installation. It may be useful in other contexts, but it does not satisfy the retained requirement of all devices over non-Bluetooth transport.

### Govee Desktop

Important platform limitation: **Govee Desktop is Windows-only** for this use case. Do not plan a macOS-native Govee Desktop controller.

Observed on Windows Govee Desktop:
- **Music DreamView** displayed a capacity of `0/50`, but only the H619D Kitchen device appeared eligible.
- H6008 bulbs and H6176 UpperDeck did **not** appear as Music DreamView-selectable devices.
- **Scenic DreamView** also displayed a `0/50` capacity and showed approximately 15 devices, including the H6008 bulbs and, per user confirmation, UpperDeck H6176.
- Therefore, the network/device visibility exists for Scenic DreamView while Govee applies a narrower compatibility boundary to Music DreamView.

Durable architectural lesson: do not diagnose the H6008/H6176 Music DreamView absence as a generic LAN reachability failure merely because they are absent from Music DreamView. The same Desktop installation can see those devices for Scenic DreamView.

### Unresolved music-sync direction

No production solution was selected in this chat that satisfies all requirements.

Potential future directions:
1. determine whether Govee exposes a supported programmable interface for Scenic DreamView that can be driven by music analysis
2. evaluate direct local/LAN control of compatible Govee devices from a local controller, with music analysis performed outside Govee
3. continue evaluating future Govee hardware/software that supports the full device set over LAN/Wi-Fi

Do not treat speculative direct-LAN music visualization as an implemented design.

## UpperDeck IP/discovery issue

Observed problem:
- UpperDeck's Hubitat Device Network ID was manually corrected to an IoT-side `192.168.2.x` address, specifically `460/192.168.2.169` during the investigation.
- The user reported Hubitat/Govee integration behavior that reverted the device to a `192.168.1.x` address.
- The text `192.168.1...` seen in the Hubitat device **name** was manually entered text and is **not** evidence of rediscovery by itself.
- The device Preferences screen did not expose a direct IP preference.

Relevant parent/integration setting discovered:
- **Send discovery broadcast every hour** was enabled.
- It was turned **off** during the investigation.

Working hypothesis:
- periodic Govee LAN discovery was the likely mechanism capable of rewriting rediscovered device network information.

Current classification:
- hourly discovery is disabled as a mitigation
- root cause of why discovery could prefer/learn the wrong subnet address was **not proven** in this chat
- do not state that the discovery toggle definitively fixed the issue without persistence/live verification
- avoid manually running discovery while testing whether the corrected DNI remains stable, unless discovery itself is the controlled test

## Fade and Door Lights interaction with native Govee scenes

This chat materially refined the scene-interaction diagnosis.

### Proven observed sequence

When a Govee light/strip is displaying a native Govee scene:

1. **Fade runs**
   - Fade successfully moves the light away from the native scene to the randomized curated Fade RGB color/palette.
   - The light is dimmed as intended by Fade.

2. **A door opens**
   - Door Lights intends to temporarily raise the lights to **2700 K / 100%**.
   - Instead, affected Govee scene-capable lights can return to their **previous native Govee scene**, brightened, rather than displaying the intended 2700 K white.

3. **Door Lights timeout expires**
   - the light correctly restores to the **Fade randomized RGB color** that was active before the door-open override.

This is more precise than the earlier theory that Govee scenes simply could not be saved/restored.

### Diagnostic implication

The successful post-timeout restoration means the Fade-state capture/restore path is substantially working. The defect is concentrated in the **temporary Door Lights override** to CT 2700 K / 100%, not in the final restoration to Fade.

A prior WebCoRE log included a warning that it could not set `colorMode` directly while restoring device state. That remains relevant because Govee/native scene state, RGB mode, and CT mode may not map cleanly to Hubitat's writable standard attributes.

### Working hypothesis, not yet proven

A native Govee scene/effect context may remain latent after Fade has changed the visible output to RGB. When Door Lights sends its level/CT commands, the Govee integration/device may reassert the prior scene instead of cleanly entering CT mode.

This requires controlled observation before code changes.

### Planned diagnostic

Compare Hubitat **Current States** for UpperDeck/affected Govees at two moments:
1. while the device is correctly showing its Fade RGB color
2. while Door Lights has caused it to return incorrectly to the old Govee scene

Inspect at minimum:
- `colorMode`
- `colorTemperature`
- `hue`
- `saturation`
- `level`
- any custom scene/effect/mode attributes exposed by the driver

Goal: determine whether Hubitat actually observes the scene/mode transition or whether the Govee device changes underneath a stale Hubitat state model.

Do **not** change Fade or Door Lights merely to run this observation.

## Scene commands from WebCoRE

Unresolved requirement:
- determine how to invoke **native Govee scenes/effects from WebCoRE**.

Reason:
- scene-aware automation could intentionally select or restore native Govee effects instead of attempting to reconstruct them only from RGB/CT/level attributes.

Investigation direction:
- inspect the full Hubitat command surface for an affected Govee device such as UpperDeck
- look for driver commands/attributes related to scene, effect, mode, snapshot, or similar concepts
- determine whether WebCoRE can invoke the driver's custom command safely

No scene-command API/command name was proven in this chat. Do not invent one.

## Potential intentional Door Lights behavior

The scene reappearance on door-open is not necessarily undesirable in every context.

Two potentially valid future Door Lights behaviors were identified:

1. **Functional raise**
   - force 2700 K / 100%
   - optimized for useful task/entry illumination

2. **Ambient raise**
   - deliberately bring the existing/native Govee scene up while the door is active
   - return to the prior Fade color after timeout

Do not globally eliminate the scene behavior until the mechanism is understood and the desired policy is chosen. If implemented, the policy may eventually depend on mode, time, door, or an explicit variable, but no production selection logic was decided here.

## Lessons learned

- Govee **device visibility**, **Scenic DreamView eligibility**, **Music DreamView eligibility**, and **Sync Center eligibility** are separate capability gates.
- A native music mode on a Govee device does not prove it can coordinate other devices.
- Hubitat aggregate group state can be misleading for Govee devices; command success and device/app state may diverge from group-reported hue/level.
- Do not treat a manually edited Hubitat device name containing an IP address as network-state evidence.
- Discovery settings can mutate device identity/address state and therefore belong in the change-control model.
- For scene-capable devices, visible RGB/CT state may not fully describe native effect context.
- When temporary override and final restore behave differently, isolate the failing phase before redesigning the snapshot/restore mechanism.

## Open items

- Verify whether UpperDeck remains stable on the intended IoT address with hourly discovery disabled.
- Determine why discovery could learn/prefer the wrong subnet address.
- Inspect/confirm the Hubitat driver command surface for native Govee scene/effect invocation.
- Determine whether WebCoRE can send native Govee scene commands.
- Capture Current States during Fade versus erroneous Door Lights scene reappearance.
- Decide whether Door Lights should support both functional-white and ambient-scene raise behavior.
- Find a non-Bluetooth, whole-installation music synchronization architecture, or explicitly accept a different requirement.
