import discord
from discord.ext import commands

from .levels import l1

class Story(commands.Cog):
    """THE STORY OF BOT THAT WILL BE SENT BY THE BOT!"""
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command(name="story",help="Get to know about the storyline of bot.")
    async def story(self,ctx):
        em=discord.Embed(
            description="Galaxycity! The Rise of <insert a good word here>",
            color=discord.Color.dark_purple()
        ).add_field(
            name="** **",
            value="<add a good story here>",
            inline=False
        ).set_footer(
            text="TCR Bot Jam",
            icon_url=self.bot.user.display_avatar
        )
        await ctx.reply(embed=em)

    @commands.command(name="play", help="Play the galaxcity game")
    async def play(self, ctx):
        user = await self.bot.database.fetch_user(ctx.author.id)
        if user.level == 1:
            if await l1.start(ctx):
                user.level += 1
        await self.bot.database.update_user(user)

def setup(bot):
    bot.add_cog(Story(bot))