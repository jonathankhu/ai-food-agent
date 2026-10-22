import pytest

from food_agent.config import ConfigError, load_config

GOOD = {"DISCORD_TOKEN": "t", "CHANNEL_ID": "123", "CLAUDE_MODEL": "m", "DATA_DIR": "/tmp/x"}


def test_loads_with_default_limit():
    cfg = load_config(GOOD)
    assert cfg.channel_id == 123 and cfg.daily_photo_limit == 15


def test_missing_items_are_named():
    with pytest.raises(ConfigError, match="DISCORD_TOKEN.*DATA_DIR"):
        load_config({"CHANNEL_ID": "1", "CLAUDE_MODEL": "m"})


def test_bad_values():
    with pytest.raises(ConfigError):
        load_config({**GOOD, "CHANNEL_ID": "abc"})
    with pytest.raises(ConfigError):
        load_config({**GOOD, "DAILY_PHOTO_LIMIT": "0"})
    assert load_config({**GOOD, "DAILY_PHOTO_LIMIT": "1"}).daily_photo_limit == 1
