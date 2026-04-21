import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# Reply with the bot's current websocket latency.
@bot.hybrid_command(name="ping", description="Check the bot latency")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.reply(f"Pong! {latency}ms")