import logging

import discord

from bot.config import Config
from bot.detection.classifier import OpenRouterClassifier
from bot.detection.detector import ResumeDetector
from bot.handler import MessageHandler

log = logging.getLogger(__name__)


class ResumeFilterBot(discord.Client):
    def __init__(self, config: Config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
        self._config = config
        classifier = OpenRouterClassifier(
            api_key=config.openrouter_api_key,
            model=config.openrouter_model,
        )
        detector = ResumeDetector(classifier)
        self._handler = MessageHandler(self, config, detector)

    async def on_ready(self) -> None:
        user = self.user
        log.info("logged in as %s (id=%s)", user, user.id if user else None)
        log.info(
            "watching %d channel(s), reposting to %s, dry_run=%s",
            len(self._config.watched_channel_ids),
            self._config.intro_channel_id,
            self._config.dry_run,
        )

    async def on_message(self, message: discord.Message) -> None:
        await self._handler.handle(message)
