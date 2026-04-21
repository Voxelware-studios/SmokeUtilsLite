import discord
import random
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *

@bot.hybrid_command(name="calc", description="Perform a simple math calculation")
async def calc(ctx, num1: float, operator: str, num2: float):
    # Check what calculation to perform based on the operator provided and compute the result.
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = num1 / num2
    else:
        await ctx.reply("Invalid operator. Please use +, -, *, or /.")
        return
    # Reply with the calculation and the result.
    await ctx.reply(f"{num1} {operator} {num2} = {result}")