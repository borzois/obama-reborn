import disnake
from disnake.ext import commands
import io
import aiohttp


async def dl_img(image):
    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            if resp.status != 200:
                raise aiohttp.ServerConnectionError  # ?
            else:
                return io.BytesIO(await resp.read())


class Booru(commands.Cog):
    def __init__(self, client, booru_tool):
        self.client = client
        self.booru = booru_tool

    @commands.command()
    async def gayporn(self, ctx):
        print(ctx.author.name + " has requested yaoi")
        image_query = self.booru.get_random("yaoi")
        try:
            data = await dl_img(image_query)
            await ctx.send(file=disnake.File(data, 'obama.png'))
        except aiohttp.ServerConnectionError:
            ctx.send("Could not download")

    @commands.command()
    async def yuri(self, ctx):
        print(ctx.author.name + " has requested yuri")
        image_query = self.booru.get_random("yuri")
        try:
            data = await dl_img(image_query)
            await ctx.send(file=disnake.File(data, 'obama.png'))
        except aiohttp.ServerConnectionError:
            ctx.send("Could not download")

    @commands.command()
    async def booru(self, ctx, *args):
        tags = ' '.join(args)
        print(ctx.author.name + " has requested " + tags)

        try:
            image_query = self.booru.get_random(tags)
            try:
                data = await dl_img(image_query)
                await ctx.send(file=disnake.File(data, 'obama.png'))
            except aiohttp.ServerConnectionError:
                await ctx.send("Could not download")
        except ValueError:
            await ctx.send("Could not find any images")

    @commands.command()
    async def safe(self, ctx, *args):
        tags = ' '.join(args)
        print(ctx.author.name + " has requested " + tags)

        try:
            image_query = self.booru.get_random_safe(tags)
            try:
                data = await dl_img(image_query)
                await ctx.send(file=disnake.File(data, 'obama.png'))
            except aiohttp.ServerConnectionError:
                await ctx.send("Could not download")
        except ValueError:
            await ctx.send("Could not find any images")
