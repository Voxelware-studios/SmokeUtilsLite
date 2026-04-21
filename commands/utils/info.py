import discord
from bootstrap.intents import *
from discord.ext import commands
from bootstrap.bot_boot import *
from bootstrap.is_ready import *

# Show basic bot statistics such as latency and server count.
@bot.hybrid_command(name="info", description="Give information about the bot")
async def info(ctx):
    latency = round(bot.latency * 1000)
    server_count = len(bot.guilds)
    embed = discord.Embed(title="SmokeUtils Bot Information", color=discord.Color.blue())
    embed.add_field(name="Servers:", value=server_count, inline=False)
    embed.add_field(name="Latency:", value=f"{latency}ms", inline=False)
    embed.add_field(name="made with ❤️ by:", value="VOXELWARE Studios", inline=False)
    await ctx.reply(embed=embed)