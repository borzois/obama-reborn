import disnake
from disnake.ext import tasks, commands

from utils.utils import Ip, BooruTool
from repository.repo import Repository

from cogs.manual_override import Manual
from cogs.misc import Misc
from cogs.vc import Voice
from cogs.booru import Booru

intents = disnake.Intents.default()
intents.message_content = True
intents.presences = True

client = commands.Bot(command_prefix='.', description="Obama", intents=intents)
ip_manager = Ip()
repo = Repository()
booru_tool = BooruTool()


@client.event
async def on_ready():
    print('{0.user} has awakened'.format(client))


client.add_cog(Manual(client, repo.get_admins()))
client.add_cog(Misc(client, ip_manager))
client.add_cog(Voice(client))
client.add_cog(Booru(client, booru_tool))

client.run(repo.get_token())
