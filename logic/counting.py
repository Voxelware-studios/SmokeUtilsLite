import json
import os

DATA_FILE = 'counting_data.json'

def load_data():
    # Load the JSON file storing counting state.
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    # Save the current counting state to disk.
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_counting_channel_id(guild_id):
    # Return the configured counting channel for a guild.
    data = load_data()
    return data.get(str(guild_id), {}).get('channel_id')

def set_counting_channel_id(guild_id, channel_id):
    # Set the counting channel for a guild and reset counter state.
    data = load_data()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]['channel_id'] = channel_id
    data[str(guild_id)]['last_count'] = 0
    data[str(guild_id)]['last_user_id'] = None
    save_data(data)

def remove_counting_channel(guild_id):
    # Remove counting configuration for a guild.
    data = load_data()
    if str(guild_id) in data:
        del data[str(guild_id)]
        save_data(data)

def get_last_count(guild_id):
    # Return the last valid count for a guild, or 0 if none.
    data = load_data()
    return data.get(str(guild_id), {}).get('last_count', 0)

def set_last_count(guild_id, count):
    # Store the last valid count for a guild.
    data = load_data()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]['last_count'] = count
    save_data(data)

def get_last_user_id(guild_id):
    # Return the ID of the last user who posted a valid count.
    data = load_data()
    return data.get(str(guild_id), {}).get('last_user_id')

def set_last_user_id(guild_id, user_id):
    # Store the last user who posted a valid count.
    data = load_data()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]['last_user_id'] = user_id
    save_data(data)