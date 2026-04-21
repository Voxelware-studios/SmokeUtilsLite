import discord
from discord.ext import commands
from bootstrap.bot_boot import *

# Command to remove a ban from a user object.
@bot.hybrid_command(name="unban", description="Unban a user from the server")
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def unban(ctx: commands.Context, user: discord.Object, reason: str = "No reason provided"):
    # Require guild context for unbanning.
    if ctx.guild is None:
        await ctx.reply("This command can only be used in a server.")
        return

    await ctx.guild.unban(user, reason=reason)
    await ctx.reply(f"Unbanned <@{user.id}>. Reason: {reason}")
