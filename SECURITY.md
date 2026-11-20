# Security policy

## Scope and current state

This project controls a public Facebook publishing workflow using sensitive access tokens. **Do not test with a production Facebook Page unless you intentionally want to publish.** This documentation does not constitute a penetration test or a certification of security.

## Report a vulnerability

Please avoid posting exploit details, credentials, personal identifiers or production video links in public GitHub Issues. If **private vulnerability reporting** is enabled in the repository, use GitHub's **Security → Report a vulnerability** flow. Otherwise, contact the maintainer through a private channel and request a secure disclosure method. Public issues are appropriate for non-sensitive bugs only.

## Secrets and permissions

- Store Meta and Telegram tokens exclusively in **GitHub Actions Secrets**, never in YAML, commits, README files, issues, or dispatch requests.
- Scope credentials to the minimum accounts, Pages and permissions necessary. Rotate tokens if you suspect exposure.
- Treat `repository_dispatch` credentials as powerful: only an authenticated, authorized integration should send events; validate allowed Telegram sender/chat IDs at the **external** bot/bridge before invoking GitHub.
- Do not embed user-supplied multiline values directly into `GITHUB_ENV` without safe escaping. The present workflow has areas for hardening; see the roadmap.
- Avoid publishing sensitive video URLs, Telegram chat IDs, or detailed Meta API responses in logs. Check historical logs and one-day artifacts after switching a repository to **Public**.
- A video artifact is available through GitHub Actions while retained; this may be unsuitable for private media.
- Do not share tokens with maintainers for debugging. Reproduce with redacted diagnostics or mock data.

## Responsible use

Use only source media you have permission to download, transform and publish. Comply with source website rules, privacy rights, and Meta/Telegram platform terms. Do not run this workflow on material that belongs to third parties without authorization.

## Planned hardening (not yet implemented)

Input validation and safe environment writes, runtime and size limits, dependency pinning, separate non-publishing tests, least-privilege dispatch handling, and improved logging/failure reporting are tracked in [docs/ROADMAP.md](docs/ROADMAP.md).
