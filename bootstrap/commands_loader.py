# Import all command modules so they are registered with the bot.
# This file is loaded once during startup by main.py.

# utils commands
from commands.utils.ping import *
from commands.utils.info import *
from commands.utils.servericon import *
from bootstrap.whitelist_check import *

# community commands
from commands.community.dont_ask import *
from commands.community.welcomer import *
from commands.community.whitelist import *

# fun commands
from commands.fun.skull import *
from commands.fun.coin import *
from commands.fun.calc import *
from commands.fun.counting import *
from commands.fun.giveaway import *

# moderation commands
from commands.moderation.kick import *
from commands.moderation.ban import *
from commands.moderation.unban import *
from commands.moderation.mute import *
from commands.moderation.unmute import *