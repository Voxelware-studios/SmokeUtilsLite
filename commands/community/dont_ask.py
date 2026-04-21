import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# Simple command that replies with a short, fixed message.
@bot.hybrid_command(name="dont_ask", description="Don't ask to ask. Just ask!")
async def dont_ask(ctx):
    await ctx.send("Don't ask to ask. Just ask!")