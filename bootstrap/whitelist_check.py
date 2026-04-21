import discord
from discord.ext import commands
from bootstrap.bot_boot import *
from logic.whitelist import is_guild_whitelisted, is_whitelist_command_user

# Always allow this special user regardless of guild whitelist.
SPECIAL_USER_ID = 991454367876132944
# Commands that should bypass the global whitelist check.
EXEMPT_COMMANDS = {"ping", "info", "cat", "servericon", "dont_ask", "skull", "nitro"}


def get_root_command_name(command: commands.Command):
    # Walk up the command parent chain to get the base command name.
    root_command = command
    while root_command.parent is not None:
        root_command = root_command.parent
    return root_command.name


def has_permissions(**perms):
    # Custom version of commands.has_permissions that respects whitelist command users.
    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError(f'Invalid permission(s): {", ".join(invalid)}')

    def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id == SPECIAL_USER_ID or is_whitelist_command_user(ctx.author.id):
            return True

        permissions = ctx.permissions
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if not missing:
            return True

        raise commands.MissingPermissions(missing)

    return commands.check(predicate)


def has_role(item):
    # Custom role check that bypasses whitelist command users.
    def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id == SPECIAL_USER_ID or is_whitelist_command_user(ctx.author.id):
            return True

        if ctx.guild is None:
            raise commands.NoPrivateMessage()

        if isinstance(item, int):
            role = ctx.author.get_role(item)  # type: ignore
        else:
            role = discord.utils.get(ctx.author.roles, name=item)  # type: ignore
        if role is None:
            raise commands.MissingRole(item)
        return True

    return commands.check(predicate)


def has_any_role(*items):
    # Custom check for membership in any of the provided roles.
    def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id == SPECIAL_USER_ID or is_whitelist_command_user(ctx.author.id):
            return True

        if ctx.guild is None:
            raise commands.NoPrivateMessage()

        if any(
            ctx.author.get_role(item) is not None
            if isinstance(item, int)
            else discord.utils.get(ctx.author.roles, name=item) is not None
            for item in items
        ):
            return True
        raise commands.MissingAnyRole(list(items))

    return commands.check(predicate)


def has_guild_permissions(**perms):
    # Guild permission check for commands and whitelist bypass.
    invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
    if invalid:
        raise TypeError(f'Invalid permission(s): {", ".join(invalid)}')

    def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id == SPECIAL_USER_ID or is_whitelist_command_user(ctx.author.id):
            return True

        if not ctx.guild:
            raise commands.NoPrivateMessage()

        permissions = ctx.author.guild_permissions
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if not missing:
            return True

        raise commands.MissingPermissions(missing)

    return commands.check(predicate)


# Override discord.py helper functions with our custom checks.
commands.has_permissions = has_permissions
commands.has_role = has_role
commands.has_any_role = has_any_role
commands.has_guild_permissions = has_guild_permissions


def command_requires_permission_check(command: commands.Command):
    # Determine whether a command has a custom permission check attached.
    while command is not None:
        if any(
            check.__module__ == __name__ and check.__name__ == 'predicate'
            for check in getattr(command, 'checks', [])
        ):
            return True
        command = command.parent
    return False


@bot.check
async def whitelist_check(ctx: commands.Context):
    # Global bot check that enforces the guild whitelist.
    if ctx.command is None:
        return True

    root_name = get_root_command_name(ctx.command)
    if root_name in EXEMPT_COMMANDS:
        return True

    if ctx.author.id == SPECIAL_USER_ID:
        return True

    if root_name == "whitelist":
        return is_whitelist_command_user(ctx.author.id)

    if ctx.guild is None:
        return False

    if command_requires_permission_check(ctx.command):
        if not is_whitelist_command_user(ctx.author.id):
            return False

    return is_guild_whitelisted(ctx.guild.id)
