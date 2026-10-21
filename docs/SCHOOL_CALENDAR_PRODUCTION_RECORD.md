# School Calendar — production record (2026-10-21)

Status: **live and operator-accepted**. Runtime truth: WebCoRE. Historical development PR [#40](https://github.com/cznkane/smart-home-hubitat/pull/40) was closed without merge; its October 14–16 cutover instructions are obsolete and MUST NOT be replayed.

## Canonical production (direct WebCoRE identity verification)

| Name | Piston ID | Build | State | Schedules |
|---|---|---:|---|---:|
| Modes | `:10066aa6c85b426ae58294e795a317ba:` | 5 | active | 5 |
| School Mornings | `:f0fe1fbf820b26076564b1f7a28c5070:` | 3 | active | 3 |
| Variables | `:ecaf8bcdc04139eebd046b5fce47d9d3:` | 2 | active | 7 |

Post-rename WebCoRE backup fingerprints:
- Modes: `6b27850948a2b59988035c93ea00ea3549395d08160d37cc97a920b03363732e`
- School Mornings: `d4381d08b4ece98b680270fd27c96af65738205b939671980b30843cde90ca4b`
- Variables: `77af2df5363d91fb306fb0e6aa99ba6ab5aded1df5aa7781fd2fd03d5eb6d613`

## Preserved rollback archives

| Name | Piston ID | Build | State | Schedules |
|---|---|---:|---|---:|
| Modes(archive) | `:610151aa2ec89c411b197dcad7666d44:` | 59 | paused | 0 |
| School Mornings(archive) | `:917583854fbc49e5610e0ef27c2aa6d0:` | 32 | paused | 0 |
| Variables(archive) | `:d5f5963fee53c8113b294d4baf24c6e9:` | 16 | paused | 0 |

Rollback is NOT authorized by this record. Preserve archives; if rollback is separately approved, back up and verify live state, pause affected production version before resuming corresponding archive, and independently verify schedules and behavior. Never activate both versions concurrently. Follow `docs/SMART_HOME_OPERATING_PROTOCOL.md` and `docs/WEBCORE_MCP_RELEASE_DEPLOYMENT_RUNBOOK.md`.

## Acceptance boundaries

The operator reports functioning production behavior. The six piston identities and active/paused states were verified by direct WebCoRE readback; active schedule counts (5/3/7) persisted across naming promotion. Rename incremented builds and changed full-definition backup hashes, so byte-for-byte logic equivalence has **not** been established. The historical 80-case runtime matrix was not independently completed. No production tests or writes were executed during administrative closeout.

The natural Dusk-to-Evening transition and recurring timer investigation remain separate: [#29](https://github.com/cznkane/smart-home-hubitat/issues/29), [#52](https://github.com/cznkane/smart-home-hubitat/issues/52). MCP test commissioning remains [#43](https://github.com/cznkane/smart-home-hubitat/issues/43). PR #40 was closed **without merging source or tests into main**; if those are needed, use a new reconciled non-deployment PR.

**Disposition:** Calendar production promotion and canonical naming are complete. No additional live deployment is required.
