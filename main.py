from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from ext import music
from ext import debug
from ext.albion import item

from discord_components import DiscordComponents

load_dotenv()
debug_cogs = [debug]
music_cogs = [music]
albion_cogs_item = [item]
client = commands.Bot(command_prefix='?/', intents = discord.Intents.all())


@client.event
async def on_ready():
    print("{0.user} successful log in! ".format(client))
    await client.change_presence(activity=discord.Game("Price Checker"))
    DiscordComponents(client)

for i in range(len(debug_cogs)):
    debug_cogs[i].setup(client)


for i in range(len(music_cogs)):
    music_cogs[i].setup(client)

for i in range(len(albion_cogs_item)):
    albion_cogs_item[i].setup(client)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    await client.process_commands(message)


client.run(os.getenv('TOKEN'))