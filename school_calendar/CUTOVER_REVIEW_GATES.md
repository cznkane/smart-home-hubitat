# Current cutover gates — 2026-10-14

Supersedes the October 13 validator/runtime handoff.

Passed: current Git branch/CI inspection; verified annual JSON; five live piston identities; healthy 0.4.14 VM with clean recovery; native parser/AST agreement; 39 unit tests; syntax compilation; preservation checks against captured live baselines; live prepare for three production bodies, seven TEST batches and the initialization-only TEST body.

Pending: explicit TEST/production approval; dashboard global inventory/types; 64 on-hub calendar/time cases plus 16 native freshness cases; merged reviewed source; actual application/readback; global initialization/readback; natural refresh/behavior observation; TEST restoration and final production documentation.

Matching versions, language database recognition, upstream source inspection and structural `ok:true` do not certify the installed Hubitat runtime. Stop before production if any expected TEST PASS is absent, any FAIL/type/expression error appears, timezone differs, live baselines change, or globals cannot be inspected/configured through a supported authorized path.
