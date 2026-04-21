import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

# Bot version display used in presence text.
version = "v0.1.0"

@bot.event
async def on_ready():
    # Called once when the bot successfully connects to Discord.
    global server_count
    server_count = len(bot.guilds)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f'SmokeUtils Lite {version}'))
    print("running")