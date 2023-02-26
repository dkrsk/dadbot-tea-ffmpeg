import asyncio
from discord import FFmpegPCMAudio
from discord.ext import commands
from yt_dlp import YoutubeDL
from requests import get
from datetime import timedelta
from collections import deque

from Ytools import yembeds, misc

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class MusicPlayer():
    
    def __init__(self,client):
        self.client = client
        self.playlist = dict()

        for guild in client.guilds:
            self.playlist.update({
                guild.id: self.MusicPlaylist()
            })


    async def getSong(self, arg, user, isSearch:bool = False):
        def editInfo(info):
            editedInfo = info.copy()

            

            if editedInfo['duration'] == 0.0:
                editedInfo['duration'] = 'Live'
                editedInfo['title'] = info['title'][:-16]
            else:
                editedInfo['duration'] = str(timedelta(seconds = editedInfo['duration']))

            return {
                'title':editedInfo['title'],
                'url':editedInfo['url'],
                'duration':editedInfo['duration'],
                'webpage_url':editedInfo['webpage_url'],
                'thumbnail':editedInfo['thumbnail'],
                'requestedBy':user
            }


        isSearch=int(isSearch)*9 + 1

        with YoutubeDL({'format': 'bestaudio/95/91','noplaylist':'True','playlistend': 20}) as ydl:
            try: get(arg)
            except: info = ydl.extract_info(f"ytsearch{isSearch}:{arg}", download=False)['entries']
            else: 

                info = ydl.extract_info(arg, download=False)

                if info.get('_type') == 'playlist':
                    info = info['entries']
                else: info = [info]
                


        
        songs = []
        for i in info:
            if type(i) == type(dict()):
                songs.append(editInfo(i))
        return songs

    def playSong(self, guildID):
        playlist = self.playlist[guildID]

        if not playlist.voice_client or playlist.voice_client.is_playing():
            #asyncio.run_coroutine_threadsafe(playlist.text_channel.send(':musical_note: В очередь добавлено: `' + playlist.queue[-1]['title'] + '`' + '.'),self.client.loop)
            return

        try:
            if not playlist.trackIsLooped:
                playlist.nowplaying = playlist.queue.popleft()
            source = playlist.nowplaying.get('url')
        except IndexError: return
        
        asyncio.run_coroutine_threadsafe(playlist.text_channel.send(embed = yembeds.embeds(playlist).nowplayingEmbed()),self.client.loop)
        playlist.voice_client.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=(lambda x: self.playSong(guildID)))

    def playNextSong(self, guildID):
        playlist = self.playlist[guildID]
        playlist.voice_client.stop()
        self.playSong(guildID)
        

    async def stdCheck(self, ctx):
        guildPlaylist = self.playlist[ctx.guild.id]

        if guildPlaylist.text_channel not in (None,ctx.channel):
            await ctx.send(f'Сейчас я работаю в {guildPlaylist.text_channel.mention}')
            return True

        if ctx.author.voice == None:
            await ctx.send(':interrobang: Сначала подключитесь к каналу!')
            return True

        return False

        

    class MusicPlaylist():

        #__getattr__ = dict.get
        #_setattr__ = dict.__setitem__
        #__delattr__ = dict.__delitem__

        def __init__(self):
            self.voice_client = None
            self.text_channel = None
            self.queue = deque()
            self.nowplaying = None
            self.trackIsLooped = False

        def nullify(self):
            self.voice_client = None
            self.text_channel = None
            self.queue = deque()
            self.nowplaying = None
            self.trackIsLooped = False

        
                