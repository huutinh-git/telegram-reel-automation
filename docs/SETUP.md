# Setup and usage

This guide documents the **current** `.github/workflows/test.yml` behavior. It does not add an external Telegram bot implementation.

## Prerequisites

- GitHub repository with Actions enabled.
- A Facebook **Page** you are authorized to publish Reels to, and a Page access token accepted by the Meta Graph API for video publishing.
- A direct or extractor-supported video URL that you are authorized to use.
- Optional: a Telegram bot token and chat ID for notifications or processed-video delivery.

GitHub-hosted Ubuntu runners install FFmpeg through apt and a pre-release `yt-dlp` build through pip. The workflow references Graph API `v26.0` as written; API access, scopes and token validity must be verified separately against current Meta documentation.

## Configure Actions secrets

In GitHub: **Repository → Settings → Secrets and variables → Actions → New repository secret**.

| Name | Purpose |
| --- | --- |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | Required to upload, publish and query the Reel |
| `TELEGRAM_BOT_TOKEN` | Required only when Telegram status/video delivery is desired |
| `TELEGRAM_CHAT_ID` | Optional fallback chat for manual runs |

Never put access tokens in `README.md`, GitHub Issues, workflow inputs, `client_payload` or files in the repository. **Do not share tokens through chat for setup.**

## Option A: run manually

1. Open **Actions → Telegram to Facebook Reel**.
2. Select **Run workflow** on branch `main`.
3. Enter `video_url` and optional `caption`.
4. Start the workflow only when you are ready to **publish publicly**.
5. Follow job `publish` in the Actions log. Check the Facebook Page directly to confirm the Reel.

If `TELEGRAM_CHAT_ID` is empty, the manual run does not attempt to send a Telegram message/video. If it is set, `TELEGRAM_BOT_TOKEN` must also be valid or a post-publication delivery step may fail.

## Option B: dispatch from an external Telegram integration

The workflow accepts `repository_dispatch` events with `event_type` `telegram-video`, created by an **external authenticated bridge**. That bridge is not in this repository. Its responsibilities include receiving Telegram updates, checking the sending user's authorization, acquiring a video URL, and dispatching the event.

Payload shape (example only; **no secrets**):

```json
{
  "event_type": "telegram-video",
  "client_payload": {
    "video_url": "https://example.org/your-authorized-video.mp4",
    "caption": "Optional caption",
    "chat_id": "<telegram-chat-id>",
    "status_message_id": "<optional-existing-message-id>"
  }
}
```

The bridge must use a GitHub credential authorized to send repository dispatch events. Keep that credential in the bridge's secret store, not in the payload or source code. Verify exact required permissions against the current GitHub REST API documentation.

## What happens after you run it?

1. Resolve the manual or dispatch input.
2. Install `ffmpeg` and `yt-dlp`.
3. Download one video into `downloads/`.
4. Require at least four seconds of input video; normalize to a vertical MP4, up to 60 seconds.
5. Start an upload session, upload `processed/ready.mp4`, then request Facebook Reel publication.
6. Poll up to 30 times, approximately 10 seconds apart, for Facebook's publishing status.
7. Attempt to fetch a permalink, optionally notify/send the video via Telegram, and upload a GitHub Actions artifact retained for one day.

The final Telegram delivery and artifact steps happen **after** publication. A failure at one of those steps does **not** prove that publication failed. Check the Page before restarting a run.

## Safe operation

- Use a dedicated test Facebook Page and content you own when testing.
- Do not invoke the main workflow as a lint/syntax test: it may publish a Reel.
- Do not paste secrets into Actions logs or upload real sensitive media.
- Review repository visibility and historical public Actions runs/artifacts for unintended disclosure.
- If credentials might have been exposed before the repo became public, rotate them and revoke old tokens.
