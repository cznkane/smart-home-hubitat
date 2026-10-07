# WebCoRE MCP Foreground Runtime Operations

**Status:** Canonical interim operations note  
**Scope:** Foreground-managed Smart Home WebCoRE MCP tunnel/runtime  
**Governing protocol:** `docs/SMART_HOME_OPERATING_PROTOCOL.md`  
**Release procedure:** `docs/WEBCORE_MCP_RELEASE_DEPLOYMENT_RUNBOOK.md`  
**Related issue:** #23

## Purpose

Until a managed reboot/recovery runtime is commissioned, the production MCP tunnel depends on a foreground shell that owns the runtime credential environment. This document preserves the terminal-role discipline established during the 0.4.9 deployment so future troubleshooting does not destroy the only known restart-capable context.

This is an interim operating model, not the desired permanent recovery architecture.

## Terminal roles

### TOKEN-BEARING

The original shell containing the locally exported runtime credential reference required by:

`tunnel-client run --profile webcore`

Normal state: occupied by the live long-running tunnel process.

Rules:
- do not expose, echo, print, screenshot, paste, or commit the credential value
- do not close or repurpose this shell while it owns the only proven restart-capable environment
- do not recreate the secret in CONTROL merely for convenience
- before stopping the tunnel, prove the restart path and preserve this environment

### CONTROL

An ordinary fresh shell for:
- Git inspection/work
- process inspection
- profile inspection
- read-only diagnostics
- commands that do not require the tunnel runtime credential

Do not assume CONTROL inherited the TOKEN-BEARING environment.

A prior deployment error attempted to start the tunnel from CONTROL; it failed because the credential environment was absent. The correct action was to restart from TOKEN-BEARING.

### SERVER

If a distinct development/server shell exists, treat it as a separate role. Leave it alone unless the current task explicitly requires it.

## Operating rules

1. Identify terminals by **purpose/role**, never by window number.
2. Before any stop/restart, distinguish TOKEN-BEARING from CONTROL.
3. Do not restart a known-good runtime merely to investigate a downstream Business/Personal ChatGPT exposure problem.
4. Stop old -> verify old gone -> start replacement -> verify replacement -> close obsolete windows.
5. Keep only continuing-purpose windows. Completed, failed, stale, duplicate, or “Process completed” windows are residue.
6. Preserve one intentional rollback runtime according to the release runbook; do not confuse rollback inventory with forgotten dust.
7. Secrets remain local through the supported environment/config mechanism.

## Current lifecycle

webcore-CLI 0.4.9 is the certified active runtime and 0.4.8 is the retained rollback payload. The foreground terminal dependency remains technical debt tracked by #23.

When #23 commissions a supported managed recovery mechanism and that mechanism passes reboot/recovery acceptance, this interim document should be revised or retired and the no-dust cleanup completed.
