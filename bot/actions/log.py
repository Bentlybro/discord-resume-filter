import discord


async def log_action(
    log_channel: discord.TextChannel | None,
    author: discord.User | discord.Member,
    original_channel_name: str,
    target_channel_name: str,
    moved_link: str,
    dm_sent: bool,
) -> None:
    if log_channel is None:
        return
    embed = discord.Embed(
        title="Resume post moved",
        description=f"[Jump to moved message]({moved_link})",
        color=discord.Color.orange(),
    )
    embed.add_field(name="User", value=f"{author.mention} (`{author.id}`)", inline=False)
    embed.add_field(name="From", value=f"#{original_channel_name}", inline=True)
    embed.add_field(name="To", value=f"#{target_channel_name}", inline=True)
    embed.add_field(name="DM sent", value="yes" if dm_sent else "no (DMs closed)", inline=True)
    try:
        await log_channel.send(embed=embed)
    except discord.HTTPException:
        pass
