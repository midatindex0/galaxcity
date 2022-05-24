import discord
from discord.ext import commands
from PIL import Image,ImageDraw,ImageChops

def circles(pfp,size = (220,220)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

class Controls(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot=bot

    async def get_profile(self,guild:discord.Guild,member:discord.Member,level,fails,hint_used):
        pfp=