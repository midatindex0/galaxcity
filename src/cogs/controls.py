import discord
from discord.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO


def circle(pfp, size=(100, 100)):

    pfp = pfp.resize(size).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


async def get_profile(member: discord.Member, level, fails, score):
    bg = Image.open("src/asset/imgs/bg2.jpg")
    av = member.display_avatar
    data = BytesIO(await av.read())
    pfp = Image.open(data)
    pfp = circle(pfp)

    title_font = ImageFont.truetype("src/asset/fonts/font.otf", 30)
    defs = ImageFont.truetype("src/asset/fonts/font.otf", 17)
    name_font = ImageFont.truetype("src/asset/fonts/font.otf", 20)

    title = "Your Game Profile"
    name = f"{member.name}"
    ids = f"> ID: {member.id}"

    draw = ImageDraw.Draw(bg)
    draw.text((100, 10), text=title, font=title_font, fill="#ffffff")
    draw.text((150, 60), text=name, font=name_font, fill="#ffffff")
    draw.text((170, 90), text=ids, font=defs, fill="#ffffff")
    draw.text((170, 115), text=level, font=defs, fill="#ffffff")
    draw.text((170, 140), text=fails, font=defs, fill="#ffffff")
    draw.text((170, 165), text=score, font=defs, fill="#ffffff")

    bg.paste(pfp, (30, 60), pfp)

    return bg


class Controls(commands.Cog):
    """
    ALL THE COMMANDS AND EVENTS RELATED TO CONTROLS
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="profile", aliases=["prof", "id", "pf"])
    async def profile(self, ctx: commands.Context):
        """
        Profile Command
        """
        user = await self.bot.database.fetch_user(ctx.author.id)
        level = f"> Level: {user.level}"
        tries = f"> Tries: {user.tries}"
        score = f"> Score: {user.score}"
        profile = await get_profile(
            member=ctx.author, level=level, fails=tries, score=score
        )
        with BytesIO() as image_binary:
            profile.save(image_binary, "PNG")
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, "profile.png"))

    @commands.command(
        name="reset", help="Reset your level, tries and score.", aliases=["r"]
    )
    async def reset(self, ctx):
        user = await self.bot.database.fetch_user(ctx.author.id)
        user.level = 1
        user.tries = 0
        user.score = 0
        await self.bot.database.update_user(user)
        embed = discord.Embed(
            title="Reset your level, tries and score", color=self.bot.primary_theme
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Controls(bot))
