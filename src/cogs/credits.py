import discord
from discord import Embed
from discord.ext import commands
from discord.ext.pages import Page, Paginator


class Credits(commands.Cog):
    """A cog which contains credits for those who helped make this bot possible"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.contribs = {
            "midnight": {
                "id": 823588482273902672,
                "message": "Developing the bot, testing it,creating and adding levels, handling database.",
                "role": "Lead Developer",
                "color": 0x353635,
            },
            "ayu": {
                "id": 748053138354864229,
                "message": "Developing the bot, testing it, creaing API related commands, help commands, misc commands",
                "role": "Co-Developer",
                "color": 0xcc85ff
            },
            "tapu": {
                "id": 673105565689446409,
                "message": "Testing the bot, spamming commands, suggested to add map in `iss` command",
                "role": "Suggesstion Giver",
                "color": 0x85dcff
            },
            "andreaw": {
                "id": 724275771278884906,
                "message": "Testing the bot, Giving useful suggestions",
                "role": "Tester",
                "color": 0xfffd75
            },
            "arthex": {
                "id": 870635915461156917,
                "message": "Testing the bot, giving useful suggestions",
                "role": "Tester",
                "color": 0xffd899
            },
        }

    @commands.command(
        name="credits", aliases=["creds","credit","cred"], help="People who made this bot possible"
    )
    async def credits(self, ctx):
        pages = [
            Page(
                embeds=[
                    Embed(
                        title="This is the list of people who helped make this bot possible",
                    ).set_image(url="https://share.creavite.co/Lv2Sds8xi2gFBakY.gif")
                ]
            )
        ]
        for key, value in self.contribs.items():
            user = await self.bot.fetch_user(value["id"])
            if user:
                pages.append(
                    Page(
                        embeds=[
                            Embed(
                                title=user.name,
                                description=value["message"],
                                color= value["color"],
                            )
                            .set_thumbnail(url=user.avatar.url)
                            .add_field(name="Role", value=value["role"])
                        ]
                    )
                )
        paginator = Paginator(pages)
        await paginator.send(ctx)


def setup(bot):
    bot.add_cog(Credits(bot))