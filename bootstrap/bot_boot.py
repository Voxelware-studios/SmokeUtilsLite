import discord
from bootstrap.intents import *
from discord.ext import commands

# Custom bot subclass for SmokeUtils.
class SmokeUtils(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="su!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Called during bot startup to sync application commands.
        await self.tree.sync()
        print("commands synced")

bot = SmokeUtils()

