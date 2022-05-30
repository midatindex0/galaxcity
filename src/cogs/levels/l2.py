import random
from typing import List

import discord
from discord import Embed, Interaction, ui
from discord.ext.commands import Context

from .script import l2_c1, l2_c2


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


class BtnColor(ui.View):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.cleared = False
        self.try_again = False
        super().__init__()

    @ui.button(label="Red", style=discord.ButtonStyle.green, emoji="🔵")
    async def red(self, button: ui.Button, interaction: discord.Interaction):
        view = Next(self.ctx)
        view.message = await interaction.response.send_message(
            embed=Embed(title="Correct button!", color=self.ctx.bot.success), view=view
        )
        self.cleared = True
        await view.wait()
        await view.message.delete_original_message()
        self.stop()

    @ui.button(label="Green", style=discord.ButtonStyle.blurple, emoji="🔴")
    async def green(self, button: ui.Button, interaction: discord.Interaction):
        view = TryAgain(self.ctx)
        view.message = await interaction.response.send_message(
            embed=Embed(
                title="Wrong button! Xilon's guards broke into the rocket and dragged you out.",
                color=self.ctx.bot.fail,
            ),
            view=view,
        )
        self.try_again = not (await view.wait())
        await view.message.delete_original_message()
        self.stop()

    @ui.button(label="blue", style=discord.ButtonStyle.red, emoji="🟢")
    async def blue(self, button: ui.Button, interaction: discord.Interaction):
        view = TryAgain(self.ctx)
        view.message = await interaction.response.send_message(
            embed=Embed(
                title="Wrong button! Xilon's guards broke into the rocket and dragged you out.",
                color=self.ctx.bot.fail,
            ),
            view=view,
        )
        self.try_again = not (await view.wait())
        await view.message.delete_original_message()
        self.stop()


class RocketControls(ui.View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.ctx = ctx
        self.cleared = False
        self.try_again = False

        async def interaction_check(interaction: discord.Interaction):
            if ctx.author.id == interaction.user.id:
                if len(self.grid) > 1:
                    return True
                else:
                    view = TryAgain(self.ctx)
                    view.message = await interaction.response.send_message(
                        embed=Embed(title="You passed the plannet and entered a blackhole."),
                        view=view,
                    )
                    self.try_again = not (await view.wait())
                    await view.message.delete_original_message()
                    self.stop()
            return False

        self.interaction_check = interaction_check

        self.target = ["⬛", "⬛", "⬛", "⬛", "🌎", "⬛", "⬛", "⬛", "⬛"]
        self.initial_rocket = ["⬛", "⬛", "⬛", "⬛", "🚀", "⬛", "⬛", "⬛", "⬛"]

    @ui.button(style=discord.ButtonStyle.blurple, emoji="↖️")
    async def left(self, button: ui.Button, interaction: discord.Interaction):
        if self.rocket_index == 0:
            return
        self.rocket_index -= 1
        line = self.grid[len(self.grid) - 2]
        line = await self.insert_rocket(self.rocket_index, line, interaction)
        if line:
            self.grid = self.grid[: len(self.grid) - 2]
            self.grid.append(line)
            embed = self.generate_embed(self.grid)
            await self.update_game(embed)

    @ui.button(style=discord.ButtonStyle.blurple, emoji="⬆️")
    async def up(self, button: ui.Button, interaction: discord.Interaction):
        line = self.grid[len(self.grid) - 2]
        line = await self.insert_rocket(self.rocket_index, line, interaction)
        if line:
            self.grid = self.grid[: len(self.grid) - 2]
            self.grid.append(line)
            embed = self.generate_embed(self.grid)
            await self.update_game(embed)

    @ui.button(style=discord.ButtonStyle.blurple, emoji="↗️")
    async def right(self, button: ui.Button, interaction: discord.Interaction):
        if self.rocket_index == 8:
            return
        self.rocket_index += 1
        line = self.grid[len(self.grid) - 2]
        line = await self.insert_rocket(self.rocket_index, line, interaction)
        if line:
            self.grid = self.grid[: len(self.grid) - 2]
            self.grid.append(line)
            embed = self.generate_embed(self.grid)
            await self.update_game(embed)

    def generate_line(self):
        line = []
        for _ in range(9):
            if random.choice([False, False, False, True, False]):
                line.append("🪐")
            else:
                line.append("⬛")
        return line

    def generate_embed(self, grid: List[List]):
        desc = ""
        for line in grid:
            for each in line:
                desc += each
            desc += "\n"
        return Embed(description=desc)

    async def insert_rocket(
        self, rocket_index: int, line: list, interaction: discord.Interaction
    ):
        if line[rocket_index] == "🪐":
            view = TryAgain(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(title="You crashed into an asteroid."),
                view=view,
            )
            self.try_again = not (await view.wait())
            await view.message.delete_original_message()
            self.stop()
            return
        elif line[rocket_index] == "🌎":
            view = Next(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(title="Good job navigating through those asteroids!"),
                view=view,
            )
            self.cleared = True
            await view.wait()
            await view.message.delete_original_message()
            self.stop()
        try:
            await interaction.response.defer()
        except discord.errors.InteractionResponded:
            pass
        line[rocket_index] = "🚀"
        return line

    async def update_game(self, embed: Embed):
        await self.message.edit(embed=embed, view=self)

    async def play(self, message: discord.Message):
        self.message = message
        grid = [self.target]
        for _ in range(9):
            grid.append(self.generate_line())
        grid.append(self.initial_rocket)
        self.grid = grid
        self.rocket_index = 4
        embed = self.generate_embed(grid=grid)
        await message.edit(embed=embed, view=self)


async def start(ctx: Context):
    while True:
        cleared = False
        embed = Embed(
            title=l2_c1["title"],
            description=l2_c1["description"],
            color=ctx.bot.primary_theme,
        )
        view = Next(ctx)
        message = await ctx.send(embed=embed, view=view)
        await view.wait()
        view = BtnColor(ctx)
        embed = Embed(
            title="There are three buttons. A manual says you to press the green button to launch the rocket.",
            color=ctx.bot.primary_theme,
        )
        await message.edit(embed=embed, view=view)
        await view.wait()
        if not view.cleared:
            if view.try_again:
                await message.delete()
                continue
            break
        embed = Embed(
            title=l2_c2["title"],
            description=l2_c2["description"],
            color=ctx.bot.primary_theme,
        )
        view = Next(ctx)
        await message.edit(embed=embed, view=view)
        await view.wait()
        game = RocketControls(ctx)
        await game.play(message)
        await game.wait()
        if not game.cleared:
            if game.try_again:
                await message.delete()
                continue
            break
        embed = Embed(
            title="Congrats! You have completed level 2.", color=ctx.bot.primary_theme
        ).set_footer(text="Use g!play to play level 3")
        await message.edit(embed=embed, view=None)
        cleared = True
        break
    if cleared:
        user = await ctx.bot.database.fetch_user(id=ctx.author.id)
        user.score += 30
        user.tries += 1
        await ctx.bot.database.update_user(user)
    return cleared
