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


def fallback_details(agent_name: str) -> dict[str, str]:
    details = {
        "source_status": (
            "No approved live source connector is configured for this agent yet. "
            "No external facts were collected in this run."
        ),
        "today_result": "No verified updates are available from configured sources.",
        "notification_status": "No Notification. There is no verified item requiring attention.",
        "next_steps": "- Configure approved sources before treating this report as intelligence.",
        "summary": "No verified source data is available for this run.",
        "signals": "- No verified live signals available.",
        "open_questions": "- Which approved sources should this agent query?",
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
        "today_recommended_actions": "- No action recommended without verified source reports.",
        "sync_to_knowledge_hub": "No. No verified item is ready to sync.",
    }

    if agent_name in ("event-radar", "Polaris Event Radar"):
        details.update(
            {
                "source_status": "External search sources are not connected yet. No live event search was performed.",
                "today_result": "No verifiable important new AI, agent, insurance AI, data, analytics, cloud, or platform events are available from configured sources.",
                "notification_status": "No Notification. There is no verified event requiring attention today.",
                "next_steps": "- Connect approved external search sources.\n- Rerun Event Radar after sources are available.\n- Keep any unverified event leads out of the report until they can be cited.",
                "summary": "External event search is not connected yet, so this report contains only a source-status fallback.",
                "signals": "- No verified important new events available.",
                "open_questions": "- Which event sources should be approved for Event Radar?",
            }
        )
    elif agent_name == "insurance-brief":
        details.update(
            {
                "source_status": "External news and insurance AI sources are not connected yet. No live insurance intelligence collection was performed.",
                "today_result": "No verifiable important insurance, market, regulatory, product, distribution, claims, or insurance AI intelligence is available from configured sources.",
                "notification_status": "No Notification. There is no verified insurance intelligence item requiring attention today.",
                "next_steps": "- Connect approved insurance news, regulator, insurer, and AI source feeds.\n- Rerun Insurance Brief after sources are available.\n- Do not add market claims without citations.",
                "summary": "Insurance and insurance AI source collection is not connected yet, so this report contains only a source-status fallback.",
                "signals": "- No verified insurance or insurance AI signals available.",
                "implications": "- No implications can be drawn without verified source data.",
                "follow_ups": "- Approve insurance market and AI sources for future runs.",
            }
        )
    elif agent_name == "mail-watch":
        details.update(
            {
                "source_status": "Gmail or email data sources are not connected yet. No mailbox review was performed.",
                "today_result": "No actionable email, reply, deadline, or decision item can be determined from configured sources.",
                "notification_status": "No Notification. There is no verified email item requiring attention today.",
                "next_steps": "- Connect or provide approved email summaries.\n- Rerun Mail Watch after mailbox access or input is available.\n- Do not copy sensitive full email bodies into reports.",
                "summary": "Mailbox collection is not connected yet, so this report contains only a source-status fallback.",
                "needs_attention": "- No actionable email items available.",
                "waiting_or_fyi": "- No waiting or FYI email items available.",
                "follow_ups": "- Provide approved mailbox access or safe email summaries.",
            }
        )
    elif agent_name == "notification-hub":
        details.update(
            {
                "source_status": "Notification Hub has not read actual Event Radar, Insurance Brief, or Mail Watch results in this runner path yet.",
                "today_result": "There is no verified downstream signal available for Notification Hub to evaluate.",
                "notification_status": "No Notification. There is no basis for High or Medium priority today.",
                "next_steps": "- Run or provide the latest Event Radar, Insurance Brief, and Mail Watch reports.\n- Update Notification Hub to read downstream reports before making priority decisions.\n- Keep High and Medium empty until there is verified downstream evidence.",
                "summary": "Notification Hub has not read actual downstream report results yet.",
                "high_priority": "- None. There is no verifiable basis for High Priority.",
                "medium_priority": "- None. There is no verifiable basis for Medium Priority.",
                "fyi": "- No verified FYI items available.",
                "mail_watch": "- No verified Mail Watch items available.",
                "recommended_reading_time": "0 minutes.",
                "today_recommended_actions": "- No action recommended until downstream reports are available and reviewed.",
                "sync_to_knowledge_hub": "No. No verified downstream item is ready to sync.",
            }
        )
    return details


def build_fallback_report(agent: dict[str, str], prompt: str, template: str) -> str:
    today = date.today().isoformat()
    agent_name = agent["name"]
    details = fallback_details(agent_name)
    common_values = {
        "report_date": today,
        "agent_name": agent_name,
        "mission": agent.get("mission", "No mission configured."),
        **details,
    }
    rendered = template.format(**common_values)
    return rendered.rstrip() + "\n"


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
    if not report.strip():
        report = build_fallback_report(agent, prompt, template)
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
