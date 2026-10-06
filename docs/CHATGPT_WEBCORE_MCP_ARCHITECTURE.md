# ChatGPT ↔ WebCoRE MCP Architecture

**Status:** In progress  
**Decision owner:** CIO / CTO operating model  
**Last updated:** 2026-10-06

## Objective

This implementation is also intended to become a **repeatable deployment pattern** that can be reproduced for other Hubitat/WebCoRE environments and potentially offered as a professional service. Documentation therefore needs to be sufficient for a clean-room deployment by a competent technician who was not present for the original build.

The acceptance test is not merely “ChatGPT can connect to WebCoRE.”

The target operating experience is a request such as:

> Kids Away was ON and School Mornings fired anyway because AndieEffective was true. Fix it.

ChatGPT should then be able to inspect the live pistons, relevant variables/devices and execution logs; determine the root cause and blast radius; prepare the smallest appropriate change; present the proposed change for approval; apply it after approval; verify the stored piston read-back; and record the change.

The user should not have to act as a human API by repeatedly supplying screenshots or manually translating changes into WebCoRE.

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

## Current implementation state

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

### Deployment productization principle

The reusable deliverable should distinguish three artifacts:
1. Architecture/design record: component boundaries, trust model, decisions, and rationale.
2. Deployment runbook: deterministic clean-room installation, validation, rollback, and customer-specific parameter collection.
3. Operations runbook: health checks, upgrades, backup/recovery, credential rotation, incident response, Mac replacement, customer offboarding, and troubleshooting.

Customer-specific identifiers and secrets must not be embedded in the reusable runbook. Use named placeholders/parameters for environment-specific values. Secrets remain local or in an approved secret store.
