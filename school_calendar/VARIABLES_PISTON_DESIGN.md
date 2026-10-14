# Variables piston native calendar design

Owner: existing Variables piston, freshly verified build 15 on 2026-10-14. Native candidate is complete and live-prepare validated; not yet deployed/runtime certified.

One constant schoolCalendarClosures string contains the canonical JSON's 35 delimited weekday closure dates. Each refresh captures $now into schoolCalendarNow, then derives today's and tomorrow's boolean/date from the same timestamp. Functions: formatDateTime, addDays, weekDayName, contains, concat, isBetween, and if. Exact matching expression text accompanies every native parsed AST. Bounds derive from JSON, not hard-coded handoff dates.

Refreshes: 00:05, 04:50, 17:00 and sunset. Existing 04:50 late-arrival logic remains a separate unchanged block. Each school boolean precedes its date stamp. Only obsolete seasonal school sections 7 and 10 are removed; all other original sections are byte/logic-preserved.

Runtime certification, global type/existence checks, rollback and cutover order are mandatory in PRODUCTION_CUTOVER.md. Do not execute the full Variables body as a test.
