import json
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"
CONFIG: dict[str, Any] | None = None


def load_config() -> dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def init_config(config: dict[str, Any]) -> None:
    global CONFIG
    CONFIG = config


def get_config() -> dict[str, Any]:
    if CONFIG is None:
        raise RuntimeError("Config not initialized. Call bootstrap first.")
    return CONFIG
