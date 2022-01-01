import discord
from discord.ext import commands
from ext.db_module import fetch
from ext.db_module import update
import json
import time

def check_config():
    debug_db = fetch.one("config", 'name', 'DEBUG')
    debug_data = json.loads(debug_db)
    if debug_data['value'] == 'TRUE':
        return True
    else:
        return False

def developer_check():
    dev_db = fetch.all('developer')
    dev_data = json.loads(dev_db)
    dev_id = []
    for i in range(len(dev_data)):
        dev_id.append(int(dev_data["{i}".format(i = i)]["dev_id"]))
    return dev_id

class debug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def abc_hello(self, ctx):
        if check_config():
            await ctx.reply('Hello <@{user}> ! \nHow r u today? \n'.format(user=ctx.author.id), mention_author=True)
        else:
            await ctx.reply("Fitur debug pada bot ini sedang dimatikan oleh developer.")
    
    @commands.command()
    async def abc_ping(self, ctx):
        if check_config():
            before = time.monotonic()
            message = await ctx.reply("Pong!")
            ping = (time.monotonic() - before) * 1000
            await message.edit(content=f"Pong!, avr Ping is `{int(ping)}ms` for last 1-5 second interval")
        else:
            await ctx.reply("Fitur debug pada bot ini sedang dimatikan oleh developer.")

    @commands.command()
    async def setting(self, ctx, *params):
        if ctx.author.id not in developer_check():
            await ctx.reply("This Command Only for Developer!.")
        else:
            print(params)
            if len(params) == 2:
                jsondata = fetch.all("config")
                fetchdata = json.loads(jsondata)
                settingname = params[0]
                for i in range(len(fetchdata)):
                    looping = '{i}'.format(i = i)
                    if settingname == fetchdata[looping]['name']:
                        if params[1] == 'ON':
                            if update.one("config", "name", settingname, "value", 'TRUE'):
                                await ctx.reply("Setting Update Successfully.")
                            else:
                                await ctx.reply("Setting Update Failed.")
                                print("Setting Update Failed, Check DB Connection!")
                        elif params[1] == 'OFF':
                            if update.one("config", "name", settingname, "value", 'FALSE'):
                                await ctx.reply("Setting Update Successfully.")
                            else:
                                await ctx.reply("Setting Update Failed.")
                                print("Setting Update Failed, Check DB Connection!")
                        else:
                                await ctx.reply("Parameter's Invalid.")
                        notfounddata = False
                        break
                    else:
                        notfounddata = True
                        continue
                if notfounddata:
                    await ctx.reply("Data Setting for {data} is not found.".format(data = params[0]))
            elif params[0] == 'LS_DEV':
                dev_data = developer_check()
                dev_print = "**List Developer:**\n"
                for i in range(len(dev_data)):
                    dev_print += "{dev}\n".format(dev = self.client.get_user(dev_data[i]))
                await ctx.reply(dev_print)
                
            else:
                await ctx.reply("Parameter's invalid.")

def setup(client):
    client.add_cog(debug(client))