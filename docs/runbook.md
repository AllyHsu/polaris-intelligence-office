# Polaris Runbook

This runbook keeps Polaris Intelligence Office simple: run agents locally in Codex, write Markdown reports, and use GitHub only to version the repo.

## Weekly Thursday Event Radar SOP

1. Open Codex in the Polaris workspace.
2. Ask Codex to read `agents/event-radar.yaml` and `prompts/polaris-event-radar.md`.
3. Ask Codex to search or review only accessible sources for relevant AI, agent, enterprise AI, insurance/financial AI, data, analytics, cloud, and platform events.
4. Require source links or source names for every factual event item.
5. If live search is unavailable, write a TODO section and do not invent events.
6. Save the report to:

```text
reports/event-radar/YYYY-MM-DD.md
```

7. Review the report, then commit it when ready.

## Weekly Insurance Brief SOP

1. Open Codex in the Polaris workspace.
2. Ask Codex to read `agents/insurance-brief.yaml` and `prompts/polaris-insurance-brief.md`.
3. Provide or approve the sources to review, such as public regulator updates, insurer announcements, product pages, industry news, or internal notes safe for the repo.
4. Ask Codex to separate verified facts, implications, follow-ups, and open questions.
5. If source access is unavailable, write a TODO section and do not fabricate market data.
6. Save the report to:

```text
reports/insurance-brief/YYYY-MM-DD.md
```

7. Review the report, then commit it when ready.

## Daily Mail Watch SOP

1. Open Codex in the Polaris workspace.
2. Ask Codex to read `agents/mail-watch.yaml` and `prompts/polaris-mail-watch.md`.
3. Provide only the email snippets, summaries, or connected mail access you want Codex to review.
4. Ask Codex to group items by urgency and recommended next step.
5. Avoid copying sensitive email bodies into the repo. Summarize only what is necessary.
6. If mailbox access is unavailable, write a TODO section and do not invent messages.
7. Save the report to:

```text
reports/mail-watch/YYYY-MM-DD.md
```

8. Review the report, then commit it when ready.

## Naming Rules

- Agent names use lowercase kebab-case: `event-radar`, `insurance-brief`, `mail-watch`.
- Prompt files use `prompts/polaris-{agent-name}.md`.
- Agent files use `agents/{agent-name}.yaml`.
- Template files use `templates/{agent-name}-report.md`.
- Report files use ISO dates: `YYYY-MM-DD.md`.

## Report Output Rules

- Event Radar reports go to `reports/event-radar/YYYY-MM-DD.md`.
- Insurance Brief reports go to `reports/insurance-brief/YYYY-MM-DD.md`.
- Mail Watch reports go to `reports/mail-watch/YYYY-MM-DD.md`.
- Every report should include a source status section.
- If source access is missing, write a clear TODO instead of filling gaps with guesses.
- Do not commit Python cache files, virtual environments, or local secrets.

## Security Reminder

Never write these into the repo:

- API keys or access tokens
- Passwords
- Private keys
- Company confidential material
- Customer personal data
- Full sensitive email bodies
- Internal documents unless they are explicitly approved for this repository

Use summaries and source labels when possible. Keep sensitive details outside Git unless they are explicitly approved for version control.
