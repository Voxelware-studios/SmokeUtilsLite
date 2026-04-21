import asyncio
import datetime
import random
import re

import discord
from discord.ext import commands
from bootstrap.bot_boot import *
from logic.giveaway import get_all_giveaways, get_giveaway, remove_giveaway, set_giveaway

# Regex used to parse simple duration values like "10" or "10m".
DURATION_RE = re.compile(r"^(\d+)(?:m)?$")


def parse_duration(duration: str | None) -> int:
    # Convert a human-friendly duration string into minutes.
    if not duration:
        return 0

    duration = duration.strip().lower()
    match = DURATION_RE.fullmatch(duration)
    if not match:
        return -1

    return int(match.group(1))


def format_duration(ends_at: int | None) -> str:
    # Format the end timestamp for display.
    if not ends_at:
        return "Manual end"
    return f"<t:{ends_at}:R>"


async def _complete_giveaway(guild: discord.Guild, active: dict, manual: bool = True):
    # Finish the giveaway and announce winners.
    channel = guild.get_channel(active["channel_id"])
    if channel is None:
        remove_giveaway(guild.id)
        return

    try:
        message = await channel.fetch_message(active["message_id"])
    except discord.NotFound:
        remove_giveaway(guild.id)
        return

    reaction = discord.utils.get(message.reactions, emoji="🎉")
    if not reaction:
        remove_giveaway(guild.id)
        return

    users = [user async for user in reaction.users() if not user.bot]
    if not users:
        remove_giveaway(guild.id)
        return

    winner_count = min(active["winners"], len(users))
    winners = random.sample(users, winner_count)
    winner_mentions = ", ".join(w.mention for w in winners)

    ended_embed = discord.Embed(
        title="🎉 GIVEAWAY ENDED (MANUAL) 🎉" if manual else "🎉 GIVEAWAY ENDED 🎉",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow(),
    )
    ended_embed.add_field(name="Prize", value=active["prize"], inline=False)
    ended_embed.add_field(name="Winner(s)", value=winner_mentions, inline=False)
    ended_embed.set_footer(text="Giveaway ended")

    await channel.send(embed=ended_embed)
    remove_giveaway(guild.id)


async def _schedule_giveaway_end(guild_id: int, delay: int):
    # Wait until the giveaway should end, then complete it.
    await asyncio.sleep(delay)
    active = get_giveaway(guild_id)
    if not active:
        return

    guild = bot.get_guild(guild_id)
    if not guild:
        return

    await _complete_giveaway(guild, active, manual=False)


@bot.listen("on_ready")
async def giveaway_ready():
    # Restore active giveaways after the bot starts.
    if getattr(bot, "_giveaway_ready", False):
        return
    bot._giveaway_ready = True

    for guild_id_str, active in get_all_giveaways().items():
        ends_at = active.get("ends_at")
        if not ends_at:
            continue

        remaining = ends_at - int(discord.utils.utcnow().timestamp())
        guild_id = int(guild_id_str)
        if remaining <= 0:
            guild = bot.get_guild(guild_id)
            if guild:
                bot.loop.create_task(_complete_giveaway(guild, active, manual=False))
        else:
            bot.loop.create_task(_schedule_giveaway_end(guild_id, remaining))

@bot.hybrid_group(name="giveaway", description="Manage giveaways")
@commands.has_permissions(manage_guild=True)
async def giveaway_group(ctx: commands.Context):
    # Root command group for the giveaway feature.
    if ctx.invoked_subcommand is None:
        await ctx.reply("Use `/giveaway start` to begin a giveaway or `/giveaway end` to finish one.")


@giveaway_group.command(name="start", description="Start a giveaway")
@commands.has_permissions(manage_guild=True)
async def giveaway_start(
    ctx: commands.Context,
    channel: discord.TextChannel,
    prize: str,
    winners: int = 1,
    duration: str = None,
):
    # Create a new giveaway in a channel.
    if winners < 1:
        await ctx.reply("Winners must be at least 1.")
        return

    active = get_giveaway(ctx.guild.id)
    if active:
        await ctx.reply("A giveaway is already active. End it first with `/giveaway end`.")
        return

    minutes = parse_duration(duration)
    if minutes < 0:
        await ctx.reply("Invalid duration format. Use minutes only, for example `10` or `10m`.")
        return

    now = discord.utils.utcnow()
    ends_at = int((now + datetime.timedelta(minutes=minutes)).timestamp()) if minutes > 0 else None
    ends_text = format_duration(ends_at)

    embed = discord.Embed(
        title="🎉 GIVEAWAY 🎉",
        description="React with 🎉 to enter!",
        color=discord.Color.gold(),
        timestamp=now,
    )
    embed.add_field(name="Prize", value=prize, inline=False)
    embed.add_field(name="Winners", value=str(winners), inline=False)
    embed.add_field(name="Ends", value=ends_text, inline=False)
    embed.set_footer(text="Today at")

    message = await channel.send(embed=embed)
    await message.add_reaction("🎉")

    set_giveaway(ctx.guild.id, {
        "channel_id": channel.id,
        "message_id": message.id,
        "prize": prize,
        "winners": winners,
        "ends_at": ends_at,
        "started_at": int(now.timestamp()),
    })

    if ends_at:
        delay = ends_at - int(discord.utils.utcnow().timestamp())
        if delay > 0:
            bot.loop.create_task(_schedule_giveaway_end(ctx.guild.id, delay))

    await ctx.reply(f"Giveaway started in {channel.mention}.")


@giveaway_group.command(name="end", description="End the active giveaway")
@commands.has_permissions(manage_guild=True)
async def giveaway_end(ctx: commands.Context):
    # End the currently active giveaway.
    active = get_giveaway(ctx.guild.id)
    if not active:
        await ctx.reply("There is no active giveaway to end.")
        return

    guild = ctx.guild
    if guild is None:
        await ctx.reply("This command must be used in a guild.")
        return

    channel = guild.get_channel(active["channel_id"])
    if channel is None:
        remove_giveaway(ctx.guild.id)
        await ctx.reply("Giveaway ended, but the channel could not be found.")
        return

    try:
        message = await channel.fetch_message(active["message_id"])
    except discord.NotFound:
        remove_giveaway(ctx.guild.id)
        await ctx.reply("Giveaway ended, but the giveaway message could not be found.")
        return

    reaction = discord.utils.get(message.reactions, emoji="🎉")
    if not reaction:
        remove_giveaway(ctx.guild.id)
        await ctx.reply("Giveaway ended, but no entries were found.")
        return

    users = []
    async for user in reaction.users():
        if user.bot:
            continue
        users.append(user)

    if not users:
        remove_giveaway(ctx.guild.id)
        await ctx.reply("Giveaway ended, but there were no valid entries.")
        return

    winner_count = min(active["winners"], len(users))
    winners = random.sample(users, winner_count)
    winner_mentions = ", ".join(w.mention for w in winners)

    ended_embed = discord.Embed(
        title="🎉 GIVEAWAY ENDED (MANUAL) 🎉",
        color=discord.Color.green(),
        timestamp=datetime.datetime.utcnow(),
    )
    ended_embed.add_field(name="Prize", value=active["prize"], inline=False)
    ended_embed.add_field(name="Winner(s)", value=winner_mentions, inline=False)
    ended_embed.set_footer(text="Giveaway ended")

    await channel.send(embed=ended_embed)
    remove_giveaway(ctx.guild.id)
    await ctx.reply("Giveaway ended successfully.")