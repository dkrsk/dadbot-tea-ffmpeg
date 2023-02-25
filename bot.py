import discord
from discord.ext import commands

import json
import os

discord.opus.load_opus('/usr/lib/libopus.so.0')

#чтение конфиг файла
with open('/data/config.json', 'r', encoding='utf8') as f:
    config = json.load(f)
settings = config['config']

client = commands.Bot(
    command_prefix=settings['prefix'],
    strip_after_prefix = True,
    case_insensitive=True,
    intents = discord.Intents.all()
)

#подключение когов
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')


client.run(os.environ["DTOKEN"])

""" TODO: !s !автооткл !pause """
