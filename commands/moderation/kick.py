import discord
from discord.ext import commands
from bootstrap.bot_boot import *

# Helper to compare role hierarchy for kick and ban commands.
def _is_higher_role(member: discord.Member, target: discord.Member) -> bool:
    return member.guild.owner_id == member.id or member.top_role > target.top_role


@bot.hybrid_command(name="kick", description="Kick a member from the server")
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, reason: str = "No reason provided"):
    # This command requires a guild context.
    if ctx.guild is None:
        await ctx.reply("This command can only be used in a server.")
        return

    # Prevent self-kicking.
    if member == ctx.author:
        await ctx.reply("You cannot kick yourself.")
        return

    # Ensure the invoker has a higher role than the target.
    if not _is_higher_role(ctx.author, member):
        await ctx.reply("You cannot kick a member with an equal or higher role.")
        return

    await member.kick(reason=reason)
    await ctx.reply(f"Kicked {member.mention}. Reason: {reason}")
