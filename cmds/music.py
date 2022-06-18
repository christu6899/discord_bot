import json
import queue
import os
import random
import asyncio
import discord
import yt_dlp
from yt_dlp import YoutubeDL
from core.classes import Cog_Extension
from discord import FFmpegPCMAudio
from discord.ext import commands

with open('setting.json','r',encoding='utf8') as jfile:
    jdata=json.load(jfile)

class Music(commands.Cog):
    def __init__(self,bot):
        self.music_list=[]
        self.bot=bot
        self.now=''
    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            voice.stop()
    @commands.command()
    async def leave(self,ctx):
        if ctx.voice_client:
            self.music_list.clear()
            await ctx.guild.voice_client.disconnect()
            
    @commands.command()
    async def play(self,ctx,url:str):
        voice = discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
        with YoutubeDL() as ydl:
            res = ydl.extract_info(url=url,download=False)
        title = res.get('title')
        self.music_list.append({'name':title,'url':url})
        if voice.is_playing():
           await ctx.send('加入播放列表') 
        else:
            await self.playMusic(ctx)
        
    async def playMusic(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients,guild=ctx.guild)

        ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':'192',
        }]
        }
        info=self.music_list.pop(0)
        title=info['name']
        self.now=title
        url=info['url']
        temp=title
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        for file in os.listdir("./"):
            if file.endswith('.mp3'):
                os.rename(file,'song.mp3')
        source=FFmpegPCMAudio('song.mp3')
        voice.play(source)
        await ctx.send(f'正在播放{title}')
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        os.remove('song.mp3')
        
        if not self.music_list:
            await ctx.send('沒歌了')
        else:
            await ctx.send('將播放下一首歌曲')
            await self.playMusic(ctx)

    @commands.command()
    async def pause(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send('沒在播歌')

    @commands.command()
    async def resume(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('沒有暫停')

    @commands.command()
    async def skip(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
        else:
            await ctx.send('沒在播歌')
            
    @commands.command()
    async def q(self,ctx):
        if not self.music_list:
            await ctx.send('沒歌')
        else:    
            for i in range(len(self.music_list)):
                await ctx.send(self.music_list[i]['name'])
                
    @commands.command()        
    async def stop(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            self.music_list.clear()
        else:
            await ctx.send('沒在播歌')

def setup(bot):
    bot.add_cog(Music(bot))

