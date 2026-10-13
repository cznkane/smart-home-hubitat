# TERMINAL restricted VM management commissioning

Status: PR #5 merged with user approval as f4c3ca3a78338dbe8d22464ec517ba40dfb80eac; production installation authorized but preflight stopped before provisioning. Corrective 0.4.12 implementation in cznkane/webcore-CLI PR #8 was merged with explicit approval as 9b15da31b9845883b03ac0fc2c0c61f66455d0c5. No production installation or cutover has occurred. Canonical tracking: issues #36 and #43. Current source, security assessment, pinned Windows CI artifacts and installation/recovery procedure are maintained with the implementation PR. This record does not certify installed TERMINAL state.

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
5. Verify installed hashes/ACLs, limited identity, actual Node payload, MCP initialize/tools, exactly one intended tunnel, Business Admin refresh and fresh-chat status/Maker reads plus one approved syntax request. Expected enabled 0.4.12 inventory: 25 tools, 19 read and 6 write, subject to exact pinned source verification.
6. Complete controlled reboot and rollback acceptance only after separate authorization, then classify active/rollback/retire/investigate inventory and document real outcomes.

GitHub Windows hosted CI is development evidence, not evidence that TERMINAL has been changed. Production schedules, device logic, active/paused pistons and tunnel credentials are outside this installation's mutation scope.

## Recovery and retirement

Retain the original payload and protected original YAML as initial break-glass inventory. The packaged Recover mode disables the new management tasks and restores the original runtime, including original watchdog enablement; it avoids restarting an already-selected healthy original runtime. Uninstall requires prior recovery, removes only new tasks/account/logon rights/outbound deny/shortcut/commissioning marker, and removes the worker profile or schedules protected cleanup at next startup if Windows retains its batch-logon hive, and retains protected audit/recovery/payload files for explicit retirement. Do not declare no-dust completion while retained inventory lacks an owner and retirement condition.

The legacy vm_git_status tool inspects C:\SmartHome\webcore-CLI, which is not proof of the active versioned payload. Use management health plus actual process/MCP identity for the new active release. An initial imported snapshot is explicitly identified as a local snapshot, not a Git commit.

## Read-only evidence during preparation (2026-10-13)

Live WebCoRE status reported plugin 0.4.10, connected=true, dashboard_confirmed=true and hub_snapshot. VM diagnostics identified TERMINAL Windows 11 Pro; the existing MCP task was Running, watchdog Ready with result zero, and the legacy inspected checkout was clean at e8eceeed487fe27dad566bdbe5ed50c160156d39. These observations prove read-path availability at their timestamps, not the installed worker or active-payload Git identity. No production write, installation, restart or device test was performed by this engineering task.


## Pinned development evidence

Implementation candidate `08f6d436870240df85bf4fddd5bd02b072925d81` (0.4.11) passed repository workflow 38461610646 and Windows workflow 38461610758. Windows evidence includes 119 full-suite tests, 16 native checks and real limited-account installation/restart/staging/deployment/rollback/recovery/uninstall checks. Artifact 11846107735 is bound to that commit; its outer ZIP SHA-256 is be6ac7e63489f527f5f50dc8c3da5043557855deb42ec14bfdc2f1085cce2997. No production commissioning is implied. Deferred profile cleanup registration is tested; the subsequent real reboot cleanup is still a retirement gate.

## TERMINAL preflight incident and correction (2026-10-13)

User-reported administrator output verified both artifact checksums, then 0.4.11 preflight stopped with `Unique current MCP payload path not established`. Read-only local task/process evidence identified active configuration `C:\ProgramData\SmartHome\WebCoRE\webcore-windows.yaml`, Node `C:\Program Files\nodejs\node.exe`, and active script `C:/SmartHome/staging/webcore-cli-0.4.10/windows-readonly-launcher.cjs`. The prior content-based discovery selected `webcore-windows.pre-0.4.10.yaml`, a backup referencing the legacy source. This corrects the earlier inferred active-payload layout; legacy vm_git_status still does not prove active runtime identity.

The reviewed launcher contains only strict mode, `WEBCORE_WINDOWS_MANAGEMENT_READONLY=enabled`, and `require('./server/index.js')`. Corrective PR #8 binds discovery to the task's actual single --config argument, verifies the running Node child, rejects stale backup substitution and unsupported wrapper code, preserves forward-slash/escaped/backslash pointer encoding, and catalogs the reviewed wrapper in baseline/candidate snapshots. Original unmanaged runtime-file verification allows unrelated documentation residue while preserving protected/hash checks on every snapshotted runtime file; managed payloads still enforce exact file sets. Windows CI now has direct and production-style wrapper layouts. The old staged 0.4.11 package is superseded for TERMINAL installation; do not modify its verified bytes or edit working production YAML to bypass preflight.

Passing corrected Windows evidence and a new pinned artifact are required before resuming installation. Reboot, rollback and end-to-end management acceptance on TERMINAL remain pending. Installation authorization does not certify those gates or authorize unrelated device actions.

## Corrected pinned development evidence

Corrective 0.4.12 candidate `bb236f550080f99453af2d27a2e8ab99c2317e60` passed repository workflow 38480287804 and Windows workflow 38480287737. Both Windows direct/wrapper jobs passed 22 native checks, actual limited-account installation and security tests, controlled restart, merged-source staging/deployment, prior-release rollback, byte-exact YAML recovery and scoped uninstall. There are 120 distinct repository tests; Windows full-suite logs show 240 passing executions per job because integration packaging leaves a duplicate suite under build/package. Wrapper artifact 11856144017 has outer ZIP SHA-256 `7c02075aa5f660cf81775b9d138915fa7d2463e135a31e7a73f48d77ed32234f`. Corrective PR #8 was merged with explicit approval as `9b15da31b9845883b03ac0fc2c0c61f66455d0c5`; independent compare confirms the tested candidate remains a main ancestor with no file delta. This supersedes the 0.4.11 installation candidate for TERMINAL. No installed or commissioned management boundary is claimed.

## Runtime permission preflight stop (2026-10-13)

User-reported 0.4.12 package checksum verification passed, but preflight stopped before provisioning with Unprotected management input. A read-only ACL inspection identified inherited Authenticated Users Modify on the active `C:\SmartHome\staging\webcore-cli-0.4.10` root/launcher and the existing tunnel-client v0.0.15 executable. Node had no reported foreign write finding. No installation, permission modification or service restart occurred.

Corrective implementation PR #9 (0.4.13) adds explicit administrator-only runtime permission hardening with protected metadata ACL backups, reduced foreign runtime write rights, ancestor replacement protection and unchanged unrelated descendant permissions. Default preflight/install do not repair permissions silently. New native runtime validation allows read-only access to public Node/tunnel/original-source code while continuing to reject all foreign writes; configuration, managed worker inputs and audit/recovery remain confidential. Global Node ACLs are not rewritten. Hosted Windows integration now reproduces writable inherited source, public executable readers and a replaceable parent. Passing final CI, corrective merge approval and explicit permission-hardening approval are required before resuming production commissioning.
