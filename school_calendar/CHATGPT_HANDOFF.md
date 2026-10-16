# School calendar continuation — 2026-10-14

Implementation is corrected and prepared. Resume from APPROVAL_PACKAGE.md and PRODUCTION_CUTOVER.md, not the superseded external publisher/scraper design.

Current interface: WebCoRE MCP 0.4.14, TERMINAL VM healthy/idle with clean recovery, commit 243860500b82f7a3c0ff91f5e5157e22b5e643a1 and digest 1acac29bcf90c8e02679ea4e8702ac8b1c53a4d42427d75c95df9f1197585b8c observed. No restart/redeploy is needed.

No live changes were made during preparation. Variables/School Mornings/Modes/Scheduled Actions remain active; TEST remains paused. Fresh native bodies, exact candidates and preparation hashes are in cutover/2026-10-14. For sequential TEST updates, refresh the current remote hash while retaining each approved proposed hash/body hash. Do not reuse TEST's initial remote hash after the first write.

Pending mandatory approval covers the bounded TEST validation and conditional exact production cutover. Global existence/types are not observable through current MCP tools; supported dashboard fallback must be approved and inspected. Source-only tests and parser matches are not runtime certification. Do not declare completion until runtime/log evidence, persisted bodies, global readback, scheduled refreshes and TEST cleanup are observed and documented.
