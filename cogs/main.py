import discord
from discord.ext import commands

import json


class main(commands.Cog):

    def __init__(self,client):
        self.client = client
        with open('/data/config.json', 'r', encoding='utf8') as f:
            self.config = json.load(f)
        self.settings = self.config['config']

        for guild in self.client.guilds:
            guildSettings = self.config['ServerSettings'].get(str(guild.id))
            if not guildSettings:
                self.config['ServerSettings'].update({str(guild.id):{'aggressive':'on',
                                                                     'whiteChannel':None}})
                with open('config.json', 'w', encoding='utf8') as f:
                    json.dump(self.config, f, indent=4, ensure_ascii=False)
        


    @commands.Cog.listener()
    async def on_ready(self):
        status = discord.Status
        await self.client.change_presence(status=getattr(status,self.settings['status']),
                                          activity=discord.Activity(type=discord.ActivityType.watching,
                                          name=self.settings['watching']))

        print(f'-------------Bot activated!-------------\nCurrent servers: {len(self.client.guilds)}')


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.config['ServerSettings'].pop(str(guild.id))
        with open('config.json', 'w', encoding='utf8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.config['ServerSettings'].update({str(guild.id):{'aggressive':'on',
                                                             'whiteChannel':None}})
        #self.config['ServerSettings'][str(guild.id)].update({'aggressive':'on',
        #                                                     'whiteChannel':None})
        with open('config.json', 'w', encoding='utf8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)


def setup(client):
    client.add_cog(main(client))
