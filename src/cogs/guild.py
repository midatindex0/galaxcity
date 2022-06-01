import discord
from discord.ext import commands


class Guild(commands.Cog):
    """
    A cog to send message when bot joins a guild
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        em = discord.Embed(
            title="Joined a new server!",
            description=f"**{guild.name}**",
            colour=discord.Colour.purple(),
        )
        em.set_image(url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif")
        em.set_thumbnail(url=guild.icon.url)
        em.set_footer(
            text=f"Requested by {guild.owner.name}", icon_url=guild.owner.display_avatar
        )
        em.add_field(
            name="Members",
            value=f"{guild.member_count}",
        )
        em.add_field(
            name="Channels",
            value=f"{len(guild.channels)}",
        )

        await self.bot.get_channel(978473001991413801).send(embed=em)
        for ch in guild.text_channels:
            if (
                "general" in ch.name.lower()
                or "bot-commands" in ch.name.lower()
                or "bot-logs" in ch.name.lower()
                or "testing" in ch.name.lower()
                or "bot-testing" in ch.name.lower()
            ):
                await ch.send(
                    embed=discord.Embed(
                        title="Thanks for inviting!",
                        description="I'm glad you invited me to your server! do `g!help` to see what I can do!",
                        colour=discord.Colour.purple(),
                    )
                    .set_image(url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif")
                    .set_thumbnail(url=self.bot.user.display_avatar)
                )
                break


def setup(bot):
    bot.add_cog(Guild(bot))
