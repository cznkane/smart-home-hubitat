# WebCoRE MCP: Windows release, Business plugin discovery, and chat acceptance

**Status:** Detailed operational companion to `docs/WEBCORE_MCP_RELEASE_DEPLOYMENT_RUNBOOK.md`.  
**Prepared:** 2026-10-13. **Current incident:** v0.4.10 server and Business plugin show 22 tools, but new ChatGPT chats expose 17 or 18 and cannot call four new VM tools. **Do not label this deployment accepted until the calls succeed.**  
**Authority:** `CHATGPT_INIT.md`, `docs/SMART_HOME_OPERATING_PROTOCOL.md`, `docs/WEBCORE_MCP_RELEASE_DEPLOYMENT_RUNBOOK.md`, `docs/WINDOWS_WEBCORE_MCP_RUNTIME.md`, `docs/CHATGPT_WEBCORE_MCP_ARCHITECTURE.md`. Read these first. If a conflict exists, the canonical protocol and newer verified runtime evidence prevail.

## 0. The problem this runbook prevents

A local MCP server can return the expected tools while ChatGPT still exposes a previous inventory. **Do not conflate:** Git source; tested release; staged payload; running Node child; independent MCP `tools/list`; tunnel connectivity; Business plugin Admin discovery; enabled tool toggles; plugin installation/availability; per-conversation tool exposure; successful invocation. Each is an independent gate with its own evidence.

Historical incident: v0.4.9 introduced Hubitat Maker API tools; Business Admin showed 18 while an existing chat did not show the new tools. On 2026-10-13, v0.4.10 introduced four read-only VM diagnostics; Business Admin shows 22 with all four individually enabled, but multiple new chats still show 17/18. **No verified root cause or repair of this last discrepancy is recorded yet.** Do not claim a refresh, restart, or new chat alone fixed it. Record the exact eventual resolution here.

## 1. Required roles, safety, and evidence

- Operator: Windows VM `TERMINAL`; ChatGPT Business workspace; GitHub `cznkane/webcore-CLI` (source), `cznkane/smart-home-hubitat` (canonical operations).
- Before consequential instructions, complete `CHATGPT_INIT.md` initialization and all required canonical reads.
- One command/action per turn with **Do / Expect / Stop if / Next**. `go` confirms the immediately preceding expected result **as user-reported**, not independently verified. Do not re-ask the same checkpoint.
- Never expose credential-bearing tunnel YAML, access URLs, secrets, token-bearing command lines, enrollment keys, or protected config contents in chat/screenshots/logs.
- Read-only investigation before modification. Do not restart a healthy tunnel, loosen permissions, delete/recreate a plugin, or redeploy Windows to repair a chat-tool discrepancy.
- Track **PROVEN / NOT PROVEN / CHANGED / ROLLBACK / CLEANUP** with timestamp, workspace, actor, and evidence.
- All writes to production require the canonical change-control/approval gates; a saved Admin tool inventory is not authorization to change device automation.
- Screen captures of Admin views must be reviewed for secrets before sharing.

## 2. Gate ledger template (copy into each release record)

| Gate | Evidence required | Result / timestamp |
|---|---|---|
| A Source | GitHub commit/tag, branch, reviewed diff | |
| B Manifests | `package.json`, `plugin.json`, `.codex-plugin/plugin.json` agree | |
| C Tests | `npm run check` and `npm test` exit 0, counts recorded | |
| D Payload | Exact versioned release path and files | |
| E Runtime | Running child process command/path, version, one intended instance | |
| F MCP protocol | Independent `initialize` and `tools/list` count/names/annotations | |
| G Tunnel | Task/process connected to intended child/config; watchdog status | |
| H Business Admin | Correct plugin/workspace, refreshed and **saved** inventory; tool toggles and read/write classification | |
| I Installation | Plugin enabled and available to intended user; policy/connection errors noted | |
| J Chat exposure | New Business chat, plugin explicitly selected, count and exact names visible | |
| K Calls | Newly added tools **actually invoked** with successful real results | |
| L Closure | Rollback classified, residue cleaned, Git documentation updated | |

**Stop at the first failed gate.** Do not replay already proven lower gates without new contrary evidence.

## 3. Release and Windows deployment (only when the source/runtime actually needs updating)

1. Inspect Git branch, clean/dirty state, source commit and GitHub canonical HEAD. Inspect all three version manifests. Record reviewed release diff and expected tool delta.
2. Run `npm run check` then `npm test` in the intended release checkout. Record exit codes and complete test totals. Do not deploy on a failed test.
3. Stage the immutable versioned payload. On `TERMINAL`, use version-specific paths and avoid overwriting a known-good release. For 0.4.10, staging path used: `C:\SmartHome\staging\webcore-cli-0.4.10`; **this directory is ACTIVE, not disposable staging, while production points to it**.
4. Independently launch a temporary MCP stdio child with the same Node execution/feature flag as production; send `initialize` and `tools/list`. Verify server identity, version, tool count, exact new names and annotations. Terminate temporary child; do not leave duplicate services.
5. Inspect Windows Task Scheduler task `SmartHome-WebCoRE-MCP` (SYSTEM) and `SmartHome-WebCoRE-Watchdog`, running tunnel-client v0.0.15, production config reference, and live child process path. Never print credential-bearing YAML.
6. Before an approved cutover, make a byte-verified, ACL-preserving config backup and validate a candidate with `tunnel-client doctor`. Coordinate watchdog suspension only for the approved maintenance window; stop MCP task, verify old child gone, switch candidate, restore ACL, start MCP task, verify one intended Node child, then re-enable watchdog. Each operation is its own user-confirmed gate. Preserve the previous 0.4.9 checkout as rollback.
7. Independently call WebCoRE status through the connector; verify connectivity, hub snapshot, plugin version. Do not infer the new VM tools are ChatGPT-exposed from this result.
8. If any lower gate fails, use the documented rollback with explicit approval; otherwise **do not disturb production**.

### 0.4.10 recorded deployment evidence (not current-live proof)

- Release commit `b69e625006ee8a48c680a679be6c376fa2cac611`; prior production v0.4.9 commit `e8eceeed487fe27dad566bdbe5ed50c160156d39`.
- 0.4.10 independent MCP protocol audit returned 22 tools, including `vm_status`, `vm_scheduled_tasks`, `vm_processes`, `vm_git_status`; pre-cutover tests reported 114/114 passing.
- Opt-in feature flag `WEBCORE_WINDOWS_MANAGEMENT_READONLY=enabled` was scoped to version-specific launcher `C:\SmartHome\staging\webcore-cli-0.4.10\windows-readonly-launcher.cjs`; not a machine-wide environment change.
- Original config backup `C:\ProgramData\SmartHome\WebCoRE\webcore-windows.pre-0.4.10.yaml` preserved with matching hash/ACL. Do not show file contents.
- Post-cutover independent `webcore_status` returned connected, dashboard confirmed, snapshot from hub, plugin version 0.4.10. Watchdog re-enabled, user-reported.
- Admin UI screenshots on 2026-10-13 showed **22 tools**, **17 read tools**, all four `vm_*` toggles ON, `Allow read tools`, `Enable all new tools`, and disabled `Save changes` button (no pending changes). Plugin marked Enabled. Another Admin screen displayed `Unable to load installation policy` under Availability; this is an **unresolved clue**, not proven cause.
- New Business chats reported **17 or 18 exposed tools**, zero `vm_*`. Therefore **Gate J/K failed**. No VM diagnostic calls were executed; do not mark release complete.

## 4. Business plugin discovery and installation: mandatory exact sequence

1. Identify the **Business** workspace, not Personal. Verify the exact WebCoRE plugin by title, catalog/developer, and intended tunnel binding. A plugin display version such as 1.0.0 is **not** the MCP server version 0.4.10.
2. In Business Admin → Plugins → WebCoRE, open **Tools**. Click **Refresh** only if the server's advertised inventory has changed or Admin is stale. Count tools and verify each new exact name and its read-only annotation.
3. Verify **each new tool's toggle is ON**. Verify read-tools group enabled; retain `Allow read tools` permission policy. Do not use `Allow all tools` to conceal a classification issue.
4. If the tool settings changed, click **Save changes** and wait for confirmation. If **Save changes** is disabled and toggles are correct, there is no unsaved tool change; do not keep toggling or refreshing.
5. Inspect plugin Enabled state, **Availability/installation policy**, and whether the user is actually entitled/installed. Record any `Unable to load installation policy` error separately; use **Try again** once for read-only retry if appropriate, and record outcome. Do not infer a causal relationship without evidence.
6. Confirm correct plugin is selected in the new Business chat, via plugin picker or @ mention where supported. OpenAI's public Plugins guidance documents direct plugin selection; it does not guarantee that an Admin inventory automatically propagates to all chats.
7. Run **one** new-chat acceptance test. If it fails, **STOP repeating prompts** and investigate the discrepancy with captured evidence.
8. Do not uninstall/recreate/re-enroll or weaken workspace security without a reviewed recovery plan and explicit approval.

## 5. Copy/paste fresh-chat acceptance prompt

```text
WebCoRE MCP v0.4.10 — production read-only acceptance.
Use the WebCoRE plugin connected to this Business workspace.
Report the exact WebCoRE tool count exposed to THIS chat and whether vm_status,
vm_scheduled_tasks, vm_processes, and vm_git_status are available.
If all four are exposed, invoke each and report actual read-only results.
No configuration changes, device actions, restarts, or simulated output.
If any is missing, stop and report count, exact missing names, workspace,
and whether WebCoRE was selected. Do not recommend redeploying Windows.
```

Success requires **four real tool calls** plus plausible bounded results. An assistant's statement that the tools exist, an Admin screenshot, or a `go` response is not proof of actual invocation.

## 6. Failure tree: Admin shows 22, chat shows 17/18

**This is the active 2026-10-13 failure mode.**

- **Local MCP 22?** Yes → do not change Node feature flag, launcher, Git checkout or tunnel.
- **Business Admin 22?** Yes → do not refresh repeatedly.
- **Four toggles ON and saved?** Yes, screenshots show ON and no pending Save → do not toggle repeatedly.
- **Chat is in Business workspace and explicitly selects WebCoRE?** Verify this exact boundary once. If not, correct selection and retest once.
- **Plugin Enabled and installation policy loadable?** The Admin Availability error is unverified. Inspect the policy/installation layer and workspace entitlement; do not assume the error is harmless or causal.
- **Same tool inventory in different new chats?** 17 versus 18 is a real discrepancy to preserve; ask for exact tool names and workspace/surface, not just totals.
- **Tool names present but approval requested?** That is permissions/approval, **not** missing registration. Keep read-only permission policy.
- **Tools missing after correct workspace/plugin selection?** Treat as ChatGPT-side plugin installation/tool-exposure or cached-schema incident. Gather sanitized Admin tool list, new-chat tool inventory, plugin identity/version, time, workspace type, and installation-policy error. Escalate to workspace/platform support with this reproducible evidence. Do not claim cache as proven root cause.
- **Possible browser/session fault?** A hard refresh/sign-out or separate browser can be an optional, low-risk discriminating test **after** recording evidence, not an endless ritual or proof of repair. Do not clear credentials/cookies without user approval.
- **Do not re-run fresh-chat acceptance after each guess.** Only retest after a specific verified change at the failing layer.

### Support evidence template

```text
Date/time/time zone:
Workspace: ChatGPT Business (avoid sensitive IDs)
Plugin: WebCoRE (plugin display version and active/installed status)
MCP server: webcore-cli 0.4.10, 22 tools via independent tools/list
Business Admin: 22 discovered, 17 read, four vm_* enabled, no pending save
Availability policy: "Unable to load installation policy" (if still present)
Conversation: new Business chat, plugin explicitly selected (yes/no)
Chat-exposed tools: 17 or 18; four vm_* absent
Actual invocation: 0/4; not an execution failure
Tunnel/runtime: healthy; do not restart
Expected: 22 tools and four callable VM read-only diagnostics
Actual: 17/18 exposed, four absent
Actions already tried: Admin refresh/save; multiple new chats; no fix
Sensitive info removed from screenshots/logs: yes
```

## 7. Completion and postmortem requirement

Only close deployment after Gate K succeeds: `vm_status`, `vm_scheduled_tasks`, `vm_processes`, `vm_git_status` each returns real, bounded read-only output from a new Business chat. Verify watchdog remains enabled; classify 0.4.10 path ACTIVE, 0.4.9 ROLLBACK, temporary files RETIRE/INVESTIGATE; do not delete active `staging` path. Update the canonical retained context and runtime record with final evidence, dates, exact discovered root cause, fix and proof. If still blocked, record status as **deployment running, acceptance blocked**.

**Postmortem mandatory:** When this incident is resolved, append the **exact UI action or platform change that actually fixed chat exposure**, screenshots or nonsecret evidence, whether the installation-policy error mattered, before/after tool counts, and a single clean deployment checklist that incorporates the proven remedy. Do not turn speculation into a permanent runbook instruction.

## 8. Sources and boundary notes

- Canonical: `CHATGPT_INIT.md`; `docs/SMART_HOME_OPERATING_PROTOCOL.md`; `docs/WEBCORE_MCP_RELEASE_DEPLOYMENT_RUNBOOK.md`; `docs/SMART_HOME_RETAINED_CONTEXT.md`; `docs/WINDOWS_WEBCORE_MCP_RUNTIME.md`; `docs/CHATGPT_WEBCORE_MCP_ARCHITECTURE.md`.
- OpenAI public help: [Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt), [Managing app permissions](https://help.openai.com/en/articles/20001495-managing-app-permissions-in-chatgpt), [Troubleshooting ChatGPT error messages](https://help.openai.com/en/articles/7996703-troubleshooting-chatgpt-error-messages).
- The public help documents plugin selection and workspace availability; it does **not** prove why this particular 22-to-18 exposure discrepancy occurs. Preserve this uncertainty.

## 9. 2026-10-13 acceptance update — passed, resolution mechanism unproven

After the Admin screenshots showed 22 registered tools (17 read) and all four `vm_*` toggles ON, a subsequent new Business chat reported **22/22 exposed and 4/4 VM operations invoked successfully**. This is user-provided transcript evidence, not a tool call made by the author of this documentation. All four reported `read_only: true`.

| Diagnostic | Observed result |
|---|---|
| `vm_status` | `TERMINAL`, Windows 11 Pro, 14.9 GiB total / 9.0 GiB available memory, 164.0 GiB free system drive |
| `vm_scheduled_tasks` | `SmartHome-WebCoRE-MCP` Running, last result `267009`; `SmartHome-WebCoRE-Watchdog` Ready, last result `0` |
| `vm_processes` | `node.exe` PID 6476 PPID 10492; `tunnel-client.exe` PID 15472 PPID 1576; `node.exe` PID 15820 PPID 15472 |
| `vm_git_status` | Branch `main`, commit `e8eceeed487fe27dad566bdbe5ed50c160156d39`, clean tree, 0 changed files |

**Acceptance:** tool exposure and four read-only diagnostic calls PASS. Resource/process/task presence and clean Git state PASS within their diagnostic scope. **Not independently proven:** whether the nonzero MCP task last result `267009` indicates a failure; remote Git synchronization; end-to-end application responsiveness from these four diagnostics alone. Previous separate `webcore_status` evidence did establish connected v0.4.10 service.

**Git path interpretation:** `vm_git_status` reports the retained `C:\SmartHome\webcore-CLI` checkout at v0.4.9 commit; active v0.4.10 launcher is in `C:\SmartHome\staging\webcore-cli-0.4.10`. This is consistent with the documented rollback arrangement, but the diagnostic output alone does not certify the active checkout's Git status. Do not alter the old checkout just to change this report.

**Crucial unresolved postmortem point:** the precise event that caused ChatGPT exposure to transition from 17/18 to 22 is **not verified**. The operator had refreshed/saved Admin tools, inspected all toggles, and deleted failed prompts before a successful fresh-chat audit. This sequence is a timeline, **not proof** that deleting prompts, saving Admin configuration, or a cache expiration was the fix. Future releases must use the deterministic gate checks above and record any confirmed platform behavior. No further refresh/redeploy is justified solely by this now-passing gate.

**Remaining closure:** verify stable operation as needed; classify v0.4.10 active path, v0.4.9 rollback, config backups and temporary files; update canonical runtime/retained context; merge this documentation PR after review. Do not delete the active v0.4.10 directory because it is named `staging`.

## 10. 2026-10-13 release closure: two temporary YAML files retired

Operator provided PowerShell output showing the scheduled task `SmartHome-WebCoRE-MCP` launches `C:\SmartHome\tunnel-client\v0.0.15\tunnel-client.exe run --config C:\ProgramData\SmartHome\WebCoRE\webcore-windows.yaml`. Four config hashes were checked: active `webcore-windows.yaml` and `webcore-windows.0.4.10.final.yaml` both `62FA8791A599A89C584BC9E284D11D6C5450F1563CA2208F9DB2391E3C4D56B6`; candidate `2BDD3599198E987F604AE47F18B5B2B5A49A678C519C9513D8632CEB8BEA39C4`; pre-0.4.10 backup `DFBC807670459E48A8282600BFA75C0D8538C1C9172830C35C1856E4E222E735`. No file contents or secrets were read.

A guarded `Remove-Item -WhatIf` dry run named exactly two cleanup targets. After explicit operator go-ahead, a guarded real deletion returned:

```text
Removed: webcore-windows.0.4.10.candidate.yaml
Removed: webcore-windows.0.4.10.final.yaml
```

**Post-cleanup independent connector verification:** `webcore_status` returned `connected: true`, `dashboard_confirmed: true`, `plugin_version: 0.4.10`. `vm_scheduled_tasks` returned MCP Running (last result `267009`) and watchdog Ready (last result `0`). `vm_processes` returned `tunnel-client.exe` PID 15472 with child `node.exe` PID 15820, plus separate `node.exe` PID 6476. The tool calls were read-only. The removal itself is operator-reported output, not an independent post-deletion filesystem listing.

**Artifact disposition:** `C:\SmartHome\staging\webcore-cli-0.4.10` ACTIVE (preserve despite `staging` name); `C:\SmartHome\webcore-CLI` v0.4.9 ROLLBACK (preserve); `webcore-windows.yaml` ACTIVE; `webcore-windows.pre-0.4.10.yaml` ROLLBACK; candidate/final copies RETIRED; watchdog scripts, state/log files, `runtime.key`, `gmail-smtp.bin`, and toolkit preserved. No other files were removed.

**Closure:** v0.4.10 production deployment and 22/22 tool / 4/4 VM diagnostic acceptance complete; approved temporary-YAML cleanup complete, with successful post-cleanup service checks. Remaining nonblocking uncertainties: exact cause of earlier ChatGPT tool exposure delay, significance of scheduled-task last-result code `267009`, and whether a separate Node process is expected. Do not describe those as proven faults or solved root causes. No further service restarts or deletions warranted by current evidence.
