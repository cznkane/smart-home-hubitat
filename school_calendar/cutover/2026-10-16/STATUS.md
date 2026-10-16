# School-calendar cutover status

Observed 2026-10-16; this records the live check and review package, not a claim of production cutover.

## Git and connector

- PR #40 is open and draft at `b2aef538834eb7ffe0c7a2a7fcda73e89e7b3f5a`; its recorded CI run passed. The feature branch is 9 commits behind current `main` (`088ebcde5399f54e84540595f7a86dfc82fa2f35`) and needs current-main integration plus CI before merge.
- PR #50 (pinned TEST payload data) and webcore-CLI PR #14 (source-backed preparation/apply) are merged. The 0.4.17 source-handoff candidate commit remains an ancestor of CLI `main`.
- Live WebCoRE MCP is 0.4.16. TERMINAL management is healthy, idle and clean at 0.4.16, with 0.4.14 retained as previous release. A bounded 0.4.17 stage request is awaiting the required local operator decision.

## Live piston and global state

| Piston | Build | State |
| --- | ---: | --- |
| Variables | 15 | active |
| School Mornings | 31 | active |
| Modes | 57 | active |
| Scheduled Actions | 46 | active |
| TEST | 3 | paused |

No production piston body has been changed. The approved dashboard setup created `@SchoolTomorrow` (boolean, false), `@SchoolDate` (string, empty), and `@SchoolTomorrowDate` (string, empty); `@School` remains boolean true. A fresh School Mornings activity snapshot also showed `@KidsPresent=false`. Its last-executed timestamp is 08:00 CDT on Oct 16, but the requested historical cursor returned no log entries, so that snapshot does not prove which values were present at 08:00 or why the schedule ran.

School Mornings build 31 retains `@School == true` and `@KidsPresent == true` on each of its three schedules. Compared with the Oct 14 baseline, the two restrictions moved from piston scope to every schedule; schedule commands, including the 30-second fade, are unchanged. The current candidate preserves this placement and adds one piston-level current-date guard. Preparation passed against fresh remote hash `6b4b7f7d192ed469eadd2ea1d7338341b38e9736a57b825fda92c6e01286f7dc`; intended body hash is `1c5d4b66f749742814adfacf54ab69c1c374589006ef94bbca492049810a05fc` (fingerprint v2).

## Validation and remaining gates

- Local calendar suite: 41 tests pass, including coverage for both root-level and per-schedule School/Kids restrictions.
- Seven approved device-free TEST batches remain the authorized runtime matrix. Previous large inline apply calls ended before returning a result; fresh readback confirms TEST is still its original build 3 and paused. No runtime case has been certified.
- The 0.4.17 source-reference route is intended to avoid transferring large JSON through chat. PR #50's 80 resized payloads explicitly require separate approval and are not substituted for the seven candidates in the approved b2 package.
- The Oct 14 production candidates for Variables and Modes still require fresh prepare/hash checks. The School Mornings candidate has changed because its live baseline changed; its exact production cutover requires approval under the existing package's changed-candidate rule.
- Do not merge PR #40 or change production pistons until the approved TEST matrix passes, current branch CI passes, and the refreshed School Mornings candidate is approved. TEST must be restored to build 3 and paused after testing.
