# Local Codex Workflow

Polaris Intelligence Office is designed to run from local Codex. GitHub is only for version management: commit the prompts, scripts, configs, templates, and finished reports when you want to save history or push changes.

## Open Codex

1. Open the Codex desktop app.
2. Open this workspace folder:

```text
C:\Users\User\Documents\Codex\2026-06-30\google-drive-plugin-google-drive-openai
```

3. Ask Codex to read the relevant files before running an agent:

```text
Please read agents/{agent-name}.yaml and prompts/{prompt-file}. Then run the Polaris agent locally and write the report to reports/{agent-name}/YYYY-MM-DD.md. Do not invent facts. If source access is unavailable, list the missing source as TODO.
```

## Run Polaris Event Radar

Ask Codex:

```text
Run Polaris Event Radar locally.
Read agents/event-radar.yaml and prompts/polaris-event-radar.md.
Use only sources you can access or clearly cite. If external search is unavailable, write TODOs instead of fake data.
Save the Markdown report to reports/event-radar/YYYY-MM-DD.md.
```

Optional script fallback:

```bash
python scripts/run_polaris.py event-radar
```

## Run Polaris Insurance Brief

Ask Codex:

```text
Run Polaris Insurance Brief locally.
Read agents/insurance-brief.yaml and prompts/polaris-insurance-brief.md.
Use only accessible, cited, or user-provided sources. If source access is unavailable, write TODOs instead of fake data.
Save the Markdown report to reports/insurance-brief/YYYY-MM-DD.md.
```

Optional script fallback:

```bash
python scripts/run_polaris.py insurance-brief
```

## Run Polaris Mail Watch

Ask Codex:

```text
Run Polaris Mail Watch locally.
Read agents/mail-watch.yaml and prompts/polaris-mail-watch.md.
Use only mail or message sources I explicitly provide or connect. Do not expose sensitive content unnecessarily.
Save the Markdown report to reports/mail-watch/YYYY-MM-DD.md.
```

Optional script fallback:

```bash
python scripts/run_polaris.py mail-watch
```

## Confirm Report Output

Check that the expected dated file exists:

```bash
dir reports\event-radar
dir reports\insurance-brief
dir reports\mail-watch
```

Each report should use this naming pattern:

```text
reports/{agent-name}/YYYY-MM-DD.md
```

Before committing, open the report and confirm:

- The date is correct.
- Source status is clear.
- External facts include sources when available.
- Missing source access is marked as TODO.
- No API keys, passwords, private customer data, or company secrets are included.

## Git Commit

Review changes:

```bash
git status
git diff
```

Stage the intended files:

```bash
git add README.md docs agents prompts scripts config templates reports
```

Commit:

```bash
git commit -m "Update Polaris local Codex workflow"
```

## Git Push

Push the current branch:

```bash
git push
```

If the branch has no upstream yet:

```bash
git push -u origin main
```

Use the actual branch name if it is not `main`.

## If Push Fails

1. Run `git status` and confirm the commit exists locally.
2. Run `git remote -v` and confirm the GitHub repository URL is correct.
3. Sign in to GitHub from your terminal or Git client if authentication failed.
4. Pull first if the remote branch has newer commits:

```bash
git pull --rebase
git push
```

5. If authentication still fails, push from a terminal where GitHub authentication already works, or update the repository credential in your Git client.
