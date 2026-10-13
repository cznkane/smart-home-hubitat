# Variables piston: school calendar design

## Live baseline (read-only, October 13 2026)
`Variables` piston ID `:d5f5963fee53c8113b294d4baf24c6e9:` is active. Its native body contains two competing seasonal `@School` writers: April 27 at sunset -> false; July 11 at sunset -> true. It also controls `@Holidays`, `@LateArrivalActive`, and `@GuestsPresent`, which must remain untouched.

## Decision
Use the existing `Variables` piston as the owner of daily `@School` state. Do not introduce a separate authenticated variable-writing service. The academic calendar is interpreted and updated once each school year. An executable calendar representation must be delivered into WebCoRE in a supported form; the GitHub JSON file is not directly readable by a piston without an explicit data transport. Avoid claiming the current piston can access local GitHub files.

## Required implementation
1. Choose and verify a supported WebCoRE-native date/closure lookup: either embed generated school-day ranges in the piston annually or use a verified read-only HTTP calendar endpoint with safe failure behavior. Prefer generated in-piston conditions if size and compatibility permit.
2. Replace the two seasonal `@School` writers with a daily date-aware computation. Include weekends, closures, and school-year bounds. Early release remains a school day.
3. Write `@School` and `@SchoolDate` together; if tomorrow status is supported, also write `@SchoolTomorrow` and `@SchoolTomorrowDate`.
4. Before enabling the writer, add a freshness restriction to `School Mornings`: `@SchoolDate` must match the local date. A failed update must never permit a stale true value to run morning lighting.
5. Update `Modes` for tomorrow's school status and audit `Scheduled Actions` before changing its school-dependent schedule.
6. Use WebCoRE prepare -> inspect diff and compatibility -> explicit approval -> apply -> verify persistence. Preserve rollback snapshots and never trigger lighting tests during the cutover.

## Status
Design documented only. The native condition encoding, maximum piston size, and live compatibility have not yet been verified. No production piston update has been made.
