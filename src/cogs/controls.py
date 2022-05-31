import discord
from discord.ext import commands

from io import BytesIO
from PIL import Image,ImageDraw,ImageChops, ImageFont


def circle(pfp):
    size = (270, 270)
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

async def get_profile(member:discord.Member,level,fails,score):
        av = member.display_avatar
        data = BytesIO(await av.read())
        pfp = Image.open(data)
        pfp=circle(pfp)
        color="#ffffff"
        bg=Image.open("src/asset/imgs/bg.png")
        bg.paste(pfp,(17,67),pfp)
        font=ImageFont.truetype("src/asset/fonts/font.ttf",104)
        # 330,135
        draw=ImageDraw.Draw(bg)
        draw.text(
            xy=(330,135),
            text=f"User Id",
            font=font,
            fill=color
        )
        # 48,392
        name=str(member)
        font2=ImageFont.truetype("src/asset/fonts/font.ttf",62)
        if len(name)>16:name=f"{name[0:16]}..."
        
        draw.text(
            xy=(48,392),
            text=name,
            font=font2,
            fill=color
        )

        font3=ImageFont.truetype("src/asset/fonts/font.ttf",105)
        # 90,585
        draw.text(
            xy=(90,585),
            text=str(level),
            font=font3,
            fill=color
        )

        draw.text(
            xy=(90,735),
            text=str(fails),
            font=font3,
            fill=color
        )

        draw.text(
            xy=(90,1035),
            text=str(score),
            font=font3,
            fill=color
        )

        return bg

class Controls(commands.Cog):
    """
    ALL THE COMMANDS AND EVENTS RELATED TO CONTROLS
    """
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    
    @commands.command(name="profile",aliases=["prof","id","pf"])
    async def profile(self,ctx:commands.Context):
        """
        Profile Command
        """
        user = await self.bot.database.fetch_user(ctx.author.id)
        level = f"Level: {user.level}"
        tries = f"Tries: {user.tries}"
        score = f"Score: {user.score}"
        profile = await get_profile(member=ctx.author,level=level,fails=tries,score=score)
        with BytesIO() as image_binary:
            profile.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary,"profile.png"))

    @commands.command(name="reset", help="Reset your level, tries and score.",aliases=["r"])
    async def reset(self, ctx):
        user = await self.bot.database.fetch_user(ctx.author.id)
        user.level = 1
        user.tries = 0
        user.score = 0
        await self.bot.database.update_user(user)
        embed = discord.Embed(title="Reset your level, tries and score", color=self.bot.primary_theme)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Controls(bot))
