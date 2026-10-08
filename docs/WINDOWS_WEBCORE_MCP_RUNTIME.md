# Windows WebCoRE MCP production runtime and recovery record

**Evidence date:** 2026-10-07/08. **Status:** unattended read-path accepted by user; full operational hardening and predecessor retirement remain open in #23. This document supersedes the Mac-as-active-runtime diagram in the earlier architecture narrative for the current deployment only.

## Architecture and verified state

ChatGPT Business private WebCoRE plugin → OpenAI secure tunnel → Windows VM TERMINAL → tunnel-client v0.0.15 → webcore-CLI 0.4.9 MCP stdio → Hubitat WebCoRE and read-only Maker API. No inbound public Hubitat/WebCoRE exposure. The Mac is a temporary rollback/predecessor pending controlled retirement.

Windows baseline: QEMU Windows client VM, 8 logical CPUs, about 15 GB RAM, 249 GB C: volume, Node v24.19.0, npm 11.17.0, Git 2.55.0.windows.5. Source under `C:\SmartHome\webcore-CLI`; tunnel binary under `C:\SmartHome\tunnel-client\v0.0.15`. No npm dependencies are declared and no lockfile exists; `npm ci` is not applicable. Use `npm.cmd` in PowerShell when execution policy blocks `npm.ps1`; do not weaken policy. Syntax checks passed and 106/106 tests passed. MCP advertised 18 tools, 13 read-only and 5 write/action.

The tunnel-client Windows release was checked against its publisher SHA-256 list; the executable was unsigned. This is a documented provenance caveat, not a verified Authenticode signature.

## Startup and credential boundary

Task Scheduler task `SmartHome-WebCoRE-MCP`: startup trigger, SYSTEM service account, highest privileges, restart policy of 3 retries at one-minute intervals, action invoking tunnel-client `run --config` with the protected service YAML. Service files live under `C:\ProgramData\SmartHome\WebCoRE` with restricted SYSTEM/Administrators ACLs. Runtime key is held in a separate protected machine-local file referenced through the supported `file:` credential provider. This is plaintext at rest behind Windows ACLs, not a claim of encryption. Never print, commit, or screenshot credential contents.

webcore-CLI `server/config.js` computes config location as `join(process.env.XDG_CONFIG_HOME || join(homedir(), '.config'), 'webcore-toolkit')`. The service therefore needs machine-scoped `XDG_CONFIG_HOME=C:\ProgramData\SmartHome\WebCoRE` and `C:\ProgramData\SmartHome\WebCoRE\webcore-toolkit\config.json`. That JSON contains both WebCoRE and Maker API configuration. Use BOM-free UTF-8 when editing Node JSON: Windows PowerShell `Set-Content -Encoding UTF8` in this environment produced a BOM that broke `JSON.parse`. A BOMless .NET UTF8Encoding writer worked. Do not substitute Maker API URL for the WebCoRE dashboard endpoint in the setup wizard; the endpoints share similar URL shape but are different applications.

User-scoped `CONTROL_PLANE_API_KEY` was removed after service credential commissioning. Do not remove the protected SYSTEM service key until a replacement has passed acceptance.

## Evidence and important failure correction

1. Windows interactive tunnel worked, and Business ChatGPT successfully called the read-only Hubitat tool.
2. Closing the launching PowerShell killed the interactive process. Thus `runtimes connect` process mode alone did not meet Windows service requirements.
3. SYSTEM Task Scheduler launch showed result 267009 (running), a Session 0 process, and survived the first VM reboot.
4. The **first** post-reboot Business request reported WebCoRE/Hubitat not configured. Root cause: SYSTEM had a different home directory, so it could not load the user-profile WebCoRE config. A healthy tunnel process alone did not prove functional MCP downstream access.
5. Copied the working config into protected ProgramData, selected it via `XDG_CONFIG_HOME`, and restarted the task. Business ChatGPT reported Maker API 96 devices and WebCoRE 95 devices.
6. After a **second reboot**, with no Windows user logged in, the user reported a successful Business test of both WebCoRE status and Maker API inventory. This is the actual unattended end-to-end acceptance gate. Counts are from the prior live calls; do not assume the second test independently recounted every device unless evidence is captured.

## Open acceptance and cleanup

- #23: prove process-crash restart, duplicate process prevention, deterministic start/stop/status, health alerts, service logs, rollback, backup and recovery, and retire the Mac predecessor without losing rollback capability prematurely.
- Platform organization was named Kane Consulting; business-email owner invite failed in both browser session modes. Diagnose invite error with the provider without creating redundant organizations or weakening permissions. Existing ChatGPT Business owner membership is not equivalent to API Platform membership.
- Revoke an orphaned runtime API key and audit current Platform runtime key inventory. Do not revoke the active SYSTEM key.
- Remove old Mac tunnel client profile, credentials, autostart/recovery artifacts and obsolete payloads only after verified rollback plan; preserve unrelated Mac development tools and the status-bridge code.
- Verify the 96-versus-95 authorized-device difference if a complete inventory parity requirement is adopted; unequal counts are not inherently wrong.
- Historical log collector, JSONL retention, reconnect logic and backups remain uncommissioned (#25).
- Update architecture diagrams and deployment/recovery runbooks to reflect Windows as active runtime. Do not declare full no-dust completion until that is done.
