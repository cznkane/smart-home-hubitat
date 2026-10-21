# School calendar — maintained source and historical test fixtures

**Production status (2026-10-21): deployed.** See [canonical production record](../docs/SCHOOL_CALENDAR_PRODUCTION_RECORD.md) for live piston IDs, builds, rollback predecessors, and evidence boundaries.

This directory preserves the calendar engine, source, tests, and design work from [closed PR #40](https://github.com/cznkane/smart-home-hubitat/pull/40). The `cutover/2026-10-14/baselines/` JSON files are **historical test fixtures only**, retained because `test_cutover_preservation.py` requires them. They are **not** current WebCoRE production definitions.

Do **not** execute candidate-builder outputs, reapply old cutover manifests, or interpret historical approvals as authorization to alter production. Any production change requires fresh live readback, review, rollback planning, and separate approval under the operating protocol.

## Verification

Run `python -m unittest discover -s school_calendar -p 'test_*.py' -v`. The GitHub Actions workflow runs this suite for pull requests that modify this directory. Passing tests validate repository code, **not** live WebCoRE behavior or source-to-live equivalence.

## Historical record

For original October 14–16 design notes, candidate snapshots, and approval packages, refer to [PR #40](https://github.com/cznkane/smart-home-hubitat/pull/40/files). Those instructions describe a **superseded pre-deployment state** and are not part of this preservation PR.

## Annual maintenance

Review the official academic calendar, update the academic-year JSON, validate boundary cases and closures, and obtain explicit approval before any WebCoRE deployment. The existing production configuration remains authoritative until independently changed and verified.
