"""讀取 .env 設定，缺任何必要項目就在啟動時明確說缺什麼。"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

REQUIRED = ("DISCORD_TOKEN", "CHANNEL_ID", "CLAUDE_MODEL", "DATA_DIR")
DEFAULT_DAILY_PHOTO_LIMIT = 15


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Config:
    discord_token: str
    channel_id: int
    claude_model: str
    data_dir: Path
    daily_photo_limit: int

    @property
    def photos_dir(self) -> Path:
        return self.data_dir / "photos"

    @property
    def log_path(self) -> Path:
        return self.data_dir / "food-log.xlsx"


def load_config(env: Mapping[str, str] | None = None) -> Config:
    env = os.environ if env is None else env
    missing = [key for key in REQUIRED if not env.get(key, "").strip()]
    if missing:
        raise ConfigError(f".env 缺少設定：{'、'.join(missing)}")

    try:
        channel_id = int(env["CHANNEL_ID"].strip())
    except ValueError:
        raise ConfigError("CHANNEL_ID 必須是純數字") from None

    raw_limit = env.get("DAILY_PHOTO_LIMIT", "").strip()
    try:
        limit = int(raw_limit) if raw_limit else DEFAULT_DAILY_PHOTO_LIMIT
    except ValueError:
        raise ConfigError("DAILY_PHOTO_LIMIT 必須是整數") from None
    if limit < 1:
        raise ConfigError("DAILY_PHOTO_LIMIT 必須至少是 1")

    return Config(
        discord_token=env["DISCORD_TOKEN"].strip(),
        channel_id=channel_id,
        claude_model=env["CLAUDE_MODEL"].strip(),
        data_dir=Path(env["DATA_DIR"].strip()).expanduser().resolve(),
        daily_photo_limit=limit,
    )
