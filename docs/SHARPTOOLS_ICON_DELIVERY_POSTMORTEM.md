# SharpTools Icon Delivery: Failure Analysis and Controlled Process

**Status:** Canonical lessons learned and artifact delivery checklist
**Date:** 2026-10-08
**Applies to:** SharpTools Super Tile image assets, especially ON/OFF icon pairs
**Bootstrap:** [CHATGPT_INIT.md](../CHATGPT_INIT.md)

## Incident summary

During iterative SharpTools icon design, especially Sadie's adjustable desk lamp, the assistant displayed an ON/OFF mockup that the user explicitly approved, but delivered PNGs that differed materially from that approved design. Subsequent attempts compounded the error by recreating silhouettes, treating extracted/derived geometry as equivalent to the source, and shipping additional mismatched ZIPs. The user supplied side-by-side screenshots showing the differences. Previous ZIP integrity checks and image dimension checks were technically valid but did not establish **visual fidelity**.

The user requirement is categorical: **When the user says "approved", no visible change is permitted between the approved mockup and the delivered icon files.** Approval freezes the design, not just the concept or style.

## Observed failures, causes, and required solutions

| Failure | What happened | Preventive control / solution |
| --- | --- | --- |
| Mockup-to-delivery drift | Approved adjustable-lamp mockup was replaced with a differently shaped lamp during export. | Treat the approved pixels/source layers as immutable. Export from the same source, never regenerate or reconstruct without a new mockup and approval. |
| ON/OFF silhouette mismatch | OFF had a filled shade and solid arm while ON used a line-outline shade and double-line arms. | Compare states independently to their **respective** approved mockup panels. Matching ON and OFF to each other is not a substitute for matching the approved preview; the approved pair may intentionally use different fill treatments. |
| Incorrect 'same geometry' claim | Deriving a white image from bright ON pixels did not recreate the approved filled OFF silhouette. | Do not claim equivalence based on shared canvas, bounding boxes, tracing, or algorithmic extraction. Perform direct image-to-reference visual comparison. |
| Background and transparency defects | Black areas, black matte, checkerboard-like preview patterns, and halo artifacts remained in delivered images. | Work from source with real alpha. Inspect RGBA pixels and preview over black, white, and busy dashboard-like backgrounds. If background is baked into foreground, **stop**; do not perform destructive automatic background removal and call it exact. |
| Wrong apparent scale | Same 512 x 512 dimensions hid differences in actual content size and padding. | Compare visible silhouette bounding boxes and perceived size, not only pixel canvas. Preserve approved size and placement. |
| Glow drift and artifacts | Blue glow was too weak, noisy, or changed shape during revisions. | Preview at real SharpTools display size. Preserve approved glow color, radius, intensity, and distribution. Fix only the user-reported issue. |
| Contact-sheet delivery | Two icons were delivered as one combined image rather than two individual state files. | Deliver one PNG per state, and package those exact individual files in a verified ZIP. |
| Unverified download claims | Links, integrity checks, and image properties were sometimes reported without proving the linked assets represented the approved artwork. | Verify files exist at exact linked paths, archive opens, members are correct, sizes are under limit, and each member is a pixel-faithful export. Technical checks alone are not approval. |
| Repeated edits after approval | Post-approval redrawing, resizing, and reinterpretation caused unnecessary regressions. | Approval locks artwork. Any necessary visible edit invalidates the approval gate and requires a new mockup and explicit approval. |

## Required production workflow

### 1. Design and preview

- Show side-by-side ON and OFF mockups before export. Use established Smart Home design language where applicable: white inactive, bright blue/cyan glow active, transparent backgrounds, consistent apparent scale.
- The mockup must be export-ready or backed by individual layered/vector originals that can be exported **without changing visible artwork**.
- Clearly identify when a mockup has only a simulated checkerboard, composited background, or flattened raster that cannot be faithfully separated.
- Preserve the approved preview/source with a stable descriptive identifier and record which state is which.

### 2. Approval freeze

- Explicit user approval is a hard visual freeze for **each state independently**.
- Lock silhouette, line contours, filled/hollow areas, proportions, stroke width, color, glow, scale, position, and any intentional state-specific differences.
- Do not silently 'fix', simplify, vectorize, redraw, re-render, or stylize after approval.
- If source pixels cannot be exported as transparent assets without visible changes, STOP and present a new clean mockup for approval. Do not silently replace the art.

### 3. Exact extraction and packaging

- Export one RGBA PNG per state from the same approved source layers or pixel-faithful extraction.
- Default canvas 512 x 512, but honor any specifically approved format. Keep every individual PNG strictly below 1 MB for SharpTools.
- No embedded background, checkerboard, black matte, or unrelated objects.
- Compare the **actual exported PNG**, not a regenerated preview, against the corresponding approved panel at both full size and expected dashboard size.
- Inspect alpha and composite over light, dark, and visually busy backgrounds. Verify ON and OFF scale and centering.
- If comparison fails, do not release. Revert to source or return to approval gate.
- Build ZIP from those same inspected PNG bytes; verify member filenames and integrity. No contact sheet in place of state files.
- Provide verified ZIP and, where useful, individual PNG links. Never invent paths or claim checks not performed.

### 4. Acceptance and archive

- User dashboard screenshots are the acceptance evidence. Do not confuse Super Tile layout issues with image defects.
- If a defect is reported, change only that aspect and show a new mockup when any visible artwork will change.
- Record accepted versions and relevant source assets when available. Do not treat an unsuccessful ZIP as the approved baseline.
- Never overwrite or rewrite the approved original while experimenting; use a new versioned artifact and preserve rollback.
- Document provenance: approved preview identity, source asset, exported PNG identities, checks performed, and any remaining uncertainty.

## Release checklist

- [ ] User saw BOTH final state mockups and explicitly approved them.
- [ ] Each export is derived directly from the approved artwork, not regenerated or independently redrawn.
- [ ] OFF export matches OFF preview; ON export matches ON preview, including any intentionally different fill treatment.
- [ ] No visual changes occurred after approval.
- [ ] Actual RGBA alpha verified; no baked-in background or black matte.
- [ ] Full-size and tile-size previews visually checked on contrasting backgrounds.
- [ ] Scale, position, silhouette, line weight, glow, and color match approved reference.
- [ ] Each file is separate, appropriately named, and < 1 MB.
- [ ] ZIP includes the exact checked PNGs; archive integrity verified.
- [ ] All provided download paths exist and point to the inspected artifacts.
- [ ] If any check fails, stop delivery and return to preview/approval; never claim success.

## Scope and current disposition

This is a process postmortem, not proof that the Sadie lamp ZIP issue has been resolved. The prior mismatched exports are **rejected**. The user-supplied approved side-by-side lamp mockup is the design reference. A future delivery must be exported faithfully from that approved source, or must first receive renewed approval for an export-ready reference.

Do not infer that this documentation authorizes modifications to live SharpTools, Hubitat, or WebCoRE. Follow the operating protocol for operational changes.
