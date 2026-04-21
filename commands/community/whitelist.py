import discord
from discord.ext import commands
from bootstrap.bot_boot import *
from logic.whitelist import add_guild_to_whitelist, remove_guild_from_whitelist, get_whitelist_command_users

# User ID that is always allowed to manage the whitelist.
SPECIAL_USER_ID = 991454367876132944


@bot.hybrid_group(name="whitelist", description="Manage the server whitelist")
async def whitelist_group(ctx: commands.Context):
    # If no subcommand is invoked, show usage instructions.
    if ctx.invoked_subcommand is None:
        await ctx.reply("Use `/whitelist add [guild_id]` or `/whitelist remove [guild_id]`.")


@whitelist_group.command(name="add", description="Add a server to the whitelist")
async def whitelist_add(ctx: commands.Context, guild_id: str = None):
    # Restrict whitelist management to authorized users.
    if ctx.author.id != SPECIAL_USER_ID and ctx.author.id not in get_whitelist_command_users():
        await ctx.reply("You are not allowed to use whitelist management commands.")
        return

    target_id = None
    if guild_id is not None:
        try:
            target_id = int(guild_id)
        except ValueError:
            await ctx.reply("Please provide a valid guild ID number.")
            return
    elif ctx.guild is not None:
        target_id = ctx.guild.id

    # Ensure a valid target guild is determined.
    if target_id is None:
        await ctx.reply("Please provide a guild ID.")
        return

    added = add_guild_to_whitelist(target_id)
    if added:
        await ctx.reply(f"Guild {target_id} added to the whitelist.")
    else:
        await ctx.reply(f"Guild {target_id} is already whitelisted.")


@whitelist_group.command(name="remove", description="Remove a server from the whitelist")
async def whitelist_remove(ctx: commands.Context, guild_id: str = None):
    # Restrict whitelist removal to authorized users.
    if ctx.author.id != SPECIAL_USER_ID and ctx.author.id not in get_whitelist_command_users():
        await ctx.reply("You are not allowed to use whitelist management commands.")
        return

    target_id = None
    if guild_id is not None:
        try:
            target_id = int(guild_id)
        except ValueError:
            await ctx.reply("Please provide a valid guild ID number.")
            return
    elif ctx.guild is not None:
        target_id = ctx.guild.id

    if target_id is None:
        await ctx.reply("Please provide a guild ID.")
        return

    removed = remove_guild_from_whitelist(target_id)
    if removed:
        await ctx.reply(f"Guild {target_id} removed from the whitelist.")
    else:
        await ctx.reply(f"Guild {target_id} was not whitelisted.")
