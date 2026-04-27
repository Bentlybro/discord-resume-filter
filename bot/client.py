import logging

import discord
from discord import app_commands

from bot.actions.move import MoveService
from bot.commands.move import setup_move_commands
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
        self.tree = app_commands.CommandTree(self)
        classifier = OpenRouterClassifier(
            api_key=config.openrouter_api_key,
            model=config.openrouter_model,
        )
        detector = ResumeDetector(classifier)
        self._mover = MoveService(self, config)
        self._handler = MessageHandler(config, detector, self._mover)
        setup_move_commands(self.tree, self._mover)

    async def setup_hook(self) -> None:
        if self._config.sync_guild_id is not None:
            guild = discord.Object(id=self._config.sync_guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            log.info("synced %d commands to guild %s", len(synced), self._config.sync_guild_id)
        else:
            synced = await self.tree.sync()
            log.info("synced %d commands globally (may take up to 1 hour to appear)", len(synced))

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
