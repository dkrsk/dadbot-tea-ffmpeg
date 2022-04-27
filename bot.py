import discord
from discord.ext import commands

import json
import os

#read config
with open('config.json', 'r', encoding='utf8') as f:
    config = json.load(f)
settings = config['config']

client = commands.Bot(
    command_prefix=settings['prefix'],
    strip_after_prefix = True,
    case_insensitive=True
)

#connect cogs
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')


client.run(settings['token'])
