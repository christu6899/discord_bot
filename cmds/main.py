import covid
import sys
import json
import os
import random
import asyncio
import discord
from yt_dlp import YoutubeDL
from core.classes import Cog_Extension
from discord import FFmpegPCMAudio
from discord.ext import commands
import requests
import bs4
with open('setting.json','r',encoding='utf8') as jfile:
    jdata=json.load(jfile)

class Main(Cog_Extension):
	
    #透過氣象資料共享平台API撈出36小時指定縣市天氣數據
    @commands.command()
    async def 天氣(self,ctx,extension:str):
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-F8E15B60-8D01-4C59-82B7-8FC656653E59&limit=1&format=JSON&locationName={}&elementName='.format(extension)
        Data = requests.get(url)
        data  = (Data.json())['records']['location'][0]['weatherElement']
        await ctx.send('36小時天氣預報')

        for i in range(0,3):
            weather = data[0]['time'][i]['parameter']['parameterName']
            time = '{} ~ {}'.format(data[0]['time'][i]['startTime'][5:-3],data[0]['time'][i]['endTime'][5:-3])
            temp = "{} ~ {} °C".format(data[2]['time'][i]['parameter']['parameterName'],data[4]['time'][i]['parameter']['parameterName'])
            pop = data[1]['time'][i]['parameter']['parameterName']
            embed=discord.Embed(title=extension,color=0x00fbff)
            embed.add_field(name="天氣狀況", value=weather, inline=True)
            embed.add_field(name="溫度", value=temp, inline=True)
            embed.add_field(name="降雨機率", value=pop, inline=True)
            embed.set_footer(text=time)
            await ctx.send(embed=embed)

    #透過全球疫情地圖API獲取全台疫情數據
    @commands.command()
    async def covid(self,ctx):
        r = requests.get('https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4051&limited=TWN')
        data = (r.json()).pop()
        r = requests.get('https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=4002')
        death = r.json()
        await ctx.send("新增確診+" + data['a06'] + '\n' + "新增死亡+" + str(len(death)))

    #透過全球疫情地圖API獲取指定縣市疫情數據
    @commands.command()
    async def covidcity(self,ctx,extension:str):
        r = requests.get('https://covid-19.nchc.org.tw/api/covid19?CK=covid-19@nchc.org.tw&querydata=5002&limited={}'.format(extension))
        data = r.json()
        await ctx.send(extension + "\t新增確診+" + data[0]['a05'])

    #透過全球疫情地圖API獲取指定縣市行政區疫情數據
    @commands.command()
    async def coviddist(self,ctx,city:str,dist:str):
        cov = covid.CovidMap(city)
        data = cov.get_dist_data(dist)
        await ctx.send(city + '\t' + dist + "\t新增確診+" + data['a05'])

    #隨機抽出群友的口頭禪
    @commands.command()
    async def 每日一句(self,ctx):
        random_day=random.choice(jdata['everyday'])
        await ctx.send(random_day)

    #回報延遲
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

    #刪除指定數量的訊息
    @commands.command()
    async def clean(self, ctx, num:int):
        await ctx.channel.purge(limit=num+1)
    
    #晚餐抽籤
    @commands.command()
    async def dinner(self,ctx):
        if ctx.author.name=='yanbo':
            await ctx.send('問映黎吃啥')
        else:
            random_dinner=random.choice(jdata['Dinner'])
        await ctx.send(random_dinner)
    

def setup(bot):
    bot.add_cog(Main(bot))

