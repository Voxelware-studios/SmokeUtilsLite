import json
import os

# Local JSON file storing welcome channel configuration per guild.
DATA_FILE = 'welcomer_data.json'

def load_data():
    # Load the welcome configuration from disk.
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    # Persist welcome configuration changes.
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_welcome_channel_id(guild_id):
    # Return the configured welcome channel for a guild.
    data = load_data()
    return data.get(str(guild_id), {}).get('channel_id')

def set_welcome_channel_id(guild_id, channel_id):
    # Store the welcome channel ID for a guild.
    data = load_data()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]['channel_id'] = channel_id
    save_data(data)

def remove_welcome_channel(guild_id):
    # Remove the welcome channel configuration for a guild.
    data = load_data()
    if str(guild_id) in data:
        del data[str(guild_id)]
        save_data(data)
