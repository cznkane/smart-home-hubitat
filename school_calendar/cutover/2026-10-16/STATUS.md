# School-calendar cutover status

Observed 2026-10-16; this records the live check and review package, not a claim of production cutover.

## Git and connector

- PR #40 is open and draft at head `4c889551eb1924a77e8c606251dbe80dc19ad244`; CI run `38944714392` passed. The feature branch was observed 9 commits behind current `main` (`088ebcde5399f54e84540595f7a86dfc82fa2f35`) and needs current-main integration plus CI before merge.
- PR #50 (pinned TEST payload data) and webcore-CLI PR #14 (source-backed preparation/apply) are merged. The 0.4.17 source-handoff candidate commit remains an ancestor of CLI `main`.
- Approved WebCoRE MCP 0.4.17 deployed successfully from `fd84df61ed6da2a894ba399ffdbd0067cb020ba4` (SHA-256 `e9242aef536ebda2a7c63480474132314a49133bfa059346f3205f399a983aa4`). TERMINAL reports healthy, idle, clean recovery, and exact current release; the Hub confirms dashboard, piston-list, and device access on plugin 0.4.17. No restart was needed.

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
- Seven approved device-free TEST batches remain the authorized runtime matrix. The 0.4.17 prepare for approved `TEST_1.json` matches expected remote/body/payload hashes, but transport preflight fails at 161,568 encoded bytes (99-chunk maximum). TEST remains build 3 and paused; no batch was written or executed, and no runtime case is certified. The currently exposed prepare interface accepts native JSON bodies but does not expose the pinned source-reference handoff, so do not bypass the size gate.
- PR #50's 80 resized payloads explicitly require separate approval and are not substituted for the seven candidates in the approved b2 package. Fresh 0.4.17 prepares for Variables and Modes still match their approved body/payload hashes and pass transport preflight. The refreshed School Mornings candidate also prepares successfully against build 31, but its changed production candidate requires approval under the existing changed-candidate rule.
- Variables and Modes production candidates pass fresh 0.4.17 prepare/hash checks. School Mornings also passes prepare, with current hash `1c5d4b66f749742814adfacf54ab69c1c374589006ef94bbca492049810a05fc`; it remains outside the original production approval because the candidate changed after the baseline refresh.
- Do not merge PR #40 or change production pistons until the approved TEST matrix can pass, current-main integration CI passes, and the refreshed School Mornings candidate is approved. Current 0.4.17 transport ceiling blocks TEST_1 before any write. TEST must be restored to build 3 and paused after testing.
