# Academic calendar handoff

The monthly ChatGPT task reads the official Leander ISD academic calendar at https://www.leanderisd.org/calendar/ and reports changes. The task's ability to call GitHub write tools while running unattended has not been verified. Do not claim an automated publishing pipeline yet.

A candidate calendar submission must include the actual academic-calendar source URL, retrieval timestamp, student closure ranges, early-release dates, and school-year boundaries. The local validator checks its structure before acceptance. A source retrieval failure must never silently replace the last known-good calendar.

The preferred promotion path is a GitHub pull request with automated tests and a human-readable diff. If scheduled tasks cannot write to GitHub, a separate authenticated publisher will be required. Do not place credentials in the repository or scheduled-task instructions.

Production evaluates today's attendance for @School and tomorrow's attendance for evening routines. The monthly calendar review is not a daily execution mechanism. A date freshness guard must protect School Mornings before any live cutover.

Outstanding: prove unattended GitHub publication, read and interpret actual academic calendar data, run CI tests, implement a supported WebCoRE publisher, and approve changes to the existing Variables, Modes, Scheduled Actions, and School Mornings pistons. No production changes are authorized.
