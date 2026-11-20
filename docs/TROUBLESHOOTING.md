# Troubleshooting

Read the failing step in **Actions → Telegram to Facebook Reel → selected run**. Redact tokens, chat identifiers, private URLs and API responses before sharing any logs.

| Symptom | Common cause / next step |
| --- | --- |
| Workflow button is missing | Check Actions is enabled, default branch contains `.github/workflows/test.yml`, and you have repository access |
| `No video URL received` | `workflow_dispatch.video_url` or `repository_dispatch.client_payload.video_url` is absent |
| Download fails | Source not reachable, yt-dlp extractor no longer works, source authorization required, or website limits automation |
| `No MP4 file found` | Downloaded file not converted/merged as expected; inspect downloaded filenames without sharing private data |
| Input video too short | Current workflow requires at least four seconds |
| Meta upload start fails | Check Page token scope/validity, Page rights and Graph API response; never paste actual token |
| Upload or publish rejected | Check video limitations, API errors, token rights, endpoint version and asset ownership |
| Facebook processing times out | Processing status did not complete within current polling window; inspect actual Page before retrying |
| Failed at final Telegram notification | Reel might have been successfully published already; check Facebook Page before rerun |
| Artifact upload failed | GitHub artifact permissions/storage issue; publication may already be complete |
| Dispatch succeeds but no Telegram message | A valid Telegram chat ID/bot token may be missing; ensure bot is permitted to send to that chat |

## Avoid duplicate publishing

1. Note the current run ID and the Reel/video ID if visible in sanitized logs.
2. Check the actual Facebook Page for a published Reel.
3. If already published, **do not rerun the same request** solely to fix Telegram status or artifact delivery.
4. Fix the failing post-publication step separately.

## Report a reproducible bug

Include sanitized steps to reproduce, the failing **step name**, expected versus observed behavior, and whether a Reel was published. Do not include credentials, real chat IDs or private media.
