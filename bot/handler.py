import logging

import discord

from bot.actions.move import MoveService
from bot.config import Config
from bot.detection.detector import ResumeDetector
from bot.move_tracker import MoveTracker

log = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, config: Config, detector: ResumeDetector, mover: MoveService):
        self._config = config
        self._detector = detector
        self._mover = mover
        self._tracker = MoveTracker(
            max_moves=config.max_moves_per_window,
            window_seconds=config.move_window_seconds,
        )

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

        if not self._tracker.can_move(message.author.id):
            await self._delete_only(message)
            return

        link = await self._mover.move(message)
        if link is not None:
            self._tracker.record(message.author.id)

    async def _delete_only(self, message: discord.Message) -> None:
        try:
            await message.delete()
            log.info(
                "rate-limited: deleted message %s by %s (%s already moved within window)",
                message.id,
                message.author,
                message.author.id,
            )
        except discord.HTTPException:
            log.exception("failed to delete rate-limited message %s", message.id)

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
