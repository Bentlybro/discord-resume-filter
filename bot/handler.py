import logging

import discord

from bot.actions.log import log_action
from bot.actions.notify import notify_user
from bot.actions.repost import repost_as_user
from bot.config import Config
from bot.detection.detector import ResumeDetector

log = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, client: discord.Client, config: Config, detector: ResumeDetector):
        self._client = client
        self._config = config
        self._detector = detector

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

        await self._move_message(message)

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

    async def _move_message(self, message: discord.Message) -> None:
        target = self._client.get_channel(self._config.intro_channel_id)
        if not isinstance(target, discord.TextChannel):
            log.error("intro channel %s missing or not a text channel", self._config.intro_channel_id)
            return

        source_name = getattr(message.channel, "name", "channel")

        try:
            reposted = await repost_as_user(target, message)
        except discord.HTTPException:
            log.exception("webhook repost failed for message %s", message.id)
            return

        link = _message_link(target.guild.id, target.id, reposted.id)

        try:
            await message.delete()
        except discord.HTTPException:
            log.exception("failed to delete original message %s", message.id)

        dm_sent = await notify_user(message.author, source_name, target.name, link)

        log_channel = self._resolve_log_channel()
        await log_action(log_channel, message.author, source_name, target.name, link, dm_sent)

        log.info("moved message %s by %s (%s) → %s", message.id, message.author, message.author.id, link)

    def _resolve_log_channel(self) -> discord.TextChannel | None:
        if self._config.log_channel_id is None:
            return None
        channel = self._client.get_channel(self._config.log_channel_id)
        return channel if isinstance(channel, discord.TextChannel) else None


def _message_link(guild_id: int, channel_id: int, message_id: int) -> str:
    return f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
