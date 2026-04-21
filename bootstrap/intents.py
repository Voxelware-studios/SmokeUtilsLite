import discord
from discord.ext import commands

# Configure the gateway intents required by the bot.
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True