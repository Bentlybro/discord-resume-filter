import discord

WEBHOOK_NAME = "intro-redirect"


async def get_or_create_webhook(channel: discord.TextChannel) -> discord.Webhook:
    for wh in await channel.webhooks():
        if wh.name == WEBHOOK_NAME:
            return wh
    return await channel.create_webhook(name=WEBHOOK_NAME)


async def repost_as_user(
    target: discord.TextChannel,
    message: discord.Message,
) -> discord.WebhookMessage:
    webhook = await get_or_create_webhook(target)
    files = [await a.to_file() for a in message.attachments] if message.attachments else []
    return await webhook.send(
        content=message.content or "\u200b",
        username=message.author.display_name,
        avatar_url=message.author.display_avatar.url,
        files=files,
        suppress_embeds=True,
        wait=True,
    )
