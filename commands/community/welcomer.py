import datetime
import discord
from discord.ext import commands
from bootstrap.bot_boot import *
from logic.welcomer import get_welcome_channel_id, set_welcome_channel_id, remove_welcome_channel

# Welcome command group for configuring welcome messages.
@bot.hybrid_group(name="welcomer", description="Manage the welcome system")
@commands.has_permissions(manage_guild=True)
async def welcomer_group(ctx: commands.Context):
    pass

@welcomer_group.command(name="setup", description="Set the welcome channel")
@commands.has_permissions(manage_guild=True)
async def setup(ctx: commands.Context, channel: discord.TextChannel):
    # Configure the welcome channel for this guild.
    set_welcome_channel_id(ctx.guild.id, channel.id)
    await ctx.reply(f"Welcome channel set to {channel.mention}.")

@welcomer_group.command(name="disable", description="Disable the welcome system")
@commands.has_permissions(manage_guild=True)
async def disable(ctx: commands.Context):
    # Turn off welcome messages for this guild.
    remove_welcome_channel(ctx.guild.id)
    await ctx.reply("Welcome system disabled.")

@bot.event
async def on_member_join(member: discord.Member):
    # Handle new members joining the guild.
    channel_id = get_welcome_channel_id(member.guild.id)
    if not channel_id:
        return

    channel = member.guild.get_channel(channel_id)
    if not channel:
        return

    embed = discord.Embed(
        title="👋 Welcome!",
        description=f"Welcome to **{member.guild.name}**, {member.mention}!",
        color=discord.Color.green(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Member Count", value=f"You are member **#{member.guild.member_count}**", inline=False)
    embed.add_field(name="ID", value=str(member.id), inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="Today at", icon_url=member.guild.icon.url if member.guild.icon else None)

    await channel.send(embed=embed)
