import logging
import re

import discord
from discord import app_commands

from bot.actions.move import MoveService

log = logging.getLogger(__name__)

URL_PATTERN = re.compile(r"discord(?:app)?\.com/channels/(\d+)/(\d+)/(\d+)")


def setup_move_commands(tree: app_commands.CommandTree, mover: MoveService) -> None:
    @tree.command(
        name="move",
        description="Move a message to the intro channel (mod only)",
    )
    @app_commands.describe(message="Message URL or ID to move (ID = current channel)")
    @app_commands.default_permissions(manage_messages=True)
    async def move_command(interaction: discord.Interaction, message: str) -> None:
        await _handle_slash(interaction, message, mover)

    @tree.context_menu(name="Move to intro")
    @app_commands.default_permissions(manage_messages=True)
    async def move_context(interaction: discord.Interaction, message: discord.Message) -> None:
        await _handle_context(interaction, message, mover)


async def _handle_slash(interaction: discord.Interaction, raw: str, mover: MoveService) -> None:
    await interaction.response.defer(ephemeral=True)
    if not _can_use(interaction):
        await interaction.followup.send("You need Manage Messages permission to use this.", ephemeral=True)
        return

    message = await _resolve_message(interaction, raw.strip())
    if message is None:
        await interaction.followup.send(
            "Couldn't find that message. Pass a Discord message URL, or a message ID from this channel.",
            ephemeral=True,
        )
        return

    await _do_move_and_reply(interaction, message, mover)


async def _handle_context(
    interaction: discord.Interaction,
    message: discord.Message,
    mover: MoveService,
) -> None:
    await interaction.response.defer(ephemeral=True)
    if not _can_use(interaction):
        await interaction.followup.send("You need Manage Messages permission to use this.", ephemeral=True)
        return
    await _do_move_and_reply(interaction, message, mover)


async def _do_move_and_reply(
    interaction: discord.Interaction,
    message: discord.Message,
    mover: MoveService,
) -> None:
    if message.webhook_id is not None or message.author.bot:
        await interaction.followup.send("That's a bot/webhook message — refusing.", ephemeral=True)
        return

    link = await mover.move(message)
    if link:
        await interaction.followup.send(f"Moved → {link}", ephemeral=True)
    else:
        await interaction.followup.send("Move failed — check the bot logs.", ephemeral=True)


def _can_use(interaction: discord.Interaction) -> bool:
    if not isinstance(interaction.user, discord.Member):
        return False
    return interaction.user.guild_permissions.manage_messages


_MESSAGEABLE = (
    discord.TextChannel,
    discord.Thread,
    discord.VoiceChannel,
    discord.StageChannel,
    discord.DMChannel,
)


async def _resolve_message(interaction: discord.Interaction, raw: str) -> discord.Message | None:
    url_match = URL_PATTERN.search(raw)
    if url_match:
        guild_id, channel_id, message_id = (int(g) for g in url_match.groups())
        if interaction.guild_id != guild_id or interaction.guild is None:
            return None
        channel = interaction.guild.get_channel_or_thread(channel_id)
        if not isinstance(channel, _MESSAGEABLE):
            return None
        try:
            return await channel.fetch_message(message_id)
        except discord.HTTPException:
            return None

    if raw.isdigit() and isinstance(interaction.channel, _MESSAGEABLE):
        try:
            return await interaction.channel.fetch_message(int(raw))
        except discord.HTTPException:
            return None

    return None
