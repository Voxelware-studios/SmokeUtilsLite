import discord
import random
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# Send a random skull emoji.
@bot.hybrid_command(name="skull", description="Send a random skull emoji")
async def skull(ctx):
    skulls = [
        "💀",
        "☠️",
    ]

    await ctx.reply(random.choice(skulls))