# Architecture: current implementation

## Scope

This repository contains a single GitHub Actions publisher workflow: `.github/workflows/test.yml`. It is not a complete standalone application, Telegram bot, or hosted backend. The Telegram inbound bridge must be provided and secured separately.

```text
Manual GitHub Actions run ─────────────────────┐
                                               ├─> Resolve URL/caption/chat IDs
Trusted external Telegram bridge ─dispatch─────┘             │
                                                             v
                                                        yt-dlp download
                                                             │
                                                             v
                                                     FFmpeg normalization
                                                     1080x1920, <=60s
                                                             │
                                                             v
                                               Meta Graph API upload session
                                                             │
                                                             v
                                                Upload + publish Facebook Reel
                                                             │
                                                             v
                                                Poll status and get permalink
                                                             │
                                      ┌──────────────────────┴─────────────────┐
                                      v                                        v
                            Optional Telegram messages                Actions video artifact
                            + processed video                         retention: one day
```

## External boundaries

| System | Role | Important dependency |
| --- | --- | --- |
| GitHub Actions | Runs the orchestration | Runner, repository settings and Actions permissions |
| External Telegram bridge | Optional event intake | Not included; must authenticate the sender |
| yt-dlp | Obtains source media | Extractor support and rights to content |
| FFmpeg | Normalizes media | Available in Ubuntu runner |
| Meta Graph API | Publishes Facebook Page Reel | Valid Page token and API behavior |
| Telegram Bot API | Optional status and video delivery | Bot token/chat authorization |

## Interface

See [SETUP.md](SETUP.md) for precise GitHub Actions secret names and `repository_dispatch` payload keys. There is no database, web UI, account creation system or multi-user authorization service in the repository.

## Current operational risks

- `GITHUB_ENV` includes untrusted request values. Safer handling and input validation are needed.
- Dependency versions and Ubuntu runner are not fully pinned.
- The publisher has no dry-run mode; a failed run may already have posted a Reel.
- No automated non-publishing test workflow is included.

See the [engineering roadmap](ROADMAP.md).
