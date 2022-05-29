import disnake
from disnake.ext import commands
import wavelink

from pathlib import Path
import asyncio

class Voice(commands.Cog):
    def __init__(self, client, lavalink_key):
        self.client = client
        self.lavalink_key = lavalink_key
        self.mod_path = Path(__file__).parent
        sound_folder = '../sounds/'
        self.sound_folder_path = (self.mod_path / sound_folder).resolve()

        self.sound = {
            'gong': (self.sound_folder_path / "gong.mp3").resolve(),
            'laugh': (self.sound_folder_path / "laugh2.mp3").resolve(),
            'vineboom': (self.sound_folder_path / "vine.mp3").resolve(),
            'fart': (self.sound_folder_path / "fart.mp3").resolve(),
            'knock': (self.sound_folder_path / "knock.mp3").resolve(),
            'greier': (self.sound_folder_path / "greier.mp3").resolve(),
            'cartoon': (self.sound_folder_path / "cartoon.mp3").resolve(),
            'bruh': (self.sound_folder_path / "bruh.mp3").resolve(),
            'cinematic': (self.sound_folder_path / "cinematic.mp3").resolve(),
            'snap': (self.sound_folder_path / "snap.mp3").resolve()
        }

        self.player = None
        self.queue = wavelink.Queue()
        self.play_next_song = asyncio.Event()
        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host='0.0.0.0',
                                            port=2333,
                                            password=self.lavalink_key)

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        print("now playing:", track)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        print(track, "ended")
        if not self.queue.is_empty:
            await self.queue_play()
        else:
            await player.disconnect()

    @commands.Cog.listener()
    async def on_voice_server_update(data: Dict[str, Any]) → None

    async def queue_play(self):
        if not self.queue.is_empty:
            current_audio = self.queue.get()
            # ctx.send(f"Now playing {1}", current_audio)

            await self.player.play(current_audio)

    async def vc_init(self, ctx):
        if not ctx.voice_client:
            self.player: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            self.player: wavelink.Player = ctx.voice_client

    @commands.command()
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        print(ctx.message.author, "requested", search.uri)
        await self.vc_init(ctx)

        self.queue.put(search)
        await ctx.send("Added *" + search.title + "* to queue")
        if not self.player.is_playing():
            await self.queue_play()

    @commands.command()
    async def gong(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['gong'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def laugh(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['laugh'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def vineboom(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['vineboom'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def wetfart(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['fart'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def knock(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['knock'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def greier(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['greier'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def cartoon(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['cartoon'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def bruh(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['bruh'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def cinematic(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['cinematic'])
        if not self.player.is_playing():
            self.queue_play()

    @commands.command()
    async def snap(self, ctx):
        await self.vc_init(ctx)
        self.queue.append(self.sound['snap'])
        if not self.player.is_playing():
            self.queue_play()
