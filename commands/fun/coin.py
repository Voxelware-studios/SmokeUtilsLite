import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *
import random

# Flip a digital coin and reply with the result.
@bot.hybrid_command(name="coin", description="Flip a coin and see if it lands on heads or tails")
async def coin(ctx):
    outcomes = ["Heads", "Tails"]
    result = random.choice(outcomes)
    
    embed = discord.Embed(
        title="🪙 Flip a coin",
        description=f"**{result}**",
        color=discord.Color.gold()
    )
    await ctx.reply(embed=embed)