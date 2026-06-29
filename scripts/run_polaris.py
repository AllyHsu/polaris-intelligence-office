from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from common import ROOT_DIR, SUPPORTED_AGENTS, has_configured_sources, load_agent_config, read_text
from report_writer import write_report


OPENAI_URL = "https://api.openai.com/v1/responses"


def build_fallback_report(agent: dict[str, str], prompt: str, template: str) -> str:
    today = date.today().isoformat()
    source_status = (
        "Live source collection was not performed. "
        "TODO: connect approved search, mail, document, or business data sources before treating this report as intelligence."
    )
    common_values = {
        "report_date": today,
        "summary": f"No live data was collected for `{agent['name']}` on {today}. This is a mock fallback shell only.",
        "signals": "- No verified live signals available.",
        "open_questions": "- Which approved sources should this agent query?",
        "source_status": source_status,
        "implications": "- No implications can be drawn without source data.",
        "follow_ups": "- Configure sources and rerun the agent.",
        "needs_attention": "- No mailbox data available.",
        "waiting_or_fyi": "- No mailbox data available.",
        "events": "- No event-radar output available.",
        "insurance": "- No insurance-brief output available.",
        "mail": "- No mail-watch output available.",
        "high_priority": "- No High priority items available.",
        "medium_priority": "- No Medium priority items available.",
        "fyi": "- No FYI items available.",
        "mail_watch": "- No Mail Watch items available.",
        "recommended_reading_time": "0 minutes.",
        "today_recommended_actions": "- No action recommended without downstream source reports.",
        "sync_to_knowledge_hub": "No. No verified item is ready to sync.",
    }
    rendered = template.format(**common_values)
    return rendered + "\n\n<!-- Prompt loaded for this run; omitted from fallback output to keep the report concise. -->\n"


def call_openai(agent: dict[str, str], prompt: str, template: str) -> str:
    # TODO: Replace this guard with real source collection once approved sources are configured.
    if not has_configured_sources(agent["name"]):
        return build_fallback_report(agent, prompt, template)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return build_fallback_report(agent, prompt, template)

    user_message = (
        f"Agent: {agent['name']}\n"
        f"Mission: {agent['mission']}\n"
        f"Report date: {date.today().isoformat()}\n\n"
        "Use the following report template and fill it only with verified or explicitly unavailable information.\n\n"
        f"{template}"
    )
    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        "input": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ],
    }
    request = urllib.request.Request(
        OPENAI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        fallback = build_fallback_report(agent, prompt, template)
        return fallback + f"\n<!-- OpenAI call failed; fallback used. Error: {exc} -->\n"

    try:
        return body["output"][0]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        fallback = build_fallback_report(agent, prompt, template)
        return fallback + "\n<!-- OpenAI response shape was unexpected; fallback used. -->\n"


def run(agent_name: str) -> Path:
    agent = load_agent_config(agent_name)
    prompt = read_text(ROOT_DIR / agent["prompt_file"])
    template_file = agent.get("template_file", f"templates/{agent_name}-report.md")
    template = read_text(ROOT_DIR / template_file)
    report = call_openai(agent, prompt, template)
    return write_report(ROOT_DIR / agent["output_dir"], report)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Polaris Intelligence Office agent.")
    parser.add_argument("agent", choices=SUPPORTED_AGENTS)
    args = parser.parse_args()

    report_path = run(args.agent)
    print(f"Wrote {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
