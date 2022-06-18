
import datetime
import discord
from discord.ext import commands
from discord.flags import Intents
import json,os
with open('setting.json','r',encoding='utf8') as jfile:
    jdata=json.load(jfile)

Intents = discord.Intents.default()
Intents.members = True

bot = commands.Bot(command_prefix='!',intents=Intents)

@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded{extension} done.')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Un-Loaded{extension} done.')
  
@bot.command()
async def reload(ctx,extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Re-Loaded{extension} done.')
  
for filename in os.listdir('./cmds'):
    if filename.endswith('.py') and filename!='covid.py':
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['TOKEN']) 
