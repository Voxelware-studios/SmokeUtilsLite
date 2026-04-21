import discord
from discord.ext import commands
from bootstrap.bot_boot import *

# Command to remove the timeout from a muted user.
@bot.hybrid_command(name="unmute", description="Unmute a member")
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def unmute(ctx: commands.Context, member: discord.Member, reason: str = "No reason provided"):
    # Ensure the command is run inside a guild context.
    if ctx.guild is None:
        await ctx.reply("This command can only be used in a server.")
        return

    # Clear the member timeout and confirm the action.
    await member.edit(timed_out_until=None, reason=reason)
    await ctx.reply(f"Unmuted {member.mention}. Reason: {reason}")
