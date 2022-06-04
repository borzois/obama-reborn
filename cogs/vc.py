from disnake.ext import commands
import wavelink

from pathlib import Path
import asyncio


def get_track_length(track):
    seconds = int(track.info['length'] / 1000)
    # get seconds
    sec_mod = int(seconds % 60)
    if sec_mod < 10:
        sec_str = "0" + str(sec_mod)
    else:
        sec_str = str(sec_mod)

    # get minutes
    min_div = int((seconds % 3600) / 60)
    if min_div == 0:
        min_str = "00"
    elif min_div < 10:
        min_str = "0" + str(min_div)
    else:
        min_str = str(min_div)

    # get hours
    if seconds < 3600:
        return min_str + ":" + sec_str
    return str(int(seconds/3600)) + ":" + min_str + ":" + sec_str


def get_type(query: str):
    if "youtube.com/" in query or "youtu.be/" in query:
        return "youtube"
    if "soundcloud.com/" in query:
        return "soundcloud"
    return "search"


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
        self.looping = False
        client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host='0.0.0.0',
                                            port=2333,
                                            password=self.lavalink_key)

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        print("now playing:", track)
        # TODO: get this to send a message

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        print(track, "ended")
        if not self.queue.is_empty:
            await self.queue_play()
        else:
            await player.disconnect()

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, data: [str, any]) -> None:
    #     print("door stuck", data)

    async def vc_init(self, ctx):
        if not ctx.voice_client:
            self.player: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            self.player: wavelink.Player = ctx.voice_client

    async def queue_play(self):
        if not self.queue.is_empty:
            current_audio = self.queue.get()
            # ctx.send(f"Now playing {1}", current_audio)

            await self.player.play(current_audio)

    @commands.command()
    async def queue(self, ctx):
        if self.queue.is_empty:
            await ctx.send("```\nQueue is empty\n```")
        else:
            queue_string = "```\n"
            pos = 1
            for song in self.queue:
                queue_string = queue_string + str(pos) + ". " + song.info['title'] + " - " +  \
                               get_track_length(song) + "\n"
                pos += 1
            queue_string += '```'
            await ctx.send(queue_string)

    @commands.command()
    async def clear(self, ctx):
        self.queue.clear()
        await self.player.disconnect()
        await ctx.send("Queue cleared")

    @commands.command()
    async def play(self, ctx, *, query):
        await self.vc_init(ctx)
        query_type = get_type(query)

        if query_type == "youtube" or query_type == "soundcloud":
            tracks = await self.player.node.get_tracks(query=query, cls=wavelink.Track)
            if len(tracks) != 0:
                track = tracks[0]
            else:
                await ctx.send("Invalid link")
                return
        else:
            track = await wavelink.YouTubeTrack.search(query, return_first=True)

        print(ctx.message.author, "requested", track.uri)
        self.queue.put(track)
        await ctx.send("Added **" + track.title + "** to queue")
        if not self.player.is_playing():
            await self.queue_play()

    @commands.command()
    async def pause(self, ctx):
        await self.player.pause()
        await ctx.send("Paused")

    @commands.command()
    async def resume(self, ctx):
        await self.player.resume()
        await ctx.send("Resumed")

    @commands.command()
    async def skip(self, ctx):
        print(self.player.track.length)
        await self.player.seek(self.player.track.length * 1000)  # seeks to the end of the track
        await ctx.send("Skipped")

    @commands.command()
    async def rkelly(self, ctx):
        search = await wavelink.YouTubeTrack.search("rkelly ignition", return_first=True)
        await self.vc_init(ctx)

        self.queue.put(search)
        await ctx.send("Added **" + search.title + "** to queue")
        if not self.player.is_playing():
            await self.queue_play()

    @commands.command()
    async def loop(self, ctx):
        if not self.looping:
            self.looping = True
            await ctx.send("Now looping")
        else:
            self.looping = False
            await ctx.send("No longer looping")

    @commands.command()
    async def gong(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['gong']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def laugh(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['laugh']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def vineboom(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['vineboom']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def wetfart(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['fart']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def knock(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['knock']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def greier(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['greier']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def cartoon(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['cartoon']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def bruh(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['bruh']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def cinematic(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['cinematic']), return_first=True)
        await self.player.play(search)

    @commands.command()
    async def snap(self, ctx):
        await self.vc_init(ctx)
        search = await wavelink.LocalTrack.search(str(self.sound['snap']), return_first=True)
        await self.player.play(search)
