# WebCoRE MCP Release and Deployment Runbook

**Status:** Canonical release/deployment procedure  
**Scope:** `cznkane/webcore-CLI` releases deployed to the Smart Home MCP bridge  
**Canonical architecture:** `docs/CHATGPT_WEBCORE_MCP_ARCHITECTURE.md`  
**Governing protocol:** `docs/SMART_HOME_OPERATING_PROTOCOL.md`  
**Bootstrap:** `CHATGPT_INIT.md`  
**Last validated:** 2026-10-07 with webcore-CLI 0.4.9

## Purpose

This runbook is the authoritative procedure for preparing, releasing, deploying, verifying, rolling back, cleaning up, and documenting a webcore-CLI production release.

It exists specifically to prevent release work from becoming a chain of assumptions. A version bump, passing command, copied payload, running process, Admin tool count, and successful Business-chat invocation are separate gates. None substitutes for the others.

## Trigger phrase

When Rick says **"deploy"** in a Smart Home technical chat, treat that as a request to initialize from Git and use this runbook.

Before consequential deployment instructions:

1. Load `CHATGPT_INIT.md`.
2. Load `docs/SMART_HOME_OPERATING_PROTOCOL.md`.
3. Load this runbook.
4. Load `docs/CHATGPT_WEBCORE_MCP_ARCHITECTURE.md` when the deployment affects MCP, tunnel, Hubitat, WebCoRE, ChatGPT Business, recovery, or production topology.
5. Inspect the current canonical Git state and the relevant live/installed state.
6. Build an evidence ledger: Proven / Not yet proven / Changed / Rollback retained / Cleanup owed.

Do not rely on conversational memory as a substitute.

## Non-negotiable release principles

- GitHub `cznkane/webcore-CLI` `main` is the canonical released source after a release is pushed.
- A local commit that is ahead of `origin/main` is not yet canonical GitHub state.
- Never claim a proposed command was executed unless Rick reports its result or the result is independently retrieved.
- Never declare a release gate passed from partial terminal output.
- Before issuing another shell command, confirm the previous command has returned to a shell prompt. A Git pager (`:`, `(END)`, etc.) is not a shell prompt.
- Red/green Git diff coloring is normal deletion/addition presentation and is not itself an error.
- Do not push while the diff/release state is still uncertain.
- Never force-push production release history as a troubleshooting shortcut.
- Never weaken plugin permissions, republish/recreate the plugin, restart a known-good runtime, or reinstall components until evidence identifies that layer.
- Keep secrets out of Git, chat, screenshots, and copied commands.
- One known-good prior production payload is normally retained as rollback until explicitly retired.

## Release state model

Treat these as independent gates:

1. **Source gate** — intended code exists locally and working tree/branch state is understood.
2. **Manifest gate** — every version-bearing manifest agrees.
3. **Test gate** — complete release checks/tests pass.
4. **Diff gate** — release delta is reviewed and expected.
5. **Canonical Git gate** — tested commits are pushed to GitHub and GitHub HEAD is independently verified.
6. **Installed-payload gate** — production versioned directory contains the intended release.
7. **Running-runtime gate** — the live MCP Node process is actually running the intended versioned payload.
8. **MCP protocol gate** — independent `initialize` and `tools/list` identify the intended version and tool inventory.
9. **Tunnel gate** — exactly the intended tunnel runtime is active and connected to the intended MCP command.
10. **Business Admin discovery gate** — the private plugin discovers the expected tools/annotations.
11. **Fresh-chat acceptance gate** — a brand-new Business chat can invoke the newly added/changed capability.
12. **Cleanup/documentation gate** — predecessor classification, residue cleanup, rollback retention, and canonical documentation are complete.

Do not collapse these gates into “deployment worked.”

## Foreground runtime operating note

While the tunnel remains foreground-managed, terminal ownership and credential-bearing shell discipline are defined in `docs/WEBCORE_MCP_FOREGROUND_RUNTIME_OPERATIONS.md`. Apply that note automatically to stop/start/restart work. Managed reboot/recovery commissioning is tracked in #23.

## Phase 1: establish current state

### Git

Inspect:
- current branch
- working-tree cleanliness
- relationship to `origin/main`
- recent commits relevant to the release
- intended version

If local `main` is ahead of `origin/main`, preserve that fact in the evidence ledger. Do not infer that GitHub already contains the release.

### Production

Inspect, without changing:
- installed version directories under `~/Library/Application Support/WebCoRE-MCP/webcore-cli`
- tunnel profile MCP command
- running Node MCP process
- running tunnel-client process
- current Business Admin tool inventory when relevant

Do not restart anything during discovery.

## Phase 2: prepare release source

Implement the smallest intended change in `cznkane/webcore-CLI`.

For a versioned release, update every version-bearing manifest used by the project. As of 0.4.9 these include:

- `package.json`
- `plugin.json`
- `.codex-plugin/plugin.json`

Do not assume changing `package.json` is sufficient.

If the project adds another version-bearing manifest later, update this runbook and the manifest consistency tests.

## Phase 3: release validation

Run the repository's release checks from the intended release checkout:

`npm run check`

then:

`npm test`

Both must pass before release certification.

A failed manifest test is a release blocker. Correct the inconsistency and rerun the complete required release gate. Do not deploy merely because most tests passed.

### 0.4.8 historical lesson

During earlier version-bump work, a manifest mismatch produced 105/106 passing tests because one manifest still reported the prior version. That intermediate failure was corrected before the completed release. The lesson is that manifest consistency is a mandatory release gate, not that the final later release was defective.

## Phase 4: review release delta

Review the diff between canonical upstream state and intended release HEAD.

Confirm:
- only intended files changed
- version-bearing files agree
- new tools/modules are present
- annotations/security properties are intentional
- no credentials, generated junk, temporary files, or unrelated edits are included

Use non-paging/targeted output when appropriate so terminal state is unambiguous.

Do not issue a new command while Git's pager is still active. Exit the pager first and confirm the shell prompt.

## Phase 5: publish canonical Git

Only after source, manifests, tests, and diff are certified:

- push the intended commits normally to `origin/main`
- do not force
- independently verify GitHub `main` HEAD
- inspect the canonical GitHub files needed to prove the release contents/version

The release is not canonical merely because the local checkout is correct.

## Phase 6: stage production side-by-side

Production root:

`~/Library/Application Support/WebCoRE-MCP`

Versioned payload layout:

`~/Library/Application Support/WebCoRE-MCP/webcore-cli/<version>`

Stage the new version beside the current version. Do not overwrite the known-good active payload in place.

Before cutover:
- verify staged package version
- verify expected source/tool files
- run the appropriate checks/tests against the staged payload where applicable
- preserve the immediate known-good prior version as rollback
- back up the tunnel profile before changing its MCP command
- keep runtime credentials referenced through the existing supported secret mechanism, never embedded in Git/profile documentation

## Phase 7: cut over deliberately

Change only the versioned MCP command path needed to select the new payload.

Stop/restart the foreground tunnel only after:
- the staged payload is certified
- rollback is available
- the credential-bearing runtime environment needed to restart is understood/preserved

Do not casually restart unrelated components.

After cutover, verify the live process command points to the intended versioned `server/index.js`.

## Phase 8: certify the MCP runtime itself

Do not infer MCP identity from filesystem contents alone.

Use an independent temporary MCP stdio invocation with the same Node execution pattern as production to request:
- `initialize`
- `tools/list`

Verify:
- server name
- server version
- expected total tool count
- expected new/changed tool names
- expected annotations/classifications

Use `node <path>/server/index.js` if production launches the server with Node. Do not assume the JS file itself has executable permission and do not add `chmod` merely to make an audit command work.

The temporary audit process should exit when stdin closes and should not create a persistent service.

### 0.4.9 validated example

0.4.9 acceptance established:
- server identity `webcore-cli` 0.4.9
- 18 total MCP tools
- 13 read-only
- 5 write-capable
- new read-only tools `hubitat_list_devices` and `hubitat_get_device`

These counts are historical evidence for 0.4.9, not hard-coded expectations for future releases.

## Phase 9: certify tunnel and Business discovery

Verify one intended tunnel-client process is active and associated with the expected profile/runtime.

In ChatGPT Business Admin, refresh tool discovery when a release changes MCP tools or annotations.

Verify the discovered inventory matches the release.

Important: **Business Admin discovery is not the same gate as per-chat tool exposure.**

0.4.9 demonstrated that Business Admin could already show all 18 tools while an existing Business chat still failed to expose a newly added Hubitat tool.

Do not restart/reinstall a healthy local runtime merely because an old chat lacks a newly deployed tool.

## Phase 10: fresh-chat acceptance

When a release adds or changes a ChatGPT-visible capability, test it in a **brand-new Business chat** after Admin discovery is correct.

Use an acceptance request that uniquely proves the new path rather than a nearby legacy path.

For 0.4.9, the acceptance request was:

`Test Hubitat connection: list the authorized Hubitat devices.`

Success returned the 5 Maker API-authorized devices rather than the separate 95-device WebCoRE inventory. This proved the direct Hubitat Maker API path rather than merely proving legacy WebCoRE device access.

For future releases, define the equivalent discriminating acceptance test before deployment.

## Phase 11: rollback

If a post-cutover gate fails:

1. Stop at the failed layer.
2. Preserve evidence.
3. Do not scatter speculative repairs across lower layers already proven good.
4. If rollback is required, restore the previous tunnel profile/versioned MCP path.
5. Restart using the known credential mechanism.
6. Verify the prior version's runtime and Business access.
7. Record the rollback and reason in Git.

A failure in Business chat exposure does not automatically justify a local runtime rollback if the runtime, MCP manifest, tunnel, and Business Admin discovery are already proven correct.

## Phase 12: no-dust cleanup

After successful acceptance, inspect residue explicitly.

Classify every retained version/artifact:
- **ACTIVE**
- **ROLLBACK**
- **RETIRE**
- **INVESTIGATE**

Normally retain the immediate prior known-good payload as rollback. Older superseded payloads should be retired once they no longer provide meaningful recovery value.

Also inspect, where relevant:
- temporary/staging directories
- downloaded archives/checksums
- temporary MCP processes
- development terminals
- background processes
- profile backups
- stale branches
- obsolete documentation
- credentials/environment changes
- services/launch agents
- permissions/security exceptions

Do not delete something merely because it is old. Do not retain something merely because deletion was forgotten.

## Phase 13: document final state

Update the canonical architecture/operations record with:
- purpose
- release commits/version
- test results
- manifest/tool changes
- production path
- runtime verification
- tunnel/Admin discovery results
- fresh-chat acceptance result
- security outcome
- rollback inventory
- cleanup/retirement
- known remaining work

The deployment is not done until the record reflects reality.

## 0.4.9 incident lessons incorporated into this runbook

The 2026-10-07 recovery established several permanent rules:

- GitHub may lag a correct local release. Check both.
- A local branch ahead of `origin/main` is evidence, not failure.
- Do not mistake Git pager state for a shell prompt.
- Do not mistake normal red diff deletions for an error.
- Do not declare a push appropriate before source/diff state is actually understood.
- Verify all version-bearing manifests, including `.codex-plugin/plugin.json`.
- Passing tests and correct source do not prove the installed payload.
- Correct installed payload does not prove the running process.
- Correct running process does not prove the MCP-advertised tool inventory.
- Correct MCP inventory does not prove Business Admin discovery.
- Correct Business Admin discovery does not prove an existing chat has refreshed tool exposure.
- A fresh Business chat is a required acceptance gate for newly exposed tools.
- Distinguish Maker API device inventory, WebCoRE device inventory, and MCP tool inventory.
- Do not disturb lower layers once evidence has exonerated them.
- Finish with cleanup and documentation.

## Definition of done

A deployment is complete only when:

**Source certified → tests green → diff reviewed → Git canonical → payload staged → runtime cut over → MCP identity/tools certified → tunnel certified → Business discovery certified → fresh-chat capability accepted → rollback classified → residue cleaned → final state documented**

Anything less is an intermediate state, not “done.”
