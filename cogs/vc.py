import disnake
from disnake.ext import commands

from pathlib import Path
import youtube_dl
import asyncio

ytdl_format_options = {
    'format': 'm4a',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(disnake.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(disnake.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mod_path = Path(__file__).parent
        sound_folder = '../sounds/'
        self.sound_folder_path = (self.mod_path / sound_folder).resolve()

        self.gongul = (self.sound_folder_path / "gong.mp3").resolve()
        self.laugh = (self.sound_folder_path / "laugh2.mp3").resolve()
        self.vineboom = (self.sound_folder_path / "vine.mp3").resolve()
        self.fart = (self.sound_folder_path / "fart.mp3").resolve()
        self.knock = (self.sound_folder_path / "knock.mp3").resolve()
        self.greier = (self.sound_folder_path / "greier.mp3").resolve()
        self.cartoon = (self.sound_folder_path / "cartoon.mp3").resolve()
        self.bruh = (self.sound_folder_path / "bruh.mp3").resolve()
        self.cinematic = (self.sound_folder_path / "cinematic.mp3").resolve()
        self.snap = (self.sound_folder_path / "snap.mp3").resolve()

        self.chan = None
        self.queue = []

    def queue_play(self, e=None):
        if len(self.queue) != 0:
            current_audio = self.queue.pop(0)
            print("now playing:", current_audio)
            self.chan.play(disnake.FFmpegOpusAudio(current_audio), after=self.queue_play)
        else:
            pass

    @commands.command()
    async def play(self, ctx, url):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice is None:
            self.chan = await vc.connect()

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            self.chan.play(player)

    @commands.command()
    async def gong(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.gongul)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def laugh(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.laugh)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def vineboom(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.vineboom)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def wetfart(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.wetfart)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def knock(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.knock)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def greier(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.greier)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def cartoon(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.cartoon)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def bruh(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.bruh)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def cinematic(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.cinematic)
        if not self.chan.is_playing(): self.queue_play()

    @commands.command()
    async def snap(self, ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = disnake.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice == None:
            self.chan = await vc.connect()

        self.queue.append(self.snap)
        if not self.chan.is_playing(): self.queue_play()
