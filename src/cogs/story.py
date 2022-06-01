import discord
from discord.ext import commands

from .levels import l1, l2, l3


class Story(commands.Cog):
    """THE STORY OF BOT THAT WILL BE SENT BY THE BOT!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="story", help="Get to know about the storyline of bot.")
    async def story(self, ctx):
        em = (
            discord.Embed(
                title="Galaxcity Game",
                description="This bot is based on a space themed story line. Use g!play to play the game",
                color=discord.Color.dark_purple(),
            )
            .set_footer(text="TCR Bot Jam 2022", icon_url=self.bot.user.display_avatar)
        )
        await ctx.reply(embed=em)

    @commands.command(name="play", help="Play the galaxcity game", aliases=["p"])
    async def play(self, ctx):
        user = await self.bot.database.fetch_user(ctx.author.id)
        if user.level == 1:
            if await l1.start(ctx):
                user.level += 1
        elif user.level == 2:
            if await l2.start(ctx):
                user.level += 1
        elif user.level == 3:
            if await l3.start(ctx):
                user.level += 1
        else:
            await ctx.send(
                embed=discord.Embed(
                    title="You have completed all levels.",
                    description="Use g!reset to reset your level, tries and score.",
                    color=ctx.bot.primary_theme,
                )
            )
        await self.bot.database.update_user(user)


def setup(bot):
    bot.add_cog(Story(bot))
