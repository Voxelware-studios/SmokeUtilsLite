# Entry point for the SmokeUtils bot application.
# Load the bot, configure startup behavior, and start the event loop.
import os
import asyncio
import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *
from bootstrap.get_token import get_token
from bootstrap.is_ready import *
from bootstrap.commands_loader import *

# Load the token from disk and start the bot.
token = get_token()
bot.run(token)