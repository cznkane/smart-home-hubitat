# TERMINAL restricted VM management commissioning

Status: implementation release candidate in cznkane/webcore-CLI PR #5; no production installation authorized or performed by this engineering task. Canonical tracking: issues #36 and #43. Current source, security assessment, pinned Windows CI artifacts and installation/recovery procedure are maintained with the implementation PR. This record does not certify installed TERMINAL state.

## Architecture

The existing SYSTEM SmartHome-WebCoRE-MCP and existing watchdog retain their identity, triggers, tunnel configuration, credential references and automation responsibilities. A separate SYSTEM broker performs only fixed release/restart transactions after independent scoped approval. A separate limited local account runs verified tests and syntax validation with no production-credential access, immutable input files, a private scratch directory, user-scoped outbound deny and Windows Job Object containment. Local named pipes use restrictive DACLs, remote-client rejection, SID/PID/executable verification and bounded frames. No arbitrary shell, caller-supplied command/path/argument/environment, TCP listener or MCP approval issuer is introduced.

Every changing operation binds operation, commit/snapshot identity, release digest and expected current digest to a five-minute one-use grant. The independently selected human operator approves through a native UAC approval window on TERMINAL or an authenticated remote-desktop session. Routine management needs an approval click, not a PowerShell command relay. Broker restart invalidates pending approvals. Metadata-only audit is flushed to protected daily JSONL; unavailable audit prevents execution.

The six operations are tests, syntax check, merged pinned-source staging, release deployment, prior-release rollback and MCP restart. The MCP adapter adds two read tools and one write/destructive request tool only after verified commissioning. The request is open-world because staging contacts the fixed canonical GitHub source. Existing Business policy stays Allow read tools; do not weaken it. Operator approval is independent of ChatGPT/MCP permission prompts.

## Trust and operational limits

SYSTEM and local administrators remain trusted. Existing MCP already has SYSTEM privileges; this installation does not elevate it, and this boundary cannot defend against a compromised SYSTEM process. Test suites are approved trusted code, not an untrusted-code sandbox. Native artifacts are unsigned and require pinned-source/CI-package digest verification. Process output is suppressed; audit/results contain metadata only. There is no new unattended external approval portal.

Controlled cutover inhibits the watchdog only for the transaction, changes only the selected payload path, verifies the tunnel's actual Node child/payload, restores watchdog enablement, and automatically restores prior configuration on a local failure. Uncertain broker death leaves a durable recovery marker and requires independent local recovery. The existing watchdog and administrator recovery procedure are the out-of-band path if the tunnel is unavailable. No new framework is allowed to replace the already accepted watchdog/email configuration silently.

## Installation gates

1. Approve review/merge and separately approve production commissioning. Deploy only the exact reviewed commit reachable from canonical main; if merge rewrites the candidate SHA, rebuild/test/package that resulting commit.
2. Download the successful Windows CI artifact and independently verify its digest. Extract into an administrator-owned directory whose ancestors prevent ordinary-user replacement. Do not run a floating branch archive or weaken permissions/execution policy.
3. Run the packaged preflight. It checks package components, immutable source/ancestors, existing runtime identity/launcher, protected files, Node 24, firewall profiles and task state. No live changes occur. Ambiguous or unexpected current state is a stop condition.
4. Install only the new boundary. Reinstall is validation-only. Existing task XML, tunnel YAML, watchdog/SMTP files and credential files are retained. The selected operator identity is fixed from the administrator session. Initial cutover is independently queued/approved through the installed window.
5. Verify installed hashes/ACLs, limited identity, actual Node payload, MCP initialize/tools, exactly one intended tunnel, Business Admin refresh and fresh-chat status/Maker reads plus one approved syntax request. Expected enabled 0.4.11 inventory: 25 tools, 19 read and 6 write, subject to exact pinned source verification.
6. Complete controlled reboot and rollback acceptance only after separate authorization, then classify active/rollback/retire/investigate inventory and document real outcomes.

GitHub Windows hosted CI is development evidence, not evidence that TERMINAL has been changed. Production schedules, device logic, active/paused pistons and tunnel credentials are outside this installation's mutation scope.

## Recovery and retirement

Retain the original payload and protected original YAML as initial break-glass inventory. The packaged Recover mode disables the new management tasks and restores the original runtime, including original watchdog enablement; it avoids restarting an already-selected healthy original runtime. Uninstall requires prior recovery, removes only new tasks/account/profile/logon rights/outbound deny/shortcut/commissioning marker, and retains protected audit/recovery/payload files for explicit retirement. Do not declare no-dust completion while retained inventory lacks an owner and retirement condition.

The legacy vm_git_status tool inspects C:\SmartHome\webcore-CLI, which is not proof of the active versioned payload. Use management health plus actual process/MCP identity for the new active release. An initial imported snapshot is explicitly identified as a local snapshot, not a Git commit.

## Read-only evidence during preparation (2026-10-13)

Live WebCoRE status reported plugin 0.4.10, connected=true, dashboard_confirmed=true and hub_snapshot. VM diagnostics identified TERMINAL Windows 11 Pro; the existing MCP task was Running, watchdog Ready with result zero, and the legacy inspected checkout was clean at e8eceeed487fe27dad566bdbe5ed50c160156d39. These observations prove read-path availability at their timestamps, not the installed worker or active-payload Git identity. No production write, installation, restart or device test was performed by this engineering task.
