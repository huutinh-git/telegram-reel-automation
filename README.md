# Telegram Reel Automation

Automate a **video URL → Facebook Page Reel** workflow using GitHub Actions, with optional Telegram status updates and delivery of the processed video.

> **Status:** Community documentation and security guidance are being prepared. The publishing workflow exists and has had successful historical GitHub Actions runs, but a fresh end-to-end verification has **not** been performed for this documentation release. This repository is **not** a complete Telegram bot: a separate bot or bridge must trigger `repository_dispatch` events.

**Tiếng Việt:** Dự án nhận URL video, tải video bằng yt-dlp, xử lý bằng FFmpeg, đăng lên Facebook Page Reels và có thể gửi thông báo cùng video đã xử lý qua Telegram. Bạn có thể chạy thủ công trên GitHub Actions. Nếu muốn gửi URL ngay trong Telegram, bạn phải tự thiết lập bot/bridge để gọi GitHub API; mã nguồn bot đó chưa có trong repository.

## Features / Tính năng

- Run manually through GitHub Actions (`workflow_dispatch`) with a video URL and an optional caption.
- Receive `repository_dispatch` events of type `telegram-video` from an **external** trusted integration.
- Download one source video with `yt-dlp` (not a playlist).
- Convert to up to **60 seconds** of 1080 × 1920, 30 fps H.264/AAC video with FFmpeg (padding may be added; content is not necessarily cropped).
- Create, upload, and publish a Facebook Page Reel through the Meta Graph API.
- Poll publishing status and attempt to retrieve the Reel permalink.
- Optionally notify a Telegram chat and send the processed video; upload a GitHub Actions artifact retained for one day.

**Important:** Running this workflow performs a **real Facebook publish**. It has no dry-run switch. Only use videos you have the rights and permissions to download and publish. Follow the source platform's and Meta's terms.

## What is in this repository?

| Path | Purpose |
| --- | --- |
| `.github/workflows/test.yml` | Existing publisher workflow; no operational change is included in this documentation kit |
| `docs/SETUP.md` | Initial setup, secrets, manual and Telegram-triggered execution |
| `docs/ARCHITECTURE.md` | Processing flow, inputs, outputs, current boundaries |
| `docs/TROUBLESHOOTING.md` | Known failure patterns and safe troubleshooting |
| `docs/ROADMAP.md` | Prioritized engineering work before a stable release |
| `SECURITY.md` | Secret handling and responsible vulnerability reporting |
| `CONTRIBUTING.md` | How to propose changes without publishing to a real Page |

## Quick start (manual workflow)

1. Fork or clone the repo and configure a Facebook Page access token as an **Actions repository secret** named `FACEBOOK_PAGE_ACCESS_TOKEN`. It must be authorized for the requested publishing operations.
2. Optional: add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` if you want Telegram notifications for manually dispatched runs.
3. Open **Actions → Telegram to Facebook Reel → Run workflow**.
4. Enter a source `video_url` and, optionally, a `caption`.
5. Observe the run and check the result on the **actual Facebook Page** before retrying a failed run. Some later steps can fail **after** Facebook has published a Reel.

See [detailed setup instructions](docs/SETUP.md) before running the workflow.

## Configuration reference

| GitHub Actions secret | Required | Used for |
| --- | --- | --- |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | **Yes** for actual publishing | Meta Graph API session/upload/publish/status |
| `TELEGRAM_BOT_TOKEN` | Only if Telegram notifications or video delivery are used | Telegram Bot API |
| `TELEGRAM_CHAT_ID` | Optional; manual runs only | Default chat ID for Telegram notifications |

**The current workflow** expects the following event inputs:

| Trigger | Input | Notes |
| --- | --- | --- |
| `workflow_dispatch` | `video_url` | Required source video URL |
| `workflow_dispatch` | `caption` | Optional description |
| `repository_dispatch` (`telegram-video`) | `client_payload.video_url` | Required; caller must be authenticated |
| `repository_dispatch` (`telegram-video`) | `client_payload.caption` | Optional |
| `repository_dispatch` (`telegram-video`) | `client_payload.chat_id` | Optional Telegram destination |
| `repository_dispatch` (`telegram-video`) | `client_payload.status_message_id` | Optional existing Telegram message to edit |

The repository does not contain a Telegram message listener, external bridge deployment, or a credentials provisioning tool. Do **not** paste secrets into workflow YAML, README files, screenshots, issue comments, or dispatch payloads.

## Operational limitations

- Video processing currently stops at 60 seconds, even when the source is longer.
- The processing uses vertical padding to preserve aspect ratio; landscape video may have borders.
- `yt-dlp` extractor availability depends on the source service and may change.
- Processing and publishing depend on GitHub-hosted runners, Meta APIs and a working Page access token.
- A run can be marked failed after the Reel was already published (for example, Telegram delivery or artifact upload fails). **Verify before rerunning** to avoid duplicates.
- The workflow uses a moving runner image and installs dependencies dynamically; reproducibility and dependency hardening are roadmap items.
- Video artifacts and workflow logs should be reviewed for confidentiality before use with private or sensitive material.

## Security and contributions

Please read [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md). Changes that may publish publicly should be reviewed and tested with a dedicated test Page before merging.

## License / Giấy phép

**No OSI-approved LICENSE has yet been chosen by the maintainer.** Public visibility alone does not authorize reuse of the source code. The maintainer should explicitly select a license (for example, MIT or Apache-2.0) after reviewing ownership and any third-party code obligations. Do not claim this repo is fully open source until a suitable license is added.
