import logging

from bot.client import ResumeFilterBot
from bot.config import Config


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    config = Config.from_env()
    bot = ResumeFilterBot(config)
    bot.run(config.discord_token, log_handler=None)


if __name__ == "__main__":
    main()
