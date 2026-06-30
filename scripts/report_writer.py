from __future__ import annotations

from datetime import date
from pathlib import Path


def dated_report_path(output_dir: str | Path, report_date: date | None = None) -> Path:
    current_date = report_date or date.today()
    return Path(output_dir) / f"{current_date.isoformat()}.md"


def write_report(output_dir: str | Path, content: str, report_date: date | None = None) -> Path:
    path = dated_report_path(output_dir, report_date)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.strip():
        current_date = (report_date or date.today()).isoformat()
        content = (
            f"# Polaris Report - {current_date}\n\n"
            "## Source Status\n"
            "Report generation returned empty content. No source data was written.\n\n"
            "## Next Steps\n"
            "- Rerun the agent after checking its prompt, template, and source configuration.\n"
        )
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return path
