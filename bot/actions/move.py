import logging

import discord

from bot.actions.log import log_action
from bot.actions.notify import notify_user
from bot.actions.repost import repost_as_user
from bot.config import Config

log = logging.getLogger(__name__)


class MoveService:
    def __init__(self, client: discord.Client, config: Config):
        self._client = client
        self._config = config

    async def move(self, message: discord.Message) -> str | None:
        target = self._client.get_channel(self._config.intro_channel_id)
        if not isinstance(target, discord.TextChannel):
            log.error("intro channel %s missing or not a text channel", self._config.intro_channel_id)
            return None

        source_name = getattr(message.channel, "name", "channel")

        try:
            reposted = await repost_as_user(target, message)
        except discord.HTTPException:
            log.exception("webhook repost failed for message %s", message.id)
            return None

        link = _message_link(target.guild.id, target.id, reposted.id)

        try:
            await message.delete()
        except discord.HTTPException:
            log.exception("failed to delete original message %s", message.id)

        dm_sent = await notify_user(message.author, source_name, target.name, link)

        log_channel = self._resolve_log_channel()
        await log_action(log_channel, message.author, source_name, target.name, link, dm_sent)

        log.info("moved message %s by %s (%s) → %s", message.id, message.author, message.author.id, link)
        return link

    def _resolve_log_channel(self) -> discord.TextChannel | None:
        if self._config.log_channel_id is None:
            return None
        channel = self._client.get_channel(self._config.log_channel_id)
        return channel if isinstance(channel, discord.TextChannel) else None


def _message_link(guild_id: int, channel_id: int, message_id: int) -> str:
    return f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
