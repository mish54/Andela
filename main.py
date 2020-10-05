# main.py
import os
import asyncio
import datetime
import json

import discord
from dotenv import load_dotenv

from core.parser import Parser

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
parser = None

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            global parser
            parser = Parser(guild)
            print("I am alive.")
            break

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    output = parser.parse(message)
    if output is not None:
        print("OUTPUT: ")
        print(output)
        print("==================================")
        await message.channel.send(output)

client.run(TOKEN)
