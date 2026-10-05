# ChatGPT ↔ WebCoRE MCP Architecture

**Status:** In progress  
**Decision owner:** CIO / CTO operating model  
**Last updated:** 2026-10-05

## Objective

The acceptance test is not merely “ChatGPT can connect to WebCoRE.”

The target operating experience is a request such as:

> Kids Away was ON and School Mornings fired anyway because AndieEffective was true. Fix it.

ChatGPT should then be able to inspect the live pistons, relevant variables/devices and execution logs; determine the root cause and blast radius; prepare the smallest appropriate change; present the proposed change for approval; apply it after approval; verify the stored piston read-back; and record the change.

The user should not have to act as a human API by repeatedly supplying screenshots or manually translating changes into WebCoRE.

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

An OpenAI Platform tunnel was created and associated with the intended Business workspace. The official OpenAI tunnel client repository/release path was identified. The target Mac reports `arm64`, so the macOS Darwin ARM64 artifact is required.

Before execution, the downloaded artifact must be verified against the publisher-provided SHA-256 checksum.

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
- Official OpenAI tunnel-client release location identified.
- Target Mac architecture confirmed as `arm64`.
- Screenshot security scoring and proactive redaction procedure adopted.
- CTO direction/risk scoring adopted.

Not yet completed:
- Download/verify/install the Darwin ARM64 tunnel client.
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

1. Download the official macOS Darwin ARM64 tunnel-client artifact.
2. Verify SHA-256 against the official published checksum before execution.
3. Inspect/install the tunnel client using the publisher-supported procedure.
4. Connect it to the already-created tunnel; keep enrollment credentials local.
5. Verify Node.js version and install/upgrade to 24+ if required.
6. Install/pin the reviewed webcore-CLI release.
7. Run local WebCoRE setup. Enter the execute URL/token and dashboard password locally only.
8. Run read-only `status` / `diagnose`.
9. List/pull a known piston and verify it against the known current state.
10. Connect the tunnel client to the webcore-CLI stdio MCP process.
11. Create the private WebCoRE custom MCP plugin using the tunnel.
12. Create/compress the plugin icon and publish with conservative access.
13. From ChatGPT Business, prove live read-only inspection.
14. Only then test an approved write through prepare → diff → approval → apply → read-back verification.

## Acceptance scenario

The integration is mature when the user can report an operational symptom in natural language, for example:

> Kids Away was on and School Mornings fired this morning anyway due to AndieEffective being true. Fix it.

ChatGPT should independently gather the relevant live evidence, explain the root cause, distinguish whether the defect belongs in School Mornings or upstream occupancy/effective-presence logic, inspect dependencies, propose the smallest robust fix, obtain approval, apply and verify it, and document the material change.

A second known acceptance scenario is cancellation/control of queued WebCoRE work: pausing School Mornings did not stop an already queued 30-minute fade. The mature design should include a deliberate kill/cancel strategy for pending work rather than relying on piston pause as an emergency stop.
