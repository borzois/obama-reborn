from disnake.ext import commands

import json
from pathlib import Path
import logging


class Manual(commands.Cog):
    def __init__(self, client, admins):
        self.client = client
        self.admins = admins
        self.channels = {}

        self.mod_path = Path(__file__).parent
        ip_filename = '../repository/channels.json'
        ip_file_path = (self.mod_path / ip_filename).resolve()
        with open(ip_file_path, 'r') as ip_file:
            self.channels.update(json.load(ip_file))

    def update_channels(self):
        ip_filename = '../repository/channels.json'
        ip_file_path = (self.mod_path / ip_filename).resolve()
        with open(ip_file_path, 'w') as ip_file:
            json.dump(self.channels, ip_file)

    @commands.command()
    async def send(self, ctx, channel_name: str, message: str):
        try:
            user = ctx.author.id
            user_name = ctx.author.name
            if user in self.admins:
                channel_obj = self.client.get_channel(int(self.channels[channel_name]))
                await channel_obj.send(message)
                await ctx.send("message sent")
                logging.info(user_name + " sent '" + message + "' to " + channel_name)
            else:
                raise Exception("invalid user")
        except Exception:
            await ctx.send("bruhhhh")

    @commands.command()
    async def send_dm(self, ctx, channel_name: str, message: str):
        try:
            user = ctx.author.id
            user_name = ctx.author.name
            if user in self.admins:
                user_obj = await self.client.fetch_user(int(self.channels[channel_name]))
                await user_obj.send(message)
                await ctx.send("message sent")
                logging.info(user_name + " sent '" + message + "' to " + channel_name)
            else:
                raise Exception
        except Exception as e:
            await ctx.send("bruhhhh")

    @commands.command()
    async def define_channel(self, ctx, channel_name: str, channel_id: str):
        try:
            user = ctx.author.id
            user_name = ctx.author.name
            if user in self.admins:
                self.channels[channel_name] = channel_id
                self.update_channels()
                await ctx.send("defined " + channel_name + " as " + channel_id)
                logging.info(user_name + " defined " + channel_name + " as " + channel_id)
            else:
                raise Exception
        except Exception:
            await ctx.send("invalid channel id. (shift+copy to get it)")
