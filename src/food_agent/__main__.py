import logging
import shutil
import sys

from dotenv import load_dotenv

from .bot import FoodBot
from .config import ConfigError, load_config


def main() -> None:
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    try:
        config = load_config()
    except ConfigError as exc:
        sys.exit(f"設定有問題：{exc}")
    if shutil.which("claude") is None:
        sys.exit("找不到 claude 指令，請先安裝 Claude Code 並登入。")

    config.photos_dir.mkdir(parents=True, exist_ok=True)
    FoodBot(config).run(config.discord_token, log_handler=None)


if __name__ == "__main__":
    main()
