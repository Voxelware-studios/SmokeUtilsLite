import datetime
import discord
from discord.ext import commands
from bootstrap.bot_boot import *

# Helper to verify whether the invoking user has a higher role than the target.
def _is_higher_role(member: discord.Member, target: discord.Member) -> bool:
    return member.guild.owner_id == member.id or member.top_role > target.top_role


@bot.hybrid_command(name="mute", description="Mute a member using timeout")
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def mute(
    ctx: commands.Context,
    member: discord.Member,
    minutes: int = 10,
    reason: str = "No reason provided",
):
    # Command only works inside a guild.
    if ctx.guild is None:
        await ctx.reply("This command can only be used in a server.")
        return

    # Prevent users from muting themselves.
    if member == ctx.author:
        await ctx.reply("You cannot mute yourself.")
        return

    # Ensure the invoker can actually moderate the target member.
    if not _is_higher_role(ctx.author, member):
        await ctx.reply("You cannot mute a member with an equal or higher role.")
        return

    # Apply a timeout until the requested time.
    until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
    await member.edit(timed_out_until=until, reason=reason)
    await ctx.reply(f"Muted {member.mention} for {minutes} minute{'s' if minutes != 1 else ''}. Reason: {reason}")
