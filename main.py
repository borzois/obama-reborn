import disnake
from disnake.ext import commands

from utils.utils import Ip, BooruTool
from repository.repo import Repository

from cogs.manual_override import Manual
from cogs.misc import Misc
from cogs.vc import Voice
from cogs.booru import Booru

import logging

logging.basicConfig(filename='logs/obama.log', encoding='utf-8', level=logging.INFO, format='%(levelname)s:%(message)s')

# enable gateway intents
intents = disnake.Intents.default()
intents.message_content = True
intents.presences = True

# initialise client object
client = commands.Bot(command_prefix='.', description="Obama", intents=intents)

# initialise utils
repo = Repository()
ip_manager = Ip()
booru_tool = BooruTool()


@client.event
async def on_ready():
    print('{0.user} has awakened'.format(client))  # keeping command line print for tradition
    logging.info('{0.user} has awakened'.format(client))

# attach cogs
client.add_cog(Manual(client, repo.get_admins()))
client.add_cog(Misc(client, ip_manager))
client.add_cog(Voice(client, repo.get_llkey()))
client.add_cog(Booru(client, booru_tool))


client.run(repo.get_token())
