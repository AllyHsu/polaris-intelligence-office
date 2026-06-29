# Polaris Intelligence Office v1.0

Polaris Intelligence Office is a local Codex-first intelligence workspace. GitHub is used for version management; the primary operating mode is to run agents from Codex on this machine and save Markdown reports into `reports/`.

## Agents

- `notification-hub`: The single notification entry point for Polaris Intelligence Office.
- `event-radar`: Tracks public events, signals, and industry movements.
- `insurance-brief`: Produces concise insurance market and product briefs.
- `mail-watch`: Summarizes priority mail themes and possible follow-ups.
- `daily`: Optional roll-up brief across Polaris outputs.

## Notification Hub Principle

Polaris Notification Hub is the only entry point for daily attention. It does not search external sources again. It summarizes downstream signals from:

- Polaris Event Radar
- Polaris Insurance Brief
- Polaris Mail Watch

Notification Hub answers three questions:

1. Is there anything important today?
2. What is the most important item?
3. What should I do today?

ChatGPT scheduling, if used, belongs only to the notification layer: reminding, nudging, and asking whether to review the latest Notification Hub output. Codex plus GitHub is the knowledge layer: Codex reads and writes the reports, while GitHub stores version history.

## Local Codex Workflow

Use Codex locally as the main runner. Ask Codex to read the matching agent file and prompt, gather only available or explicitly approved sources, and write the dated Markdown report.

Detailed instructions live in `docs/local-codex-workflow.md`.

## Local Script Fallback

The Python runner is available for creating report shells and checking the folder workflow. It does not require GitHub Actions or an API key.

```bash
python scripts/run_polaris.py event-radar
python scripts/run_polaris.py insurance-brief
python scripts/run_polaris.py mail-watch
python scripts/run_polaris.py notification-hub
```

Each run writes a dated Markdown report to:

```text
reports/{agent-name}/YYYY-MM-DD.md
```

## Configuration

- Agent definitions live in `agents/`.
- Prompts live in `prompts/`.
- Report templates live in `templates/`.
- Source, schedule, and runtime settings live in `config/`.
- Operating procedures live in `docs/`.

No API keys are stored in this repository. `OPENAI_API_KEY` and GitHub Actions are optional, not required for the local Codex workflow.

## Source Status

Live source collection must be explicit. If Codex cannot access or verify a source, the report should say so and include a TODO instead of inventing details.
