import logging

import discord

from bot.actions.move import MoveService
from bot.config import Config
from bot.detection.detector import ResumeDetector

log = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, config: Config, detector: ResumeDetector, mover: MoveService):
        self._config = config
        self._detector = detector
        self._mover = mover

    async def handle(self, message: discord.Message) -> None:
        if not self._should_process(message):
            return

        try:
            flagged = await self._detector.is_resume(message.content)
        except Exception:
            log.exception("detector failed on message %s", message.id)
            return

        if not flagged:
            return

        if self._config.dry_run:
            log.info("DRY_RUN: would move message %s by %s", message.id, message.author)
            return

        await self._mover.move(message)

    def _should_process(self, message: discord.Message) -> bool:
        if message.author.bot:
            return False
        if message.webhook_id is not None:
            return False
        if message.channel.id == self._config.intro_channel_id:
            return False
        if message.channel.id not in self._config.watched_channel_ids:
            return False
        return bool(message.content)
