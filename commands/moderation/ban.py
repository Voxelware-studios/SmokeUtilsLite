import discord
from discord.ext import commands
from bootstrap.bot_boot import *

# Helper used to ensure the command invoker is higher than the target.
def _is_higher_role(member: discord.Member, target: discord.Member) -> bool:
    return member.guild.owner_id == member.id or member.top_role > target.top_role


@bot.hybrid_command(name="ban", description="Ban a member from the server")
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, reason: str = "No reason provided"):
    # Command must be executed within a guild.
    if ctx.guild is None:
        await ctx.reply("This command can only be used in a server.")
        return

    # Prevent self-ban.
    if member == ctx.author:
        await ctx.reply("You cannot ban yourself.")
        return

    # Prevent banning members with equal or higher role.
    if not _is_higher_role(ctx.author, member):
        await ctx.reply("You cannot ban a member with an equal or higher role.")
        return

    await member.ban(reason=reason)
    await ctx.reply(f"Banned {member.mention}. Reason: {reason}")
