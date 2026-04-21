# Load the bot token from a local file.

def get_token():
    global token
    try:
        with open('token.txt', 'r') as file:
            token = file.read().strip()
        return token
    except FileNotFoundError:
        print("Error: 'token.txt' file not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None