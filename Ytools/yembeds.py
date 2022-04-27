from discord import Embed, Colour, player
from datetime import timedelta
from Ytools.misc import transformLoopToStr


class embeds():
    def __init__(self,playlist):
        self._playlist = playlist
        self._stdURL = 'https://discord.com/'
        

    def nowplayingEmbed(self):
        nowplaying = self._playlist.nowplaying
        reqBy = nowplaying['requestedBy']
        loopBool = self._playlist.trackIsLooped


        if self._playlist.trackIsLooped:
            loopStr = f'Track is {transformLoopToStr(not loopBool)}'
        else: loopStr = ''

        try: nextSong = self._playlist.queue[0]['title']
        except IndexError: nextSong = 'Ничего'

        return Embed(
            title = 'Сейчас играет :musical_note:',
            url=nowplaying['webpage_url'],
            description = f"[{str(nowplaying['title'])}]({str(nowplaying['webpage_url'])})\n\n`Запрошено:` {str(reqBy.name)}#{str(reqBy.discriminator)} \n\n`Длительность:` {nowplaying['duration']} \n\n`Что дальше:` {nextSong}",
            colour = Colour.from_rgb(222, 184, 135)   
        ).set_thumbnail(url=nowplaying['thumbnail']).set_footer(text=loopStr)


    def queuesEmbed(self):
        return Embed(
            title = 'Очередь ' + str(self._playlist.text_channel.guild.name),
            url = self._stdURL,
            description = self._cunstructQueue() + '\n\n' + str(len(self._playlist.queue)) + ' позиций в очереди',
            colour = Colour.from_rgb(221, 160, 221)
        )


    def searchedEmbed(self, arg, result):
        return Embed(
            title = f'Поиск по {arg}',
            url = self._stdURL,
            description = f'{self._cunstructSearched(result)}\nЕсли вы передумали, напишите `cancel`',
            colour = Colour.from_rgb(135, 206, 235)
        )
    


    def _cunstructQueue(self):
        queue = self._playlist.queue
        qPos = 0
        qDesc=''
        for i in queue:
            qPos+=1
            qDesc += '\n`' + str(qPos) + '`. [' + str(i['title']+'](' + str(i['webpage_url'])+')' + ' `Длительность:` ' + str(i['duration']))
        return qDesc

    def _cunstructSearched(self, result):
        if result == None:
            self.searchedEmbed = None
            return

        desc = ''
        for i in result:
            desc += f'`{result.index(i)+1}.` [{i["title"]}]({i["webpage_url"]}) Длительность: {i["duration"]}\n'
        return desc
            