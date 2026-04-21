import discord

DM_TEMPLATE = (
    "Hey {name}! I moved your message from **#{source}** to **#{target}** — "
    "it looked like an introduction or a services pitch, and we keep those "
    "in the **#{target}** channel to keep **#{source}** less cluttered.\n\n"
    "Your message is still there, just in the right place now:\n{link}\n\n"
    "If this was a mistake, please let a mod know!"
)


async def notify_user(
    user: discord.User | discord.Member,
    source_channel_name: str,
    target_channel_name: str,
    moved_message_link: str,
) -> bool:
    try:
        await user.send(
            DM_TEMPLATE.format(
                name=user.display_name,
                source=source_channel_name,
                target=target_channel_name,
                link=moved_message_link,
            )
        )
        return True
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return False
