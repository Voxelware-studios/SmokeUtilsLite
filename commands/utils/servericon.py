import discord
import random
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# Send a random skull emoji.
@bot.hybrid_command(name="servericon", description="Get the server's icon")
async def servericon(ctx):
    await ctx.reply(ctx.guild.icon)