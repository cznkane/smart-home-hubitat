# WebCoRE MCP Mac Reboot Recovery

**Status:** implementation candidate, requires commissioning test on the target Mac  
**CTO direction:** 🟢 Sound, provided the Keychain and launchd commissioning tests pass  
**Test platform:** Apple Silicon macOS, 2026-10-06

## Goal

After a Mac reboot, restore the WebCoRE MCP bridge with a simple Finder double-click without placing the OpenAI runtime API key in Git, shell history, a `.command` file, `.zshrc`, a plist, or plaintext configuration.

The operator controls are installed into `~/Applications/WebCoRE MCP/`: Start, Status, and Stop.

## Security model

The OpenAI tunnel runtime key is stored as a macOS Login Keychain generic password named `WebCoRE MCP Tunnel Runtime`. The launchd runner retrieves it at process start with macOS `security`, exports it only into the tunnel-client process environment as `CONTROL_PLANE_API_KEY`, then removes the temporary shell variable.

No secret value belongs in this repository. The tunnel profile continues to reference `env:CONTROL_PLANE_API_KEY`.

## Runtime model

A per-user LaunchAgent named `com.kaneconsulting.webcore-mcp` starts `/opt/homebrew/bin/tunnel-client run --profile webcore`.

`RunAtLoad=false`: reboot leaves the bridge stopped until the operator double-clicks Start. `KeepAlive=true`: after intentional start, launchd keeps it alive. Stop uses `launchctl bootout`, never broad `pkill` matching.

Automatic login startup is deferred until manual reboot recovery passes.

## Prerequisites

The installer refuses to proceed unless these already exist:
- Homebrew tunnel-client at `/opt/homebrew/bin/tunnel-client`
- Node at `/opt/homebrew/bin/node`
- `~/.config/tunnel-client/webcore.yaml`
- pinned webcore-CLI 0.4.7 at `~/Library/Application Support/WebCoRE-MCP/webcore-cli/0.4.7/server/index.js`
- macOS `security`, `launchctl`, and `curl`

The package does not silently install or upgrade prerequisites.

## Installation

From a trusted checkout of this repository, run `scripts/webcore-mcp/install.sh`.

The installer validates prerequisites, installs owned runtime/launcher files, creates the LaunchAgent, and creates the Keychain item only if absent. The secret prompt has terminal echo disabled. It does not start the tunnel automatically.

### Expected result

Three Finder launchers exist under `~/Applications/WebCoRE MCP`; the LaunchAgent exists under `~/Library/LaunchAgents`; the runtime key is in Keychain and absent from Git/shell startup files.

### Stop conditions

Stop if a prerequisite is missing, Keychain storage fails, generated plist contains a credential, permissions fail, or an owned path contains unexpected material that has not been reviewed.

## Start / status / stop

Start checks health/readiness first. If already healthy, it reports online and creates no duplicate. If offline, it verifies the Keychain item, starts the LaunchAgent, waits up to 20 seconds, and requires both health and readiness. Success is `🟢 WebCoRE MCP ONLINE`.

Status is read-only and reports loopback health/readiness.

Stop unloads the owned LaunchAgent. If health remains live, it reports that another tunnel-client may be running and deliberately does not kill processes blindly.

Logs: `~/Library/Logs/WebCoRE-MCP/`.

## Reboot acceptance test

Do not call this production-ready until:
1. Stop the manually foregrounded commissioning tunnel-client.
2. Run the installer from Git.
3. Verify the Keychain item exists without displaying its value.
4. Double-click Start and require health=live and readiness=ready.
5. From Business ChatGPT, list WebCoRE pistons.
6. Run WebCoRE diagnosis and verify authorized-device inventory.
7. Double-click Start again and prove no duplicate is created.
8. Double-click Stop and prove health goes offline.
9. Reboot the Mac.
10. Confirm the bridge is initially offline.
11. Double-click Start.
12. Repeat the Business ChatGPT read-only tests.

ValleyView's known-good commissioning baseline on 2026-10-06 is 17 pistons and 95 authorized devices. These are site-specific validation values, not reusable defaults.

## Rollback / ownership

Owned artifacts:
- `~/Library/Application Support/WebCoRE-MCP/ops/runner.sh`
- `~/Library/LaunchAgents/com.kaneconsulting.webcore-mcp.plist`
- `~/Applications/WebCoRE MCP/`
- `~/Library/Logs/WebCoRE-MCP/` after logs are no longer needed
- Keychain item `WebCoRE MCP Tunnel Runtime`, only during intentional decommission/rotation

Do not remove Homebrew, Node, tunnel-client, the pinned webcore-CLI payload, `~/.config/tunnel-client` wholesale, or `~/.config/webcore-toolkit` wholesale without dependency review.

## Current known limitations

- This package has not yet passed first on-Mac commissioning.
- The Business plugin icon/branding defect remains unresolved and must not be represented as completed.
- Business ChatGPT read access has been proven end-to-end: 17 pistons and 95 authorized devices.
- Future productization should parameterize site/profile/version/inventory/Keychain names.
- A later idempotent bootstrap layer can install prerequisites, but only after this recovery layer is proven.
