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

## V2.1 preview transparency regression

V2 was approved. V2.1 changed visible lamp geometry and glow instead of preserving the V2 design. It also showed a checkerboard pattern as part of the preview without establishing actual alpha transparency. The user rejected V2.1.

**New required gate before showing a preview for approval:**
- A preview claimed to be transparent must come from an actual alpha-bearing source file, not a flattened image with a checkerboard pattern.
- Check corner and background alpha values: empty background must be alpha zero, including between silhouette elements. RGBA mode by itself does not prove this.
- When transparency is uncertain, composite the same file over both light and dark backgrounds to demonstrate real transparency.
- If the preview has a baked-in checkerboard or background, label it as flattened and do not seek final export approval. Create a verifiably transparent master and show that for approval.
- An approved version is the immutable baseline. Later versions may change only explicitly requested properties, and any visible difference requires separate approval.
- Perform the transparency gate before approval, not merely at ZIP creation.

**Disposition:** V2 remains the accepted visual baseline; V2.1 is rejected.

## Scope and current disposition

This is a process postmortem, not proof that the Sadie lamp ZIP issue has been resolved. The prior mismatched exports are **rejected**. The user-supplied approved side-by-side lamp mockup is the design reference. A future delivery must be exported faithfully from that approved source, or must first receive renewed approval for an export-ready reference.

Do not infer that this documentation authorizes modifications to live SharpTools, Hubitat, or WebCoRE. Follow the operating protocol for operational changes.


## 2026-10-09: Kids Away repeat failure and hard-stop production contract

**Incident:** The user approved the running ponytail child design (white OFF / cyan-blue ON). Instead of exporting the approved art, the assistant called image generation again, producing a different pair with a flattened checkerboard. The assistant then described the result as an icon set. This is the same failure mode as the lamp and pool icon incidents, despite the earlier postmortem. The repeated failure demonstrates that prose reminders alone are not an effective control.

**Root cause:** Design generation and artifact production were not separated by a tool-level gate. The assistant treated approval as permission to make a new rendition rather than permission to export the existing rendition. The preview had no independently verified transparent per-state master. As a result, the task was not actually export-ready at approval time.

### Mandatory hard stops (apply to ALL SharpTools icon work)

1. **Before showing an approval candidate:** Produce separate OFF and ON source assets with genuine alpha transparency, preferably deterministic SVG or layered RGBA. If the displayed concept is generated and has no verified export-ready masters, explicitly label it *concept only, not approvable for production*; request approval of export-ready files later. A visually attractive image does not satisfy the source gate.
2. **Before requesting final approval:** Verify each actual state file, not merely a side-by-side screenshot: transparent background between contours and at corners, correct geometry, clean edges, no foreign pixels, correct state-specific appearance. Composite the actual state PNGs on light and dark backdrops for review. Record file paths, dimensions, content hashes and whether source is editable.
3. **At approval:** Freeze exact per-state file bytes or the export-ready layered/vector master plus deterministic export parameters. Approval is not authorization to call a generative image tool again. **Do not call image generation after approval** for production assets. Do not reconstruct by tracing, color-keying a checkerboard, or inventing a new silhouette.
4. **If only a flattened/checkerboard concept exists:** STOP. State that the source cannot be faithfully exported as transparent without altering pixels; obtain a newly reviewed export-ready master. Never silently substitute a redraw. The earlier concept approval remains design direction, not final artifact approval.
5. **For change requests like “glow ONLY”:** Modify a copy of the exact original using deterministic layer operations; keep the source layer byte-identical in the composite, and add glow only underneath. Verify before/after geometry, scale, placement and source pixels. No generative calls.
6. **For splitting combined images:** Never assume the midpoint is a safe crop. Inspect both objects' actual visible and halo bounds; prevent neighboring icon/glow bleed. If clean separation is impossible, STOP and request independent masters.
7. **For packaging:** Never create or announce a ZIP before source/approval/export gates pass. Check alpha, pixel-faithful comparison, per-file size (<1 MB), ZIP integrity, and actual linked paths. A ZIP integrity test is NOT a visual fidelity test.
8. **When a user reports “fail” or rejects a delivery:** Mark the variant rejected, retain the previous approved source, diagnose the specific gate failure, and **do not generate a new replacement without a new design request**. Show corrected actual exported files before delivery.

### Kids Away disposition and recovery

- **Approved design direction:** Side-by-side running ponytail child, backpack and skirt, white OFF and bright electric-blue/cyan ON. The first concept was approved by the user.
- **Rejected:** Subsequent regenerated “transparent checkerboard” version; not source-faithful and not proven transparent.
- **Current production status:** **NOT DELIVERED / NOT APPROVED FOR EXPORT.** Do not claim there is a usable Kids Away ZIP or that the first concept can be exactly extracted until the source is inspected.
- **Recovery:** Locate the exact originally approved image; inspect whether it has genuine alpha and separable per-state art. If it does, use deterministic pixel-preserving extraction, inspect each state, and seek approval on the actual export-ready assets. If it does not, stop and prepare a transparent master with explicit renewed approval. Never silently regenerate after approval.

**Enforcement phrase:** *No source, no export. No verified transparency, no final approval. No generation after approval. No ZIP before fidelity proof.*
