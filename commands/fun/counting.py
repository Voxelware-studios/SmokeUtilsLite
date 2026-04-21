import discord
from discord import app_commands
from discord.ext import commands
from bootstrap.bot_boot import *
from logic.counting import get_counting_channel_id, set_counting_channel_id, remove_counting_channel, get_last_count, set_last_count, get_last_user_id, set_last_user_id

@bot.hybrid_group(name="counting", description="Manage counting feature")
@commands.has_permissions(manage_guild=True)
async def counting_group(ctx: commands.Context):
    # Root command group for counting setup commands.
    pass

@counting_group.command(name="setup", description="Set the counting channel")
@commands.has_permissions(manage_guild=True)
async def setup(ctx: commands.Context, channel: discord.TextChannel):
    # Set the counting channel for this guild and initialize state.
    set_counting_channel_id(ctx.guild.id, channel.id)
    await ctx.reply(f"Counting channel set to {channel.mention}. Start counting from 1!")

@counting_group.command(name="disable", description="Disable counting feature")
@commands.has_permissions(manage_guild=True)
async def disable(ctx: commands.Context):
    # Disable the counting feature by removing stored guild state.
    remove_counting_channel(ctx.guild.id)
    await ctx.reply("Counting feature disabled.")

@bot.event
async def on_message(message):
    # Ignore messages sent by bots.
    if message.author.bot:
        return
    
    guild_id = message.guild.id
    ch_id = get_counting_channel_id(guild_id)
    # Only process counting messages in the configured channel.
    if ch_id and message.channel.id == ch_id:
        last_user = get_last_user_id(guild_id)
        # Do not allow the same user to count twice in a row.
        if last_user and message.author.id == last_user:
            await message.delete()
            return
        
        last = get_last_count(guild_id)
        try:
            num = int(message.content.strip())
            # Accept only the next integer in the sequence.
            if num == last + 1:
                set_last_count(guild_id, num)
                set_last_user_id(guild_id, message.author.id)
                await message.add_reaction("✅")
            else:
                await message.delete()
        except ValueError:
            # Remove any non-integer messages from the counting channel.
            await message.delete()
    
    # Continue processing commands after counting handling.
    await bot.process_commands(message)