# main.py
import os
import discord
from dotenv import load_dotenv
import core.parser

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
parser = None
guild = None

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            parser = Parser(guild)
            break

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    output = parser.parse(message)
    if output is not None:
        await message.channel.send(output)

client.run(TOKEN)
