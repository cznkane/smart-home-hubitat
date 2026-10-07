# Smart Home Change Log

This file records implemented Smart Home automation fixes and architecture decisions that materially change live Hubitat/webCoRE behavior.

## 2026-10-07 — Master Bedroom double-tap Button 4 → All Lights On

**Issue:** #4 — FIX: Master Bedroom double-tap Button 4 invokes canonical All Lights On

### Root cause
The Master Bedroom piston contained legacy empty native operand placeholders (`ro2`, `to`, `to2`) without parsed expression trees. The current safe-update validator rejects those obsolete stubs because they can yield null expressions on Hubitat.

### Exact change
- Removed only the obsolete empty operand placeholder objects from existing Master Bedroom conditions/restrictions. This was a semantically neutral schema cleanup.
- Added a new gesture on the current `B-Master Bedroom Switch`:
  - **double-tap Button 4**
  - action: turn `VB-AllLightsOn` ON
- Reused the existing canonical **All Lights On** piston through its virtual-switch trigger rather than duplicating whole-house lighting logic.

### Preserved behavior
- **single-tap Button 4 → Bedtime**
- Existing Button 1, Button 2, and other configured gestures unchanged.

### Verification
- Affected piston: **Master Bedroom**
- Piston remained active after save.
- Stored definition matched the approved body hash on read-back.
- Read-back result: **MATCH**
- Build changed from **46 → 47**
- Persistence verified: **true**
- Physical wall-button execution was not live-tested during the change.

### Result
- **Single-tap Button 4 → Bedtime**
- **Double-tap Button 4 → canonical All Lights On**

