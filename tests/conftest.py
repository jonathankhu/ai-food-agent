from pathlib import Path

import pytest

from food_agent.config import Config


@pytest.fixture
def config(tmp_path: Path) -> Config:
    return Config(
        discord_token="test-token",
        channel_id=111,
        claude_model="test-model",
        data_dir=tmp_path / "data",
        daily_photo_limit=3,
    )
