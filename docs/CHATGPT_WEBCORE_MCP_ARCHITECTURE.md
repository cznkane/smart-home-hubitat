# ChatGPT ↔ WebCoRE MCP Architecture

**Status:** Operational WebCoRE and direct Hubitat read paths; write workflow pending acceptance test; known Business read-approval anomaly  
**Decision owner:** CIO / CTO operating model  
**Last updated:** 2026-10-07

## Objective

This implementation is also intended to become a **repeatable deployment pattern** that can be reproduced for other Hubitat/WebCoRE environments and potentially offered as a professional service. Documentation therefore needs to be sufficient for a clean-room deployment by a competent technician who was not present for the original build.

The acceptance test is not merely “ChatGPT can connect to WebCoRE.”

The target operating experience is a request such as:

> Kids Away was ON and School Mornings fired anyway because AndieEffective was true. Fix it.

ChatGPT should then be able to inspect the live pistons, relevant variables/devices and execution logs; determine the root cause and blast radius; prepare the smallest appropriate change; present the proposed change for approval; apply it after approval; verify the stored piston read-back; and record the change.

The user should not have to act as a human API by repeatedly supplying screenshots or manually translating changes into WebCoRE.

## Canonical Smart Home operating protocol

All Smart Home work is governed by [`docs/SMART_HOME_OPERATING_PROTOCOL.md`](./SMART_HOME_OPERATING_PROTOCOL.md).

That protocol is project-wide and applies across chats. It defines the standing CIO/CTO roles, context color coding, instruction syntax, security and screenshot handling, completion gates, WebCoRE change control, Git discipline, cleanup/no-dust rule, recovery expectations, response behavior, and definition of done.

Where a procedural note in this architecture document conflicts with the operating protocol, the operating protocol governs unless Rick explicitly overrides it or this architecture document records a newer deliberate project decision.

## Documentation standard / repeatability requirement

For every material installation or architecture step, record:
- purpose and rationale
- official source/documentation URL
- prerequisites and supported versions
- exact package/tool installed and version
- install command or procedure
- resulting executable/config/data paths
- permissions and security implications
- credentials required, but never credential values
- validation command and expected result
- rollback/uninstall procedure
- stale-artifact cleanup procedure
- known failure modes and troubleshooting notes
- CTO risk score and rationale
- date tested and platform/architecture tested

Where practical, separate **environment-specific values** from the reusable procedure so the same runbook can be used for another customer without copying identifiers or secrets. The desired end state is an install/runbook that is reproducible, supportable, auditable, and suitable for controlled client deployments.

## Architectural configuration

```text
ChatGPT Business
    |
    v
Private custom MCP plugin: WebCoRE
    |
    v
OpenAI Secure MCP Tunnel
    |
    v
Mac on trusted/private network
    |
    v
webcore-CLI MCP server (stdio, Node.js 24+)
    |
    v
Hubitat-hosted WebCoRE
    |
    v
Hubitat devices / automations
```

Supporting control plane:

```text
GitHub (this repository)
    |
    +-- canonical code
    +-- architecture and decisions
    +-- operational/runbook documentation
    +-- piston archive/history
    +-- change history / rollback evidence
```

SharpTools remains the presentation/dashboard layer. Hubitat remains the device/platform layer. WebCoRE remains the automation engine.

## Design origin and durable lessons

The direct ChatGPT ↔ WebCoRE effort originated from a practical development problem: screenshot-driven troubleshooting made Rick act as the transport layer between ChatGPT and the live automation system. The desired loop was to let ChatGPT inspect piston definitions, variables, logs, and selected device state directly, then progress from read-only diagnosis to controlled execution and finally approval-gated edits.

The original architectural proposal established several principles that remain valid in the commissioned system:
- keep Hubitat and WebCoRE off the public Internet; use a secure intermediary/tunnel rather than inbound exposure
- start with read-only inspection and prove observability before enabling action/write paths
- expose only deliberately authorized devices/capabilities rather than treating Hubitat as an unrestricted remote-control surface
- separate read access, piston execution/live tests, and persistent edits into different risk/approval classes
- preserve backups/version history and verify read-back after writes; a successful save is not behavioral proof
- prefer existing WebCoRE representations and supported tooling over inventing a parallel piston model
- make direct inspection of piston definitions, variables, device state, and execution logs the normal diagnostic path so Rick is not the human API

The early concept of a bespoke LAN "Smart Home bridge" and direct use of WebCoRE external execution URLs was **superseded** by the audited `webcore-CLI` MCP server plus OpenAI secure MCP tunnel. WebCoRE external execute URLs contain credentials and remain secrets; they are not the ChatGPT-facing integration contract.

The staged capability model survives in the current change-control policy: autonomous/read-only inspection first; action-producing live tests and persistent writes remain separately controlled and require explicit approval under the operating protocol.

## Decisions and rationale

### ChatGPT Business, separate workspace

A ChatGPT Business workspace was created because the required custom MCP / Developer Mode / private tunnel workflow is exposed there. The existing Personal workspace is intentionally kept separate during implementation. No Personal-to-Business merge will occur until the integration is proven and there is a separate reason to merge.

### Private tunnel, not public exposure

The custom MCP plugin will use the OpenAI Tunnel connection option rather than a public Server URL.

Hubitat and the local WebCoRE MCP service are not to be exposed directly to the public Internet. No inbound firewall/port-forwarding exception should be created for this project unless the architecture is explicitly revisited.

### Official tunnel client

An OpenAI Platform tunnel was created and associated with the intended Business workspace. The official OpenAI tunnel client repository/release path was identified:
- Repository: https://github.com/openai/tunnel-client
- Releases: https://github.com/openai/tunnel-client/releases

The target Mac reports `arm64`.

A manual Darwin ARM64 ZIP was initially downloaded and its SHA-256 was verified successfully against the publisher-provided checksum. macOS Gatekeeper then blocked the unnotarized binary. The binary was temporarily approved with “Open Anyway” and its CLI/help output was inspected.

This path was then deliberately abandoned after reviewing OpenAI's current macOS guidance, which identifies Homebrew as the supported installation path and warns against bypassing Gatekeeper for the unnotarized ZIP distribution.

Rollback was completed and verified: the ZIP, extracted tunnel-client runtime binary, bundled `cloudflared`, manifest, license files, and SPDX metadata were removed from `~/Documents/Codex/WebcoreCode`. The pre-existing `WebCoRE_Status_Bridge.groovy` file remained intact.

Current installation strategy: use Homebrew and install the official OpenAI formula `openai/tools/tunnel-client`.

### webcore-CLI

The audited WebCoRE MCP implementation is `Cruxad0/webcore-CLI`; an inspection fork exists as `cznkane/webcore-CLI`.

Observed design safeguards include:
- local credential storage rather than chat-based credential handling
- no npm package dependencies in the reviewed release
- Node.js 24+ requirement
- piston/device/log inspection
- draft validation against live authorized devices/commands
- prepare/diff/approval/apply workflow
- remote hash/change detection before apply
- read-back verification after persistence
- separate authorization for live piston execution
- no delete or force-save tools
- no blind retry of an accepted-but-unverified write

Production installation should use a pinned/auditable release rather than casually running an unpinned development branch.

### Homebrew on the bridge Mac

Homebrew was installed successfully on 2026-10-06 using the official installer from https://brew.sh/.

Observed installation details:
- Apple Silicon install prefix: `/opt/homebrew`
- PATH integration file created by the installer: `/etc/paths.d/homebrew`
- Installer-directed shell initialization target: `~/.zprofile`
- Homebrew documentation: https://docs.brew.sh
- Homebrew analytics documentation: https://docs.brew.sh/Analytics
- Homebrew reports anonymous aggregate formula/cask analytics are enabled by default; opt-out remains available per the published analytics documentation.

The Homebrew installation itself completed successfully. Before installing tunnel-client through Homebrew, PATH initialization and `brew --version` should be verified in the active shell.

### Local terminal quality-of-life configuration

The Mac uses zsh. A native colored prompt was added to `~/.zshrc` to visually separate prompt context from command output without adding a shell framework or plugin dependency.

Prompt intent:
- user/host in cyan
- current directory in yellow
- prompt symbol in green
- command output in the terminal's normal foreground color

This is cosmetic only and is reversible by removing the added `PROMPT=...` line from `~/.zshrc`.

### GitHub is the engineering system of record

This repository is the canonical engineering record for the smart-home integration. It should contain architecture, runbooks, important decisions, code, current-state piston material where practical, and change/rollback history.

Live WebCoRE remains the runtime truth for current execution state. Git records what we intended, changed, and approved.

## Security rules

Never place the following in chat, screenshots, Git, issue text, commit messages, or documentation:
- API keys or access tokens
- tunnel credentials/enrollment secrets
- WebCoRE execute URLs containing access tokens
- WebCoRE dashboard password/PIN
- authentication codes
- commands with embedded credentials
- other reusable secrets

Avoid unnecessarily sharing internal identifiers such as Organization, Workspace, Project, Tunnel, and internal User IDs.

Secrets required by webcore-CLI are entered locally on the Mac and remain in its local configuration.

### Screenshot protocol

Before requesting an infrastructure/admin screenshot, ChatGPT must predict likely sensitive fields and explicitly say what must not be visible.

After an infrastructure/admin screenshot is uploaded, score it:
- 🟢 Clean: no concerning sensitive material
- 🟡 Caution: internal/non-secret information visible; limit distribution
- 🟠 Sensitive: information should have been cropped/redacted
- 🔴 Secret exposed: credential/key/token/password or equivalent; immediately identify required containment/rotation without reproducing the secret

## Engineering / creative-direction score

Architecture and implementation proposals should receive a CTO risk score in addition to normal technical analysis:

- 🟢 **Sound**: supported, maintainable, secure, recoverable; low fragility
- 🟡 **Watch**: acceptable but has a known dependency, workaround, beta edge, or operational burden
- 🟠 **Fragile**: meaningful security/maintenance/recovery risk; proceed only with an explicit reason and mitigation
- 🔴 **Out of bounds**: unacceptable security exposure, destructive/recovery risk, unsupported architecture, or technical debt that should not be introduced

The score evaluates the *direction*, not whether an individual step happened to work. A clever solution that makes the user the human API, bypasses change control, exposes private infrastructure, or creates brittle hidden dependencies should be challenged even if technically possible.

When useful, state the dominant reason alongside the score, for example:
`🟡 Watch — beta tunnel dependency; architecture is otherwise sound.`

## Change-control model

Default posture:
1. Read/inspect live state.
2. Diagnose root cause and identify blast radius.
3. Prepare the smallest appropriate change.
4. Present a concise change summary/diff and risk score.
5. Obtain approval before live writes.
6. Apply through webcore-CLI safeguards.
7. Verify stored read-back/hash.
8. Distinguish persistence verification from behavioral verification.
9. Record material architectural/code changes in Git.
10. Observe the next relevant real-world execution when behavior cannot be fully proven synthetically.

Live-test/device-affecting operations remain separately authorized.

## Historical implementation checkpoint (2026-10-06, pre-commissioning)

> Historical only. This checkpoint and the following next-session runbook capture the implementation plan before the MCP path was commissioned. They are retained as design history and must not be used as current-state instructions. The later 0.4.8/0.4.9 deployment sections and `SMART_HOME_RETAINED_CONTEXT.md` supersede this checkpoint for current state.

Completed:
- ChatGPT Business workspace created.
- Personal workspace retained separately.
- Developer Mode enabled.
- Private custom MCP creation UI confirmed.
- Tunnel connection option confirmed.
- OpenAI Platform tunnel created and associated with the intended workspace.
- Official OpenAI tunnel-client repository/release location identified.
- Target Mac architecture confirmed as `arm64`.
- Manual ZIP path tested, Gatekeeper exception encountered, and unsupported ZIP approach fully rolled back.
- Homebrew installed successfully from https://brew.sh/ using the official installer.
- Homebrew installed under `/opt/homebrew` with `/etc/paths.d/homebrew` PATH integration.
- Native zsh prompt customization added to `~/.zshrc` for readability.
- Screenshot security scoring and proactive redaction procedure adopted.
- CTO direction/risk scoring adopted.

Not yet completed:
- Verify the installed tunnel-client and matching `cloudflared` versions/paths.
- Connect/enroll the Mac to the existing tunnel.
- Confirm/install Node.js 24+.
- Install a pinned webcore-CLI release.
- Configure WebCoRE credentials locally.
- Prove local read-only status/diagnostics and piston access.
- Bind the tunnel to the local stdio MCP service.
- Create/publish the private WebCoRE MCP plugin in the Business workspace.
- Generate the WebCoRE plugin icon (256×256+ PNG, under the UI's 10 KB limit).
- Establish conservative plugin permissions.
- Perform read-only acceptance testing against a known piston.
- Perform first approved prepare/apply/read-back test.
- Exercise the real acceptance case around Kids Away / School Mornings / effective presence.

## Next-session runbook

1. Finish Homebrew shell-path initialization exactly as instructed by the installer.
2. Verify `brew --version` and `which brew`.
3. Install the official OpenAI formula: `brew install openai/tools/tunnel-client`.
4. Verify `tunnel-client --version`, executable path, bundled/matching `cloudflared`, and supported profile/onboarding commands.
5. Connect it to the already-created tunnel; keep enrollment/runtime credentials local.
6. Verify Node.js version and install/upgrade to 24+ if required.
7. Install/pin the reviewed webcore-CLI release.
8. Run local WebCoRE setup. Enter the execute URL/token and dashboard password locally only.
9. Run read-only `status` / `diagnose`.
10. List/pull a known piston and verify it against the known current state.
11. Connect the tunnel client to the webcore-CLI stdio MCP process.
12. Create the private WebCoRE custom MCP plugin using the tunnel.
13. Create/compress the plugin icon and publish with conservative access.
14. From ChatGPT Business, prove live read-only inspection.
15. Only then test an approved write through prepare → diff → approval → apply → read-back verification.

## Acceptance scenario

The integration is mature when the user can report an operational symptom in natural language, for example:

> Kids Away was on and School Mornings fired this morning anyway due to AndieEffective being true. Fix it.

ChatGPT should independently gather the relevant live evidence, explain the root cause, distinguish whether the defect belongs in School Mornings or upstream occupancy/effective-presence logic, inspect dependencies, propose the smallest robust fix, obtain approval, apply and verify it, and document the material change.

A second known acceptance scenario is cancellation/control of queued WebCoRE work: pausing School Mornings did not stop an already queued 30-minute fade. The mature design should include a deliberate kill/cancel strategy for pending work rather than relying on piston pause as an emergency stop.


## Installation / rollback log

### 2026-10-06

- Confirmed Mac architecture with `uname -m`: `arm64`.
- Downloaded OpenAI tunnel-client Darwin ARM64 runtime ZIP from the official GitHub release page.
- Verified SHA-256 successfully before execution.
- Extracted package contents and inspected the runtime CLI.
- macOS Gatekeeper blocked the unnotarized manual binary.
- A scoped “Open Anyway” exception was used temporarily for inspection.
- Reviewed current OpenAI macOS guidance and changed direction to the supported Homebrew installation path.
- Removed all extracted/downloaded OpenAI runtime artifacts from `~/Documents/Codex/WebcoreCode`.
- Verified only pre-existing local project artifacts remained in that directory, aside from normal macOS `.DS_Store` metadata.
- Installed Homebrew successfully from https://brew.sh/.
- Homebrew reported install prefix `/opt/homebrew` and created `/etc/paths.d/homebrew`.
- Installer requested `~/.zprofile` initialization commands; these were completed and verified.
- Verified Homebrew version: `7.0.8`.
- Verified active Homebrew executable: `/opt/homebrew/bin/brew`.
- Installed the official OpenAI `openai/tools/tunnel-client` Homebrew formula successfully.
- Post-install verification: `tunnel-client --version` reports `0.0.14+0f870e50a973fa820d4c409000059e181e8d242b` (git SHA `0f870e50a973fa820d4c409000059e181e8d242b`).
- Homebrew package version: `tunnel-client 0.0.14`.
- Executable path: `/opt/homebrew/bin/tunnel-client`.
- Added a native zsh colored prompt to `~/.zshrc` for improved prompt/output readability.


### Verified tunnel-client command surface (Homebrew 0.0.14)

The installed full client identifies itself as “Tunnel client for the OpenAI MCP control plane” and states that it connects a local/private MCP server to the OpenAI control plane over an outbound tunnel. It also exposes local operator endpoints `/healthz`, `/readyz`, and `/ui` while running.

Verified top-level commands:
- `admin`
- `admin-profiles`
- `cloudflared`
- `codex`
- `completion`
- `dev`
- `doctor`
- `health`
- `help`
- `init`
- `profiles`
- `run`
- `runtimes`

Verified agent-first help topics include `doctor`, `oauth`, `plugin`, `quickstart`, `samples`, and `troubleshooting`.

Canonical URLs emitted by the installed client:
- Tunnels management: https://platform.openai.com/settings/organization/tunnels
- Runtime API keys: https://platform.openai.com/settings/organization/api-keys
- Admin API keys: https://platform.openai.com/settings/organization/admin-keys
- ChatGPT connector settings: https://chatgpt.com/#settings/Connectors

Security note: these management pages may display internal identifiers or credentials. Do not capture/share screenshots containing API keys, tokens, tunnel secrets, Organization/Workspace IDs, or commands containing credentials.

### Quickstart-derived deployment rules

The installed `tunnel-client 0.0.14` quickstart was reviewed on 2026-10-06. The client explicitly recommends the supported tunnel-client path rather than ngrok or another ad hoc public tunnel.

For this WebCoRE architecture, the relevant target class is **local stdio MCP**. The documented initialization pattern is:

```text
tunnel-client init --sample sample_mcp_stdio_local --profile <profile-name> --tunnel-id <tunnel-id> --mcp-command "<local MCP command>"
```

Do not substitute environment-specific values into reusable documentation. Treat `<profile-name>`, `<tunnel-id>`, and `<local MCP command>` as deployment parameters.

The documented validation/start sequence is:
1. `tunnel-client doctor --profile <name> --explain`
2. `tunnel-client run --profile <name>` for an intentional foreground session.
3. For a long-lived managed local runtime, prefer `tunnel-client runtimes connect ...` rather than `nohup` or `disown`.
4. After managed connection, verify `tunnel-client runtimes status <alias>`. Do not declare deployment successful until the process is running and health/readiness are reported.

The daemon must remain running for ChatGPT connector discovery and subsequent MCP calls.

#### Credential and permission model

Keep control-plane duties separated:
- `CONTROL_PLANE_TUNNEL_ID`: non-secret tunnel identifier selected/created in tunnel management.
- `CONTROL_PLANE_API_KEY`: runtime credential used by `doctor` and `run`. Never commit or paste its value.
- `OPENAI_ADMIN_KEY`: administrative CRUD credential only. Do **not** give it to the long-lived daemon.

Least-privilege guidance from the installed client:
- runtime user/key principal: **Tunnels Read + Use**
- tunnel CRUD operator: **Tunnels Read + Manage**
- admin-key creation permission is separate

This deployment should use a dedicated runtime key for the daemon and avoid an Admin API key unless an explicit administrative operation requires one.

#### Additional canonical URLs from quickstart

- Organization roles: https://platform.openai.com/settings/organization/people/roles
- Organization groups: https://platform.openai.com/settings/organization/people/groups

### Local stdio sample profile, verified

The installed client's `sample_mcp_stdio_local` template was inspected on 2026-10-06.

Required initialization parameters:
- `--tunnel-id`
- `--mcp-command`

Optional initialization parameters:
- `--control-plane-base-url`
- `--control-plane-url-path`
- `--control-plane-api-key-ref`
- `--health-listen-addr`
- `--open-web-ui`

Behavior:
- stdio skips HTTP OAuth discovery because there is no PRMD endpoint
- the stdio command is bound to `channel=main`
- default control-plane base URL is `https://api.openai.com`
- runtime credential is referenced indirectly as `env:CONTROL_PLANE_API_KEY`, not embedded in the profile
- default health/operator listener is loopback-only `127.0.0.1:8080`
- admin UI does not open automatically by default
- default logging is JSON at info level
- MCP command is stored in the profile as the command used to launch the local MCP server

Representative reusable profile shape:

```yaml
config_version: 1
control_plane:
  base_url: "https://api.openai.com"
  tunnel_id: "<TUNNEL_ID>"
  api_key: "env:CONTROL_PLANE_API_KEY"
health:
  listen_addr: "127.0.0.1:8080"
admin_ui:
  open_browser: false
log:
  level: info
  format: json
mcp:
  commands:
    - channel: main
      command: "<LOCAL_MCP_COMMAND>"
```

Security/design consequence: the reusable profile may contain a tunnel identifier and local launch command, but the runtime API key should remain an environment reference. Never substitute a reusable secret into Git documentation.

For concurrent/clean-room runs, the sample recommends `127.0.0.1:0` plus a `url_file` so the selected local operator URL can be discovered without port collision.

### Profile initialization interface, verified

The `tunnel-client init --help` interface was inspected on 2026-10-06.

Important controls:
- `--profile-dir`: explicit profile-directory override
- `--profile`: profile name
- `--sample`: built-in sample to materialize; `--mcp-command` auto-selects the local-stdio sample
- `--tunnel-id`: tunnel identifier written to the generated profile
- `--mcp-command`: local MCP launch command
- `--control-plane-api-key-ref`: runtime-key secret reference, default `env:CONTROL_PLANE_API_KEY`
- `--health-listen-addr`: defaults to `127.0.0.1:8080`; `:0` requests an ephemeral runtime port
- `--open-web-ui`: enables automatic admin-UI browser opening
- `--force`: replaces an existing profile

Operational rule: do not use `--force` casually in deployment automation. Existing profiles should be inspected/backed up or intentionally retired before replacement.

The help output establishes that a profile directory can be explicitly controlled, but does not by itself identify the default profile filesystem location. Determine that from the profile-management interface or an actual sanitized initialization before documenting a default path.

### Profile management interface, verified

The `tunnel-client profiles --help` interface was inspected on 2026-10-06.

Available profile-management commands:
- `profiles add`: add a profile from a file or built-in sample
- `profiles edit`: edit a profile and validate it before saving
- `profiles list`: list configured profiles
- `profiles samples`: list/inspect built-in samples

A global `--profile-dir` override is supported. This help surface still does not state the default filesystem path, so the deployment documentation must not assume one until it is observed from the client itself.

### Default profile storage, verified

Running `tunnel-client profiles list` with no configured profiles reported the default profile directory as:

```text
~/.config/tunnel-client
```

On the commissioning Mac this resolves under the current user's home directory. The reusable documentation should use `~/.config/tunnel-client` rather than embedding a customer's username.

At the time of discovery, no tunnel-client profiles existed in that directory. This establishes a clean pre-initialization baseline.

Operational implications:
- include `~/.config/tunnel-client` in tunnel-client configuration backup/migration procedures
- inspect this directory during uninstall/offboarding and stale-profile cleanup
- do not assume profile files themselves contain runtime secrets; verify generated content before defining backup handling
- preserve file ownership/permissions when migrating profiles

### Node.js prerequisite baseline

The bridge Mac was checked before installing webcore-CLI:

```text
node --version  -> command not found
which node      -> node not found
```

No pre-existing Node.js runtime was present in the active shell. This is a useful clean-install baseline: Node.js must be installed before webcore-CLI can run. The reviewed webcore-CLI requires Node.js 24 or newer.

Node.js 24 was then installed with Homebrew using `brew install node@24` and verified successfully:
- Node runtime: `v24.21.0`
- Homebrew formula/build: `node@24 24.21.0_1`
- Executable path: `/opt/homebrew/bin/node`

This satisfies the reviewed webcore-CLI Node.js 24+ runtime requirement.

Deployment rule: verify `node --version` and `which node` before installing or changing Node.js. Do not overwrite an existing customer Node environment without first assessing dependencies and version-management requirements.

### webcore-CLI deployment source and layout decision

The upstream project guidance and current release metadata were re-checked on 2026-10-06.

Authoritative upstream:
- Repository: https://github.com/Cruxad0/webcore-CLI
- Latest release page: https://github.com/Cruxad0/webcore-CLI/releases/latest
- Reviewed release: https://github.com/Cruxad0/webcore-CLI/releases/tag/v0.4.7

The upstream README explicitly recommends the **versioned release ZIP** rather than GitHub's generic Source code archive. Release v0.4.7 publishes:
- `webcore-cli-v0.4.7.zip`
- `SHA256SUMS`

The GitHub release metadata also publishes a SHA-256 digest for the v0.4.7 ZIP: `ee5b32268c2b1898d3f51430b45905b3e92a9ece82a1ec349e3722ca42124170`.

The package declares:
- version `0.4.7`
- Node.js engine `>=24`
- no runtime npm dependency installation described by the README
- CLI entrypoint `node server/cli.js`

Deployment decision: use a **pinned, checksum-verified release ZIP** for the production MCP runtime. Keep the user's GitHub fork for audit/review/change tracking, not as the production executable checkout. This prevents accidental production drift from branch updates and makes rollback/version inventory deterministic.

The existing `~/Documents/Codex/WebcoreCode` directory is classified as legacy/workshop space and should not become the production runtime directory merely because it already exists. It currently contains the pre-existing status-bridge source copy and normal macOS metadata. Do not delete it until ownership/use of the remaining source copy is explicitly resolved.

The final production application directory should be deliberate, stable, user-scoped, and documented. Its exact path is to be selected before release extraction and then used consistently in the tunnel profile's MCP command, backup procedure, upgrade procedure, and uninstall/offboarding runbook.

### Verified webcore-CLI production deployment and local authentication

Verified on 2026-10-06:

- production application root: `~/Library/Application Support/WebCoRE-MCP`
- versioned payload directory: `~/Library/Application Support/WebCoRE-MCP/webcore-cli/0.4.7`
- release artifact: `webcore-cli-v0.4.7.zip`
- publisher checksum verification: `shasum -a 256 -c SHA256SUMS` returned `webcore-cli-v0.4.7.zip: OK`
- `npm run check` completed successfully
- `npm test` completed with 106 tests passed, 0 failed, 0 skipped
- local setup completed successfully with `node server/cli.js setup`
- authentication result: `ok=true`, `authenticated=true`
- credentials/configuration path: `~/.config/webcore-toolkit/config.json`
- credential file mode reported by webcore-CLI: `0600`
- live status verification: `ok=true`, `connected=true`, `dashboard_confirmed=true`
- snapshot source: `hub_snapshot`
- connection mode: `local`
- Hubitat/webCoRE instance label: `webCoRE - ValleyView`
- plugin version: `0.4.7`
- HE version: `v0.3.114.20240115_HE`
- webCoRE core version: `v0.3.114.20220203`
- read-only diagnostic: `ok=true`, no errors
- dashboard HTTP status: `200`, parsed successfully from a fresh `hub_snapshot` on first attempt
- live piston inventory: 17 pistons
- live authorized-device inventory: 95 devices
- diagnostic output explicitly reported `credentials_included=false`
- reported upload safety limits: 2048 URL bytes, 1500 chunk characters, 99 maximum chunks

The local WebCoRE execute URL/access token and dashboard password/PIN are secrets. They were entered only into the local setup prompt and are not to be copied into Git, chat, screenshots, deployment documentation, or customer runbooks. Reusable documentation records only where/how to obtain and enter them.

### Deployment productization principle

The reusable deliverable should distinguish three artifacts:
1. Architecture/design record: component boundaries, trust model, decisions, and rationale.
2. Deployment runbook: deterministic clean-room installation, validation, rollback, and customer-specific parameter collection.
3. Operations runbook: health checks, upgrades, backup/recovery, credential rotation, incident response, Mac replacement, customer offboarding, and troubleshooting.

Customer-specific identifiers and secrets must not be embedded in the reusable runbook. Use named placeholders/parameters for environment-specific values. Secrets remain local or in an approved secret store.


## 2026-10-06 production upgrade: webcore-CLI 0.4.8

### Purpose

Upgrade the local WebCoRE MCP runtime from 0.4.7 to 0.4.8 so ChatGPT Business can distinguish read-only MCP tools from write/action tools and enforce the intended approval boundary.

### Source/change control

The MCP annotation work was developed in `cznkane/webcore-CLI` on branch `fix/mcp-tool-annotations`, reviewed in PR #1, and squash-merged to `main` as commit `161febd35c67fd48459782098009932c4d764067`.

Release version: `0.4.8`.

Tool classification shipped in 0.4.8:
- 11 read-only tools: `readOnlyHint=true`, `destructiveHint=false`, `openWorldHint=false`
- 3 reversible/non-destructive write tools: create, pause, resume
- 2 action/destructive tools: apply piston update and live piston test
- all tools use `openWorldHint=false` because they operate against the bounded private Hubitat/WebCoRE environment

Regression tests assert the tool annotations returned by MCP `tools/list`.

### Production deployment

Production application root remains:

`~/Library/Application Support/WebCoRE-MCP`

Versioned runtime directories:
- previous/rollback: `webcore-cli/0.4.7`
- active: `webcore-cli/0.4.8`

The 0.4.8 payload was staged side-by-side from the clean canonical development checkout rather than overwriting 0.4.7.

Validation before cutover:
- staged package version: `0.4.8`
- test suite: 106 tests, 106 passed, 0 failed
- 0.4.7 retained untouched for rollback
- tunnel profile backed up before modification
- tunnel profile MCP command changed only from the 0.4.7 versioned path to the 0.4.8 versioned path
- runtime credential remained an environment-variable reference; no secret was added to the tunnel profile or Git

The existing foreground tunnel was stopped only after the new runtime had passed tests and the restart path was available. It was then restarted from the same credential-bearing shell, causing the already-updated profile to launch 0.4.8.

### ChatGPT Business tool metadata refresh

Important deployment requirement discovered during commissioning:

Updating the MCP server does **not** by itself refresh the tool classification already held by the ChatGPT Business private plugin.

After 0.4.8 was live, Business Admin still showed all 16 tools as write tools until:

1. Admin Console → Plugins → WebCoRE → Tools
2. Select **Refresh**
3. Verify the inventory changes from `Write tools 16` to:
   - `Read tools 11`
   - `Write tools 5`
4. Save changes

This refresh step is required after a deployed MCP release changes tool metadata/annotations.

Workspace permission policy remains **Allow read tools**. Do not weaken this to **Allow all tools** merely to suppress prompts.

### Known ChatGPT Business approval anomaly

Expected behavior after the metadata refresh:

- read tools execute without approval
- write tools require approval

Observed behavior on 2026-10-06:

- Business Admin correctly classifies WebCoRE as 11 read tools and 5 write tools
- plugin permission policy is explicitly **Allow read tools**
- the user-level plugin installation is connected and exposes no separate permission override
- a brand-new Business chat invoking `webcore_list_pistons` still displays an approval prompt
- the prompt offers **Allow once** or **Allow WebCoRE for this conversation**

The server-side annotation path is therefore verified through the Business Admin UI. The remaining read approval prompt is tracked as a ChatGPT Business permission/inheritance behavior or platform limitation, not as evidence that the 0.4.8 MCP classification failed.

Operational workaround: approve WebCoRE for the conversation when required. Do not change the workspace to **Allow all tools** as a workaround because that would weaken the intended write-approval boundary.

### Rollback

Until post-upgrade acceptance work is complete, retain 0.4.7 as the explicit rollback version.

Rollback procedure:
1. Stop the foreground tunnel deliberately.
2. Restore the backed-up pre-0.4.8 tunnel profile, or change only the versioned MCP command path from 0.4.8 back to 0.4.7.
3. Restart the tunnel with the existing runtime credential mechanism.
4. Verify local health/readiness and read-only Business access.
5. Record the rollback and reason in Git.

Do not delete 0.4.7 until 0.4.8 has completed the remaining acceptance work and the rollback-retirement decision is explicit.

### Cleanup state

Completed:
- temporary development Terminal used for the upgrade was closed after deployment
- canonical development checkout remains intentionally installed at `~/Developer/webcore-CLI`
- GitHub CLI/keyring authentication remains intentional development infrastructure
- active tunnel Terminal remains intentionally open because the runtime is still foreground-managed
- 0.4.7 remains intentionally retained as rollback inventory

Still to retire after the appropriate gates:
- merged `fix/mcp-tool-annotations` branch, after production documentation is safely recorded
- 0.4.7 rollback payload, only after 0.4.8 acceptance/stability is established
- foreground-terminal dependency, after the reboot/recovery runtime design is commissioned and verified

A deployment is not considered fully cleaned up while any of these items lacks an explicit retention or retirement reason.


## 2026-10-07 production upgrade: webcore-CLI 0.4.9

### Purpose

Extend the existing WebCoRE MCP service with a bounded, read-only direct Hubitat Maker API path for explicitly authorized devices. This path is separate from the WebCoRE-authorized device inventory and is intended for live Hubitat state that is useful to diagnosis but is not necessarily represented through WebCoRE.

### Source and release control

Canonical implementation repository: `cznkane/webcore-CLI`.

Release commits:
- `1f38ed0a2077b62e3340b647f2cd7184fd25bdf3` — Add read-only Hubitat Maker API MCP tools
- `e8eceeed487fe27dad566bdbe5ed50c160156d39` — Release 0.4.9

Release `0.4.9` is now pushed to canonical `main`.

Manifest/version verification:
- `package.json`: 0.4.9
- `plugin.json`: 0.4.9
- `.codex-plugin/plugin.json`: 0.4.9
- `server/hubitat.js`: present
- `server/index.js`: registers both direct Hubitat tools

The local release checkout passed the complete existing test suite: 106 tests, 106 passed, 0 failed.

A previously observed 105/106 manifest failure belonged to an intermediate version-bump state during earlier release work. It is not evidence that the final 0.4.9 release shipped with a failing suite.

### New Hubitat Maker API tools

0.4.9 adds two MCP tools:
- `hubitat_list_devices`
- `hubitat_get_device`

Both are classified:
- `readOnlyHint=true`
- `destructiveHint=false`
- `openWorldHint=false`

They operate only on devices explicitly authorized to the configured Hubitat Maker API instance and do not execute device commands.

The complete 0.4.9 MCP inventory is 18 tools: 13 read-only and 5 write-capable.

### Production deployment and verification

Production application root remains:

`~/Library/Application Support/WebCoRE-MCP`

Active payload:

`webcore-cli/0.4.9`

Verified on 2026-10-07:
- installed payload reports version 0.4.9
- installed `server/index.js` contains both Hubitat Maker API tools
- the live Node process launches `webcore-cli/0.4.9/server/index.js`
- exactly one tunnel-client process was observed, running `tunnel-client run --profile webcore`
- an independent MCP initialize request identified the server as `webcore-cli` 0.4.9
- MCP `tools/list` returned all 18 tools, including both Hubitat tools
- no production process restart was required during final certification

The temporary independent MCP audit process exited normally when stdin closed. It created no persistent service or deployment artifact.

### Inventory boundaries

Do not conflate these three inventories:

1. **Hubitat Maker API inventory** — devices explicitly authorized to the Maker API instance.
2. **WebCoRE inventory** — devices selected/authorized inside WebCoRE.
3. **ChatGPT-visible MCP inventory** — tools exposed to the current ChatGPT session by the private MCP plugin.

During 0.4.9 acceptance:
- direct Maker API returned 5 authorized devices
- the established WebCoRE inventory remained 95 authorized devices
- MCP advertised 18 tools

A result of 95 devices from `webcore_list_devices` does not prove the direct Maker API path is available.

### ChatGPT Business discovery and acceptance

Business Admin already displayed 18 tools before the final acceptance test. Refreshing plugin discovery continued to show 18.

An existing Business chat had previously failed to expose the new `hubitat_list_devices` tool even though Admin discovery already knew about all 18 tools. This established that Admin tool discovery and per-chat tool exposure/session state are distinct gates.

Final acceptance was performed in a brand-new ChatGPT Business chat with the request:

`Test Hubitat connection: list the authorized Hubitat devices.`

The request succeeded through the direct Maker API path and returned exactly 5 authorized devices:
- Piano
- P-Guest
- WX-WeatherFlow
- WebCoRE Status Bridge
- Virtual Switch

This is the end-to-end acceptance evidence for the 0.4.9 direct Hubitat read path.

Operational troubleshooting rule: when Admin shows the expected tool inventory but an existing chat cannot invoke a newly deployed tool, test a fresh Business chat before restarting the tunnel, reinstalling the MCP payload, republishing the plugin, or weakening permissions.

### Security and change-control outcome

No Maker API token, tunnel runtime credential, WebCoRE credential, or other reusable secret was recorded in Git or required in the acceptance transcript.

The direct Hubitat tools remain read-only. Existing WebCoRE write controls and explicit approval requirements are unchanged.

### Rollback and cleanup state

0.4.9 is the certified active runtime.

Do not delete the immediate prior production payload until rollback-retirement is explicitly approved after a suitable stability period. The versioned deployment layout makes rollback a path/profile change rather than an in-place overwrite.

Final certification left no temporary MCP process running and required no permission change, `chmod`, plugin recreation, tunnel restart, or production Node restart.

Remaining lifecycle work is separate from the 0.4.9 release itself:
- commission and verify reboot/recovery management for the tunnel/MCP runtime
- retire obsolete rollback payloads after the explicit retention decision
- complete the approved WebCoRE write-path acceptance scenario
- continue tracking the Business read-tool approval anomaly independently from Maker API availability


### 2026-10-07 rollback payload retirement

After successful 0.4.9 end-to-end acceptance, the production payload directory was inspected for deployment residue. It contained only three versioned releases: 0.4.7, 0.4.8, and 0.4.9; no staging or temporary payloads were present.

0.4.7 was deliberately retired because it was two releases behind the certified active runtime and 0.4.8 provides the immediate known-good rollback point.

Post-cleanup production payload inventory:
- 0.4.9 — active
- 0.4.8 — retained rollback
- 0.4.7 — removed

This satisfies the payload portion of the no-dust rule while preserving one explicit rollback version.
