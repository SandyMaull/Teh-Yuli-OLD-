from dotenv import load_dotenv
import os
import time
import discord
from discord.ext import commands
from ext import music
from ext.albion import item
from ext.db_module import connection
from ext.db_module import create_config
from ext.db_module import fetch
from ext.db_module import update
from discord_components import DiscordComponents
import json

load_dotenv()
cogs = [music]
albioncogs_item = [item]
client = commands.Bot(command_prefix='?', intents = discord.Intents.all())

# create_config.create()

@client.event
async def on_ready():
    print("{0.user} successful log in! ".format(client))
    await client.change_presence(activity=discord.Game("Price Checker"))
    DiscordComponents(client)

def checkdata():
    debug_stats = fetch.one("config", 'name', 'DEBUG')
    debug_data = json.loads(debug_stats)
    if debug_data['value'] == 'TRUE':
        return True
    else:
        return False

for i in range(len(cogs)):
    cogs[i].setup(client)

for i in range(len(albioncogs_item)):
    albioncogs_item[i].setup(client)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    if msg.startswith('$setting'):
        author = "{author}".format(author = message.author)
        author = author.split('#')[1]
        if author == '8887':
            settingdata = msg.split('$setting ', 1)[1]
            settingdata1 = settingdata.split()[0]
            settingdata2 = settingdata.split(settingdata1 + " ", 1)[1]
            jsondata = fetch.all("config")
            fetchdata = json.loads(jsondata)
            i = 0
            commanddata = []
            while i < len(fetchdata):
                looping = '{i}'.format(i = i)
                commanddata.append(fetchdata[looping]['name'])
                i += 1
            if any(word in settingdata1 for word in commanddata):
                if settingdata2 == 'ON':
                    if update.one("config", "name", settingdata1, "value", 'TRUE'):
                        await message.channel.send("Setting Update Successfully!")
                    else:
                        print("Setting Update Failed!")
                if settingdata2 == 'OFF':
                    if update.one("config", "name", settingdata1, "value", 'FALSE'):
                        await message.channel.send("Setting Update Successfully!")
                    else:
                        print("Setting Update Failed!")
        else:
            await message.channel.send("You're not Author! This action cannot be used.")

    if checkdata():
        if msg.startswith('$hello'):
            await message.channel.send('Hello {user} ! \nHow r u today? \n'.format(user=message.author))
        if msg.startswith('$ping'):
            before = time.monotonic()
            message = await message.channel.send("Pong!")
            ping = (time.monotonic() - before) * 1000
            await message.edit(content=f"Pong!, avr Ping is `{int(ping)}ms` for last 1-5 second interval")

    else:
        return
    await client.process_commands(message)

client.run(os.getenv('TOKEN'))