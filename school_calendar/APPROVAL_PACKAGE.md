# One bounded school-calendar approval package

Prepared 2026-10-14; no live change has occurred. This package is approval-ready, not a claim of runtime certification or completed deployment.

## Requested approval

Authorize the seven exact prepared TEST candidates to be temporarily applied/executed, including temporary TEST activation only if needed. Require all 64 calendar/time and 16 native freshness cases to pass. Restore TEST's original definition and paused state on failure or completion.

Authorize supported WebCoRE dashboard fallback to inspect the four school globals, create only missing @SchoolTomorrow boolean false, @SchoolDate string empty, and @SchoolTomorrowDate string empty, and read their types/values back. Preserve existing values during setup and stop on unexpected types. The existing @School must already be boolean. MCP preparation does not prove global existence and current MCP tools cannot list/create those globals. No credentials may be exported to chat/Git; authentication handoff may require the user.

Conditional on passing on-hub tests, verified global types, reviewed merged source and unchanged live baselines, authorize the exact prepared School Mornings, Variables and Modes production candidates. Authorize the exact TEST_seed initialization body to publish today's/tomorrow's four globals once from the actual captured timestamp and verify readback. This global initialization can cause normal subscribed automation reevaluation; no live lighting test, device commands, or test of the full Variables body is authorized. Restore TEST afterward.

A changed candidate or failed/missing test is not covered by this approval. No restart, deployment of MCP, arbitrary remote shell, permission weakening or bypass of operator approval is included.

## Production candidates

| Piston | Prepared remote hash | Intended body hash (fingerprint v2) |
| --- | --- | --- |
| Variables | `df78afd9e70cb5840886e6e3dce5d36601b3cf7ea965d881b52d49e10fc245e9` | `5e06c207ad30162fb96927e7a87b94dee1218562d00627936a5ee802d7616c16` |
| School Mornings | `a68dbbceab01316eb20b835097cd80e1140f760473f978803cfa39c5bdece0f0` | `d896387e36deccf2cb9a61af41c6c62ffcdac5a2d19be4f7420ad48b1870b60a` |
| Modes | `ceb150e8da2d262528ce88da16f3496de9a23a015457fc9197df69a75a922b0a` | `a72994eb54487a9c073d1a9dea9715d979f06d9c0ae67a8464336861b6eec89d` |

All proposed payload hashes and every TEST batch hash are in [approval_manifest.json](cutover/2026-10-14/approval_manifest.json). Full native candidates and rollback bodies are beside that manifest. Sequential TEST writes must use freshly read current remote hashes while binding the original prepared candidate's payload/body hashes. No automatic write replay is permitted.

## Review and validation

- Variables retains every unrelated original section and adds 00:05, 04:50, 17:00 and sunset refreshes; only two seasonal school sections are retired.
- School Mornings keeps all schedules/devices/commands and both existing restrictions, adding one current-date restriction.
- Modes changes exactly two school operands; Scheduled Actions is untouched.
- 39 tests pass, syntax compilation passes, native parser validation reports 456 expression matches, and all 11 candidate bodies pass live prepare on MCP 0.4.14.
- TEST's seven test bodies contain only local assignments/logging. They have no devices, globals, HTTP, schedules, or other-piston commands. TEST_seed is deliberately separate and requires the production approval.
- Current production pistons are active; TEST is paused. Those final activation states must be preserved.

## Do / Expect / Stop if / Next

**Do:** approve this bounded package if desired; the implementation engineer then performs the controlled sequence in PRODUCTION_CUTOVER.md.

**Expect:** exactly 80 on-hub PASS records; verified global values/types; three persisted production bodies; correct daily refresh scheduling; unchanged Scheduled Actions; TEST restored and paused; documented evidence. Observe the next natural execution separately.

**Stop if:** any test fails/is absent, runtime timezone differs, global types are wrong or inaccessible, live baseline changes, candidate hashes differ, persistence is unverified, or a supported security approval is unavailable.

**Next:** run the prepared on-hub matrix, merge only after evidence is satisfactory, apply freshness guard then writer, initialize/read back globals before changing Modes, restore TEST and record final state.
