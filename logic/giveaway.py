import json
import os

# Local JSON data file storing active giveaway state per guild.
DATA_FILE = 'giveaway_data.json'


def load_data():
    # Load giveaway state from disk, or return an empty structure if the file is missing.
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_data(data):
    # Save giveaway state back to disk.
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def get_giveaway(guild_id):
    # Return the active giveaway data for a guild.
    data = load_data()
    return data.get(str(guild_id))


def set_giveaway(guild_id, giveaway_data):
    # Save or update the active giveaway for a guild.
    data = load_data()
    data[str(guild_id)] = giveaway_data
    save_data(data)


def remove_giveaway(guild_id):
    # Delete the giveaway entry for a guild if it exists.
    data = load_data()
    if str(guild_id) in data:
        del data[str(guild_id)]
        save_data(data)


def get_all_giveaways():
    # Return all stored giveaways.
    return load_data()
