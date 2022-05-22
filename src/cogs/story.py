import discord
from discord.ext import commands

class Story(commands.Cog):
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

def setup(bot):
    bot.add_cog(Story(bot))