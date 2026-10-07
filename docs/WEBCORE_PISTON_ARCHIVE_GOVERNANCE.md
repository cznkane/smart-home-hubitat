# WebCoRE Piston Archive Governance

**Status:** Canonical durable project record
**Last reconciled:** 2026-10-07

## Source of truth

Live WebCoRE is runtime truth. Git is engineering/history/reference truth. The newest archived piston record is the reference baseline when live inspection is unavailable.

The Smart Home To Do thread is the master TODO and historical piston-archive intake point. Latest dedicated-thread state and newer canonical Git evidence supersede older notes. Completed work stays removed unless newer evidence explicitly reopens it. Do not infer unfinished work.

## Authoritative archive identities from the To Do archive

| Piston | Build | Import |
|---|---:|---|
| Modes | 57 | `xtp9` |
| Occupancy | 48 | `7dxps` |
| Variables | 15 | `rep9g` |
| Bedtime | 16 | `s6cx` |
| DoorLights | 10 | `0xia` |
| Fade | 66 | `vtyo` |
| Manual Chlorinator | 8 | `p0cih` |
| Mode Actions | 37 | `n82s` |
| Rick Presence | 6 | `s7tk` |
| Scheduled Actions | 46 | `r6em` |
| School Mornings | 29 | `3co00` |
| All Lights Off | 36 | `wbwwo` |
| All Lights On | 40 | `gjiyv` |
| Fridge | 6 | `27ed9` |
| Living Room | 10 | `co995` |
| Master Bedroom | 45 | `r8x2` |

These identities describe the screenshot archive at the time captured, not necessarily current live bodies. Newer Git/live evidence already supersedes some screenshot identities. For example, Git issue #3 records Occupancy build 49 after the archived build 48, and issue #4 records Master Bedroom build 47 after archived build 45. Never downgrade live/current reasoning to an older screenshot.

## Durable archive-era decisions

- Modes build 57 added ModeStatus publication of `TIME_Dusk(duskStarted)` and `TIME_Evening(eveningDue)`.
- Scheduled Actions build 46 owns the daytime low-light policy: WeatherFlow below 10,000 lux for 30 minutes, 9:30 AM-4:30 PM, Location mode Home, then invoke `VB-AllLightsOn`. Environmental/time policy belongs in Scheduled Actions rather than All Lights On.
- Variables build 15 shows P-Guest driving `@GuestsPresent`; older retained language describing P-Guest as a kid-home override is superseded.
- Bedtime build 16 already implements late-arrival behavior and the 4:50 AM cleanup. Remaining bedtime work is guest-at-bedtime policy.
- DoorLights build 10 superseded older heavy-debug/watch-delay designs with V2 captured-state restoration. Field validation remains appropriate; reopen implementation debugging only on observed failure.
- Fade build 66 established the curated hue list `0,20,110,150,190,220,250,280,310,335` and independent zone randomization. Palette implementation is complete; scene/state interaction remains separate work.
- Dusk recovery/hysteresis was intentionally removed from active TODO unless explicitly reopened.

## Completed archive-era work that must not be resurrected without newer evidence

Occupancy/KidsAway cleanup as it existed at that point; School Departure Seen cleanup; Kids Geofency/presence architecture; Rick Presence; initial School Mornings debugging; B-Kitchen/Fridge verification; GuestsPresent implementation; curated Fade colors; late-arrival Bedtime/4:50 cleanup; Jackery/chlorinator/Sadie Noise schedule modernization; legacy @CDT; mailbox false-Away; CarPlay delayed arrival; Mode Engine core review.

Later evidence may supersede a completed item. Issue #2 and issue #3 contain the later Occupancy/KidsAway corrections and therefore outrank the archive-era completion statement.

## Screenshot package history

All 16 authoritative To Do screenshot attachments were programmatically accessible. Exact PNG bytes were materialized without image processing and base64 round-trip integrity was verified. A local package was created containing:
- 16 `pistons/<Piston-Name>/current.png` files
- `pistons/README.md`
- `pistons/SHA256SUMS.txt`
- `webcore-piston-archive.zip`

The ZIP was verified to contain 16 PNGs matching source SHA-256 values.

Direct binary publication to GitHub was not completed because the GitHub connector could not consume the materialized conversation files across the connector boundary. Therefore the existence of the local ZIP must not be mistaken for a committed Git screenshot tree.
