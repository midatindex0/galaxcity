from pydoc import visiblename
import random

import discord
from discord import Embed, ui
from discord.ext.commands import Context

from .script import l1_c1, l1_c2, l1_c3, l1_c2_conti


class Next(ui.View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.timeout = None

        async def interaction_check(interaction: discord.Integration):
            return ctx.author.id == interaction.user.id

        self.interaction_check = interaction_check

    @ui.button(label="Next", style=discord.ButtonStyle.green)
    async def next(self, button: ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.stop()


class TryAgain(ui.View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.timeout = 60

        async def interaction_check(interaction: discord.Integration):
            return ctx.author.id == interaction.user.id

        self.interaction_check = interaction_check

    @ui.button(label="Try again", style=discord.ButtonStyle.red)
    async def try_again(self, button: ui.Button, interaction: discord.Interaction):
        user = await interaction.client.database.fetch_user(interaction.user.id)
        user.score -= 5
        user.tries += 1
        await interaction.client.database.update_user(user)
        await interaction.response.defer()
        self.stop()


class Drug(ui.View):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.cleared = False
        self.try_again = False
        super().__init__()

    @ui.button(
        label="Hit him with a hammer", style=discord.ButtonStyle.blurple, emoji="🔨"
    )
    async def hammer(self, button: ui.Button, interaction: discord.Interaction):
        view = TryAgain(self.ctx)
        view.message = await interaction.response.send_message(
            embed=Embed(
                title="You were caught by Xilon's bodyguards and exiled to North Korea. Try again."
            ),
            view=view,
        )
        self.try_again = not (await view.wait())
        await view.message.delete_original_message()
        self.stop()

    @ui.button(label="Drug his drink", style=discord.ButtonStyle.blurple, emoji="🍷")
    async def drug(self, button: ui.Button, interaction: discord.Interaction):
        if random.choice([True, False]):
            view = Next(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(title="Good job! Now off to the next chapter."), view=view
            )
            self.cleared = True
            await view.wait()
            await view.message.delete_original_message()

        else:
            view = TryAgain(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(
                    title="Xilon smelled something fishy in his drink and beat you to a pulp."
                ),
                view=view,
            )
            self.try_again = not (await view.wait())
            await view.message.delete_original_message()
        self.stop()

    @ui.button(label="Remain Xilon's sex slave", style=discord.ButtonStyle.blurple)
    async def none(self, button: ui.Button, interaction: discord.Interaction):
        view = TryAgain(self.ctx)
        view.message = await interaction.response.send_message(
            embed=Embed(title="Atleast try to play fucking the game! Try again."),
            view=view,
        )
        self.try_again = not (await view.wait())
        await view.message.delete_original_message()
        self.stop()

    @ui.button(label="Hint", style=discord.ButtonStyle.green)
    async def hint(self, button: ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Xilon sure likes his drinks", ephemeral=True
        )


class Bypass51(ui.View):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.cleared = False
        self.try_again = False
        super().__init__()

    @ui.button(
        label="Hit guard with a rock", style=discord.ButtonStyle.blurple, emoji="🪨"
    )
    async def rock(self, button: ui.Button, interaction: discord.Interaction):
        view = TryAgain(self.ctx)
        view.message = await interaction.response.send_message(
            embed=Embed(
                title="You hit a guard but the others guards created a thousand holes in your body."
            ),
            view=view,
        )
        self.try_again = not (await view.wait())
        await view.message.delete_original_message()
        self.stop()

    @ui.button(label="Search for another entrance", style=discord.ButtonStyle.blurple)
    async def another(self, button: ui.Button, interaction: discord.Interaction):
        if random.choice([True, False]):
            view = Next(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(
                    title="You searched really hard and found a small gap. Well done!"
                ),
                view=view,
            )
            self.cleared = True
            await view.wait()
            await view.message.delete_original_message()

        else:
            view = TryAgain(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(
                    title="A guard caught you and shot you to death. Try again."
                ),
                view=view,
            )
            self.try_again = not (await view.wait())
            await view.message.delete_original_message()

        self.stop()

    @ui.button(
        label="Tell the guards that you are a basement scientist",
        style=discord.ButtonStyle.blurple,
    )
    async def scientist(self, button: ui.Button, interaction: discord.Interaction):
        view = Next(self.ctx)
        view.message = await interaction.response.send_message(
            embed=Embed(
                title="Guards believed you preety easily and allowed you to enter"
            ),
            view=view,
        )
        self.cleared = True
        await view.wait()
        await view.message.delete_original_message()
        self.stop()

    @ui.button(label="Hint", style=discord.ButtonStyle.green)
    async def hint(self, button: ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Sometimes it's good to be brave", ephemeral=True
        )


class PasswordModal(ui.Modal):
    def __init__(self, ctx: Context, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.cleared = False
        self.try_again = False
        self.add_item(ui.InputText(label="Password"))

    async def callback(self, interaction: discord.Interaction):
        if self.children[0].value == "100512":
            view = Next(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(title="Correct password! The door opened and you entered."),
                view=view,
            )
            self.cleared = True
            await view.wait()
            await view.message.delete_original_message()
        else:
            view = TryAgain(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(
                    title="Wrong password! The guard caught and tortured you to death. Try again."
                ),
                view=view,
            )
            self.try_again = not (await view.wait())
            await view.message.delete_original_message()
        self.stop()


class Password(ui.View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.ctx = ctx
        self.timeout = 60
        self.cleared = False
        self.try_again = False

    @ui.button(label="Enter Password", style=discord.ButtonStyle.green)
    async def next(self, button: ui.Button, interaction: discord.Interaction):
        modal = PasswordModal(self.ctx, title="Password")
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.cleared = modal.cleared
        self.try_again = modal.try_again
        self.stop()

    @ui.button(label="Hint", style=discord.ButtonStyle.green)
    async def hint(self, button: ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(
            "The letter said Xilon's army base has 64 guards", ephemeral=True
        )


async def start(ctx: Context):
    while True:
        cleared = False
        embed = Embed(
            title=l1_c1["title"],
            description=l1_c1["description"],
            color=ctx.bot.primary_theme,
        ).set_image(url="https://onlinetextgenerator.com/2022/05/25/JASIdWiA.png")
        view = Next(ctx)
        message = await ctx.send(embed=embed, view=view)
        await view.wait()
        view = Drug(ctx)
        embed = Embed(title="How will you get information out of Xilon?")
        await message.edit(embed=embed, view=view)
        await view.wait()
        if not view.cleared:
            if view.try_again:
                await message.delete()
                continue
            break
        # C2
        embed = (
            Embed(
                title=l1_c2["title"],
                description=l1_c2["description"],
                color=ctx.bot.primary_theme,
            )
            .set_image(
                url="https://cdn.discordapp.com/attachments/900369794489016380/978914828573884426/letter.png"
            )
            .set_footer(
                text="Password: bnVtYmVycyBpbiB0aGUgbGV0dGVyIHBsYWNlZCBzZXJpYWxseQ=="
            )
        )
        view = Next(ctx)
        await message.edit(embed=embed, view=view)
        await view.wait()
        # C3
        view = Bypass51(ctx)
        embed = Embed(
            title=l1_c3["title"],
            description=l1_c3["description"],
            color=ctx.bot.primary_theme,
        )
        await message.edit(embed=embed, view=view)
        await view.wait()
        if not view.cleared:
            if view.try_again:
                await message.delete()
                continue
            break
        # C2-CONTI
        view = Password(ctx)
        embed = Embed(
            title=l1_c2_conti["title"],
            description=l1_c2_conti["description"],
            color=ctx.bot.primary_theme,
        )
        await message.edit(embed=embed, view=view)
        await view.wait()
        if not view.cleared:
            if view.try_again:
                await message.delete()
                continue
            break
        embed = Embed(title="Congrats! You have completed level 1.", color=ctx.bot.primary_theme).set_footer(
            text="Use g!play to play level 2"
        )
        await message.edit(embed=embed, view=None)
        cleared = True
        break
    if cleared:
        user = await ctx.bot.database.fetch_user(id=ctx.author.id)
        user.score += 30
        user.tries += 1
        await ctx.bot.database.update_user(user)
    return cleared
