import discord
from discord.ext import commands

import json
from random import choice
import asyncio


class agress(commands.Cog):

    def __init__(self,client):
        self.client = client

        with open('config.json', 'r', encoding='utf8') as f:
            self.config = json.load(f)
        self.settings = self.config['config']
        
        with open('pasts.txt', encoding='utf-8') as f:
            self.pasts = f.readlines()

    


    @commands.Cog.listener()
    async def on_message(self, message):
        #await self.client.process_commands(message)

        if self.config['ServerSettings'][str(message.guild.id)]['aggressive'] == 'off':
            print(self.config['ServerSettings'][str(message.guild.id)]['aggressive'] == 'off')
            return

        if message.author == self.client.user:
            return

        cont = message.content.lower()
        if cont.startswith('d!'):
            return
        
        if 'заткнись' in cont.split(' ') or 'заткнулся' in cont.split(' '):
            await message.channel.send('Слышишь, ' + message.author.name + ', что-то мне не нравится как ты со мной разговариваешь. Складывается впечатление что ты реально контуженный, обиженный жизнью имбицил )) Могу тебе и в глаза сказать, готов приехать послушать? ) Вся та хуйня тобою написанное это простое пиздабольство, рембо ты комнатный) )от того что ты много написал, жизнь твоя лучше не станет) ) пиздеть не мешки ворочить, много вас таких по весне оттаяло )) Про таких как ты говорят: Мама не хотела, папа не старался) Вникай в моё послание тебе< постарайся проанализировать и сделать выводы для себя)')
        
        else:
            for i in self.settings['censor']:
                if i in cont.split(' '):
                    await message.channel.send(message.author.name + ', а мама знает что ты такие слова говоришь?')
                    return
        
        if cont.startswith('я '):
            args = cont[2:]
            await message.channel.send('Привет, '+ args +', я папа')
        
        if cont in ('a', 'а'):
            await message.channel.send('б')

        if cont in ('да', 'da'):
            await message.channel.send('пизда)')

        if cont in ('нет', 'net'):
            await message.channel.send('пидора ответ))')

        
    @commands.command(aliases=['паста'],description='Бот расскажет вам одну из его любимых паст')
    async def рассказ(self, ctx):
        await self._pastSend(ctx)

    async def _pastSend(self, ctx):
        p = choice(self.pasts)
        p = tuple(p[x:x+2000] for x in range (0, len(p), 2000))
        for i in range(len(p)):
            await ctx.send(p[i].replace('$n','\n'))


    @commands.command(hidden=True)
    @commands.is_owner()
    async def добавь(self, ctx):

        def check(c):
            return c.author == ctx.author and c.channel == ctx.channel

        if(ctx.channel.id == 820240588556337167):
            
            await ctx.send('пиши давай')
            try:
                paste = await self.client.wait_for('message', check = check, timeout=20)
                paste = paste.content
                paste = paste.replace("\n", "$n")
            except asyncio.TimeoutError:
                await ctx.send('я устал ждать')
                return
            with open('pasts.txt', 'a', encoding=('utf-8')) as p:
                p.write('\n' + paste)
                self.pasts.append(paste)
                print('паста добавлена')
                await ctx.send('паста добавлена')
        else:
            await ctx.send('пососеш, ок?')

        
    @commands.command(aliases=('agressive','фппкуыышму','фпкуыышму'), description='Используйте off/on что бы включить/выключить агрессивность бота (ответы на ваши сообщения)')
    @commands.has_permissions(administrator=True)
    async def aggressive(self, ctx, arg):
        if arg in ('off','on'):
            self.config['ServerSettings'][str(ctx.guild.id)]['aggressive'] = arg
            
            with open('config.json', 'w', encoding='utf8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            await ctx.send('Статус агрессии изменен')
        else: await ctx.send('Неизвестный параметр. Используйте `off` или `on`')


def setup(client):
    client.add_cog(agress(client))