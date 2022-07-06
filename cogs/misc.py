from disnake.ext import commands


class Misc(commands.Cog):
    def __init__(self, client, ip_manager):
        self.client = client
        self.ip_manager = ip_manager

    @commands.command()
    async def h(self, ctx):
        await ctx.send(self.ip_manager.get_ip())

    @commands.command()
    async def funnydog(self, ctx):
        await ctx.send("https://tenor.com/view/borzoi-snoopa-lord-foog-dog-funny-gif-20125052")

    @commands.command()
    async def question(self, channelid, baka):
        for i in range(5):
            channel = self.client.get_channel(int(channelid))
            await channel.send('are you gay? {}'.format(baka))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.client.user:
            return
        if ctx.content.lower().startswith('gm'):
            print(str(ctx.author))
            if str(ctx.author) == "serval#2377":
                await ctx.channel.send("hiiii serval :3")
            else:
                await ctx.channel.send("Gm, " + str(ctx.author.name))
