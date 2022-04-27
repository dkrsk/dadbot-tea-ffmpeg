import discord
from discord.ext import commands

from Ytools import ytplayer
from Ytools import misc
from Ytools import yembeds

import json
import asyncio


class ytStream(commands.Cog):

    def __init__(self,client):
        self.client = client

        with open('./config.json', 'r', encoding='utf8') as f:
            self.config = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        self.player = ytplayer.MusicPlayer(self.client)
    
    @commands.command(aliases=('p','з'), description='Включает ваше видео с Ютуба. Принимает ссылки на видео/плейлисты или может найти видео по названию. d!play <имя/ссылка>')
    async def play(self,ctx, *, arg, isTopFunc=False):
        if await self.player.stdCheck(ctx): return

        guildID = ctx.guild.id
        guildPlaylist = self.player.playlist[guildID]

        

        voice_client = await misc.Connect(ctx)


        if voice_client == None: return

        await ctx.send(f':mag_right: Ищу `{arg}`')
        song = await self.player.getSong(arg, ctx.message.author, False)

        if not isTopFunc:
            guildPlaylist.queue.extend(song)
        else: guildPlaylist.queue.extendleft(song)
        guildPlaylist.voice_client = voice_client
        guildPlaylist.text_channel = ctx.channel
        
        if voice_client.is_playing():
            await ctx.send(':musical_note: В очередь добавлено: `' + guildPlaylist.queue[-1*(not isTopFunc)]['title'] + '`' + '.')
        else:
            self.player.playSong(guildID)
        


    @commands.command(aliases=('fs','аы'), description='Принудительный скип клипа')
    async def forceskip(self,ctx):
        if await self.player.stdCheck(ctx): return

        self.player.playNextSong(ctx.guild.id)

    
    @commands.command(aliases=('np','тз'), description='Выводит что играет прямо сейчас')
    async def nowplaying(self, ctx):
        if await self.player.stdCheck(ctx): return

        guildPlaylist = self.player.playlist[ctx.guild.id]
        if guildPlaylist.voice_client and guildPlaylist.voice_client.is_playing:
            await ctx.send(embed = yembeds.embeds(guildPlaylist).nowplayingEmbed())
        else: await ctx.send(':stop_button: Сейчас ничего не играет')


    @commands.command(aliases=('q','й'), description = 'Выводит очередь клипов сервера')
    async def queue(self,ctx):
        if await self.player.stdCheck(ctx): return

        playlist = self.player.playlist[ctx.guild.id]
        if len(playlist.queue) == 0:
            await ctx.send(':o: `Очередь пуста`')
            return
        await ctx.send(embed = yembeds.embeds(playlist).queuesEmbed())


    @commands.command(aliases=('sc','ыуфкср','ыс'), description='Добавляет в очередь одно из первых десяти видео по названию. d!search <имя>')
    async def search(self,ctx,*,arg):
        if await self.player.stdCheck(ctx): return

        guildID = ctx.guild.id
        guildPlaylist = self.player.playlist[guildID]
        voice_client = await misc.Connect(ctx)



        await ctx.send(f':mag_right: Ищу `{arg}`')
        searchList = await self.player.getSong(arg, ctx.author, isSearch = True)
        message = await ctx.send(embed = yembeds.embeds(guildPlaylist).searchedEmbed(arg, searchList))

        try:
            answer = await self.client.wait_for('message',
                                                check = lambda c:c.channel == ctx.channel and c.author == ctx.author,
                                                timeout=20)
        except asyncio.TimeoutError:
            await message.edit(content = ':alarm_clock: Время закончилось', embed = None)
            return
        
        if answer.content.lower() == 'cancel':
            await message.edit(content = ':negative_squared_cross_mark:', embed = None)
            return

        if answer.content.isdigit():

            await message.edit(content = ':white_check_mark:', embed = None)

            guildPlaylist.queue.append(searchList[int(answer.content)-1])
            guildPlaylist.voice_client = voice_client
            guildPlaylist.text_channel = ctx.channel
                                                    
            self.player.playSong(guildID)



    @commands.command(aliases=('dc','вс'), description = 'Отключает бота с сервера')
    async def disconnect(self,ctx):
        if await self.player.stdCheck(ctx): return

        #self.player.playlist[ctx.guild.id] = await misc.Disconnect(self.player.playlist[ctx.guild.id])
        await misc.Disconnect(self.player.playlist[ctx.guild.id])

    @commands.command(aliases=('l','д','дщщз'), description = 'Включает/выключает повтор трека')
    async def loop(self,ctx):
        if await self.player.stdCheck(ctx): return

        isLooped = self.player.playlist[ctx.guild.id].trackIsLooped
        self.player.playlist[ctx.guild.id].trackIsLooped = not isLooped

        await ctx.send(f':repeat_one: Track {misc.transformLoopToStr(isLooped)}')

    @commands.command(aliases=('сдуфк',), description = 'Очищает очередь сервера (так же останавливает воспроизведение)')
    async def clear(self, ctx):
        if await self.player.stdCheck(ctx): return

        self.player.playlist[ctx.guild.id].voice_client.stop()
        self.player.playlist[ctx.guild.id].nullify()

        await ctx.send(':ok_hand: Очередь очищена')

    @commands.command(aliases=('pt','здфнещз','зе'), description='Работает как play, но добавляет клип в начало очереди')
    async def playtop(self,ctx, *, arg):
        await self.play(ctx, arg=arg, isTopFunc=True)

    @commands.command(aliases=('r','куьщму'), description='Удаляет клип из позиции в очереди')
    async def remove(self,ctx,arg):
        if await self.player.stdCheck(ctx): return

        try:
            del(self.player.playlist[ctx.guild.id].queue[int(arg)-1])
            await ctx.send(':ok_hand: Клип удален')
        except IndexError:
            await ctx.send(':interrobang: Такого номера в этой очереди не обнаружено!')


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user:
            return

        vc = member.guild.voice_client
        if vc == None: return
        print(vc)

        if after.channel == None and before.channel == vc.channel:
            await asyncio.sleep(20)
            if len(vc.channel.members) == 1:
                await misc.Disconnect(self.player.playlist[member.guild.id])

    """ @commands.command(aliases=('setwhite','ыуе_цршеу_срфттуд','ыуецршеу'))
    @commands.has_permissions(administrator=True)
    async def set_white_channel(self, ctx):
        chID = ctx.channel.id

        self.config['ServerSettings'][str(ctx.guild.id)]['whiteChannel'] = chID
        with open('config.json', 'w', encoding='utf8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
                
        await ctx.send(f'`{ctx.channel}` установлен как основной музыкалный канал') """



def setup(client):
    client.add_cog(ytStream(client))