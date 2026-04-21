import json
import os

# Directory that contains the logic package and data files.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
WHITELIST_FILE = os.path.join(ROOT_DIR, 'whitelist_data.json')
WHITELIST_CMD_FILE = os.path.join(ROOT_DIR, 'whitelist_cmd.txt')


def load_whitelist():
    # Load the list of whitelisted guild IDs from disk.
    if not os.path.exists(WHITELIST_FILE):
        save_whitelist([])
        return []

    with open(WHITELIST_FILE, 'r') as f:
        return json.load(f)


def save_whitelist(guild_ids):
    # Persist the whitelist of guild IDs back to disk.
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(guild_ids, f)


def is_guild_whitelisted(guild_id):
    # Return True if the given guild is on the whitelist.
    return guild_id in load_whitelist()


def add_guild_to_whitelist(guild_id):
    # Add a guild to the whitelist if it is not already present.
    guilds = load_whitelist()
    if guild_id in guilds:
        return False
    guilds.append(guild_id)
    save_whitelist(guilds)
    return True


def remove_guild_from_whitelist(guild_id):
    # Remove a guild from the whitelist if it exists.
    guilds = load_whitelist()
    if guild_id not in guilds:
        return False
    guilds.remove(guild_id)
    save_whitelist(guilds)
    return True


def get_whitelist_command_users():
    # Load the list of users allowed to manage whitelist commands.
    if not os.path.exists(WHITELIST_CMD_FILE):
        return []
    with open(WHITELIST_CMD_FILE, 'r') as f:
        return [int(line.strip()) for line in f if line.strip().isdigit()]


def is_whitelist_command_user(user_id):
    # Return True if the user is allowed to run whitelist commands.
    return user_id in get_whitelist_command_users()
