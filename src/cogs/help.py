from operator import inv
import discord
from discord.ext import commands

class Help(commands.Cog):
    """
    A COG TO STORE ALL HELP COMMANDS OF THE BOT
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="help", aliases=["h", "halp", "commands", "cmds", "command", "cmd"],invoke_without_command=True)
    async def help(self, ctx):
        em=discord.Embed(
            title="Commands:",
            description="Do `g!help <command>` to get more info about a command",
            colour=discord.Colour.purple()
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        em.add_field(
            name="Story",
            value="`play` **⌬** `reset` **⌬** `profile`",
            inline=False
        )
        em.add_field(
            name="Space",
            value="`locate` **⌬** `pic-of-day`",
            inline=False
        )
        em.add_field(
            name="Miscellaneous",
            value="`credits` **⌬** `story`",
            inline=False
        )
        await ctx.send(embed=em)

    @help.command(name="reset")
    async def reset(self, ctx):
        em=discord.Embed(
            title="g!reset",
            description="Reset your level, tries and score.",
            colour=discord.Colour.purple()
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        em.add_field(
            name="Aliases",
            value="`g!r`",
            inline=False
        )

        await ctx.send(embed=em)
    
    @help.command(name="play")
    async def play(self,ctx):
        em=discord.Embed(
            title="g!play",
            description="Play the game",
            colour=discord.Colour.purple()
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        em.add_field(
            name="Aliases",
            value="`g!p`",
            inline=False
        )
        await ctx.send(embed=em)
    
    @help.command(name="profile")
    async def profile(self,ctx):
        em=discord.Embed(
            title="g!profile",
            description="Get your profile",
            colour=discord.Colour.purple()
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        em.add_field(
            name="Aliases",
            value="`g!pf` **⌬** `g!id` **⌬** `g!prof`",
            inline=False
        )

        await ctx.send(embed=em)
    
    @help.command(name="story")
    async def story(self,ctx):
        em=discord.Embed(
            title="g!story",
            description="Get to know about the storyline of bot.",
            colour=discord.Colour.purple()
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)
    
    @help.command(name="credits")
    async def credits(self,ctx):
        em=discord.Embed(
            title="g!credits",
            description="Get to know about the people who made this bot possible",
            colour=discord.Colour.purple()
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        em.add_field(
            name="Aliases",
            value="`g!cred` **⌬** `g!creds` **⌬** `g!credit`",
            inline=False
        )
        await ctx.send(embed=em)
    
    @help.command(name="locate")
    async def locate(self,ctx):
        em=discord.Embed(
            title="g!locate",
            description="Get to know about the locations of the International Space Station",
            colour=discord.Colour.purple()
        )
        em.add_field(
            name="Aliases",
            value="`g!loc` **⌬** `g!iss` **⌬** `g!location`",
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)
    
    @help.command(name="pic-of-day")
    async def pic_of_day(self,ctx):
        em=discord.Embed(
            title="g!pic-of-day",
            description="Get to know about the picture of the day",
            colour=discord.Colour.purple()
        )
        em.set_image(
            url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif"
        )
        em.set_thumbnail(
            url=self.bot.user.display_avatar
        )
        em.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.display_avatar
        )
        em.add_field(
            name="Alaiases",
            value="`potd` **⌬** `pod` **⌬** `picture-of-the-day` **⌬** `picofday`",
            inline=False
        )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Help(bot))