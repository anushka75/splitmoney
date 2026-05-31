import json
import os
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"
DOTENV_PATH = Path(__file__).resolve().parent.parent / ".env"
CONFIG: dict[str, Any] | None = None


def _load_dotenv() -> dict[str, str]:
    values: dict[str, str] = {}
    if not DOTENV_PATH.exists():
        return values

    with open(DOTENV_PATH, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def load_config() -> dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    dotenv_values = _load_dotenv()
    database_url = os.getenv("DATABASE_URL") or dotenv_values.get("DATABASE_URL")
    if database_url:
        config["database_url"] = database_url

    cors_origins = os.getenv("CORS_ORIGINS") or dotenv_values.get("CORS_ORIGINS")
    if cors_origins:
        config["cors_origins"] = [
            origin.strip() for origin in cors_origins.split(",") if origin.strip()
        ]

    return config


def init_config(config: dict[str, Any]) -> None:
    global CONFIG
    CONFIG = config


def get_config() -> dict[str, Any]:
    if CONFIG is None:
        raise RuntimeError("Config not initialized. Call bootstrap first.")
    return CONFIG
