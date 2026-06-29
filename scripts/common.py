from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SUPPORTED_AGENTS = ("event-radar", "insurance-brief", "mail-watch", "daily")


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_simple_yaml(path: str | Path) -> dict[str, str]:
    """Read the small key/value YAML files used by agent definitions."""
    data: dict[str, str] = {}
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def load_agent_config(agent_name: str) -> dict[str, str]:
    if agent_name not in SUPPORTED_AGENTS:
        supported = ", ".join(SUPPORTED_AGENTS)
        raise ValueError(f"Unknown agent '{agent_name}'. Supported agents: {supported}")

    path = ROOT_DIR / "agents" / f"{agent_name}.yaml"
    config = read_simple_yaml(path)
    required = ("name", "mission", "schedule", "output_dir", "prompt_file")
    missing = [key for key in required if not config.get(key)]
    if missing:
        missing_keys = ", ".join(missing)
        raise ValueError(f"Agent config {path} is missing: {missing_keys}")
    return config


def has_configured_sources(agent_name: str) -> bool:
    """Return whether config/sources.yaml has non-empty sources for the agent."""
    path = ROOT_DIR / "config" / "sources.yaml"
    if not path.exists():
        return False

    target = f"{agent_name}:"
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or not line.startswith(target):
            continue
        value = line.split(":", 1)[1].strip()
        return value not in ("", "[]")
    return False
