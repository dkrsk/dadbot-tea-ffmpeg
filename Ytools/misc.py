import discord

#from Ytools import ytplayer


async def Connect(ctx):
    channel = ctx.author.voice.channel
    vc = ctx.guild.voice_client
    
    try:
        if vc and vc.is_connected():
            if vc.channel != channel:
                await vc.move_to(channel)
        else:
            vc = await channel.connect()
            await ctx.send(f':thumbsup: Подключен к {channel.mention} и связан с {ctx.channel.mention}')
    except AttributeError: raise AttributeError('UserIsNotConnected')
    return vc

async def Disconnect(playlist):
    voice_client = playlist.voice_client
    if not voice_client: return

    if voice_client.is_connected():
        playlist.nullify()
        voice_client.stop()
        await voice_client.disconnect()
        
        return playlist

""" async def isWhiteCh(ctx, config):
    whiteChannel = config['ServerSettings'].get('whiteChannel',None)
    if whiteChannel not in (None,ctx.channel.id):
        await ctx.send(f':exclamation: Для музыкальных команд используется канал #{ctx.guild.get_channel(whiteChannel)}')
        return False
    return True """

def transformLoopToStr(isLoop: bool):
    return {False: 'looped', True: 'unlooped'}[isLoop]
