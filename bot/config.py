import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    discord_token: str
    openrouter_api_key: str
    openrouter_model: str
    intro_channel_id: int
    watched_channel_ids: frozenset[int]
    log_channel_id: int | None
    dry_run: bool

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            discord_token=_required("DISCORD_TOKEN"),
            openrouter_api_key=_required("OPENROUTER_API_KEY"),
            openrouter_model=os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash"),
            intro_channel_id=int(_required("INTRO_CHANNEL_ID")),
            watched_channel_ids=frozenset(_parse_ids(_required("WATCHED_CHANNEL_IDS"))),
            log_channel_id=_optional_int("LOG_CHANNEL_ID"),
            dry_run=_parse_bool(os.getenv("DRY_RUN", "false")),
        )


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"missing required env var: {name}")
    return value


def _optional_int(name: str) -> int | None:
    value = os.getenv(name)
    return int(value) if value else None


def _parse_ids(raw: str) -> list[int]:
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def _parse_bool(raw: str) -> bool:
    return raw.strip().lower() in {"1", "true", "yes", "on"}
