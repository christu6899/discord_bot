import discord
import datetime
from discord.ext import commands
import json
from core.classes import Cog_Extension
with open('setting.json','r',encoding='utf8') as jfile:
    jdata=json.load(jfile)

class Event(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_member_join(self,member):

        channel = self.bot.get_channel(int(jdata["Welcome_channel"]))
        await channel.send(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self,member):

        channel = self.bot.get_channel(int(jdata["Leave_channel"]))
        await channel.send(f'{member} leave!')

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        
        notice_channel = self.bot.get_channel(int(jdata["Voice_channel_record"]))

        if before.channel is None and after.channel is not None:
            color=0x34dac7
            title="Member join voice channel"
            description=(f'**{member}** joined #{after.channel.name}')
            embed=self.set_embed(member,title,description,color)
            await notice_channel.send(embed=embed)
        elif before.channel == after.channel:     
            return

        elif before.channel is not None and after.channel is not None:

            color=0x34dac7
            title="Member change voice channel"
            description=(f'**Before** #{before.channel.name} \n **+After** #{after.channel.name}')
            embed=self.set_embed(member,title,description,color)
            await notice_channel.send(embed=embed)

        else:
            color=0xff0000
            title="Member left voice channel"
            description=(f'**{member}** lefted #{before.channel.name}')
            embed=self.set_embed(member,title,description,color)
            await notice_channel.send(embed=embed)

    def set_embed(self,member,title,description,color):

        embed=discord.Embed(title=title, description=description, color=color, timestamp=datetime.datetime.now().replace(tzinfo=datetime.timezone(datetime.timedelta(hours=8))))
        embed.set_author(name=member,icon_url=member.avatar_url)
        return embed

    @commands.Cog.listener()
    async def on_message(self,message):

        if message.author == self.bot.user: 
            return
        if message.content =='dick':
            num=len(message.author.voice.channel.members)
            await message.channel.send(f'這裡有{num}根雞雞，錯了我可不管')
        if message.channel.id == jdata["18+"]:
            await message.channel.send('不可以色色')


def setup(bot):
    bot.add_cog(Event(bot))
