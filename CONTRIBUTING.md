# Contributing

Thank you for considering improvements to this project. Please note that the maintainer has **not yet selected an OSI-approved license**. Discuss licensing with the maintainer before substantial third-party code contributions.

## Suggested contribution process

1. Open a GitHub Issue describing the problem or proposal; **never post credentials or sensitive URLs**.
2. For a code change, create a feature branch and submit a pull request with a concise summary of the change and its expected impact.
3. Include a test plan that does **not** publish unintended Facebook Reels.
4. Explain how you verified it, which secrets/events are required, and whether it changes public publishing behavior.
5. Update README and documentation when configuration, events or behavior changes.

## Pull request checklist

- [ ] No credentials, token values, private URLs, private chat IDs or personal data committed
- [ ] Changes are small and reviewable
- [ ] Input validation and error handling considered
- [ ] Shell/YAML changes checked for quoting and injection hazards
- [ ] Verified behavior in a safe/test environment, or clearly marked as untested
- [ ] No unintended Facebook Page publication; if a live test was performed, its details are documented without secrets
- [ ] Documentation updated where necessary

## Areas for help

See [docs/ROADMAP.md](docs/ROADMAP.md): a non-publishing test path, safer handling of request data, dependency pinning, better status reporting, and a self-hostable Telegram-to-GitHub bridge are particularly useful.
