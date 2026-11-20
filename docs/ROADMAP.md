# Engineering roadmap

This is a proposed improvement plan, **not a claim that the items are already implemented**.

## P0 — Security and correctness (before broad adoption)

- [ ] Verify the original repo and historical public Actions runs/artifacts for exposed credentials, private video URLs and chat identifiers; revoke/rotate as needed.
- [ ] Validate URLs and all `repository_dispatch` inputs. Reject unexpected multiline/control characters; safely write any values to `GITHUB_ENV`.
- [ ] Set download size, duration and execution time limits; review URL schemes and network access risks for untrusted media URLs.
- [ ] Harden the optional external Telegram bridge with an authorized-user/chat allowlist, rate limits, replay protection and narrowly scoped GitHub credential.
- [ ] Remove or sanitize sensitive API-response and error logging.
- [ ] Make success/failure notifications reflect actual publication status; **avoid marking an already published Reel as a publishing failure** because Telegram/artifact delivery failed.
- [ ] Implement a non-publishing test path (mock Graph API/Telegram) before refactoring the live workflow.

## P1 — Reliability and reproducibility

- [ ] Pin reviewed Actions dependencies to immutable SHAs, and use stable `yt-dlp` versions with an intentional update policy.
- [ ] Review `ubuntu-latest` and supported Graph API version upgrades deliberately rather than relying on moving defaults.
- [ ] Add shell/YAML linting and a safe CI job that never publishes.
- [ ] Add idempotency for dispatched jobs to protect against repeated Facebook posts.
- [ ] Add retries/backoff for temporary Meta/Telegram errors and clear terminal-state handling.
- [ ] Split download, normalization, Meta publishing and Telegram notification into separate scripts/modules with tests.

## P2 — Community readiness

- [ ] Select an OSI-approved license **with the copyright owner's explicit consent** and verify third-party obligations.
- [ ] Add sanitized example screenshots and a short walkthrough video using owned test media.
- [ ] Publish a minimal reference Telegram bridge with documentation, authorization controls and safe secrets handling.
- [ ] Add release notes, contribution guidelines for tests and issue templates.
- [ ] Track real usage, external contributions and independent adoption; do not inflate GitHub activity or claim fabricated impact.

## Release checklist

- [ ] Demonstrated end-to-end in a dedicated test Page
- [ ] No secret exposed in Git history or publicly accessible logs
- [ ] Safe negative tests (bad URL, expired token, short video, Telegram unavailable)
- [ ] Docs and input contract match code
- [ ] License chosen and clearly stated
- [ ] Owner has approved a release and its actual publishing behavior
