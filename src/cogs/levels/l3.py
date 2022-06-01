import random
from typing import List
import asyncio

import discord
from discord import Embed, Interaction, ui
from discord.ext.commands import Context

from .script import l3_c1


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


class Duel(ui.View):
    def __init__(self, ctx: Context):
        super().__init__()
        self.ctx = ctx
        self.cleared = False
        self.try_again = False

        async def interaction_check(interaction: Interaction):
            if ctx.author.id == interaction.user.id:
                return True
            return False

        self.interaction_check = interaction_check

        self.health_a = 100
        self.health_b = 100

    @ui.button(label="Attack", style=discord.ButtonStyle.red, emoji="⚔️")
    async def attack(self, button: ui.Button, interaction: discord.Interaction):
        if random.choice([True, False]):
            self.health_b -= random.randint(5, 15)
            await self.message.edit(
                embed=await self.create_embed(
                    "You attacked and pulped Zark Muckerberg", interaction=interaction
                ),
                view=self,
            )
        else:
            await self.message.edit(
                embed=await self.create_embed(
                    "You attacked but the Zark Muckerberg dodged! Fuck!",
                    interaction=interaction,
                ),
                view=self,
            )
        await asyncio.sleep(2)
        try:
            await self.op_move(interaction)
        except discord.errors.InteractionResponded:
            pass

    @ui.button(label="Heal", style=discord.ButtonStyle.green, emoji="💉")
    async def heal(self, button: ui.Button, interaction: discord.Interaction):
        if random.choice([True, False]):
            self.health_a += random.randint(5, 15)
            await self.message.edit(
                embed=await self.create_embed(
                    "You gained some health", interaction=interaction
                ),
                view=self,
            )
        else:
            await self.message.edit(
                embed=await self.create_embed(
                    "The meds didn't work! Fuck!", interaction=interaction
                ),
                view=self,
            )
        await asyncio.sleep(2)
        try:
            await self.op_move(interaction)
        except discord.errors.InteractionResponded:
            pass

    async def op_move(self, interaction: discord.Interaction):
        if random.choice([True, False]):
            if random.choice([True, False]):
                self.health_b += random.randint(5, 15)
                await self.message.edit(
                    embed=await self.create_embed(
                        "Zark healed himself with his tongue licking.",
                        interaction=interaction,
                    )
                )
            else:
                await self.message.edit(
                    embed=await self.create_embed(
                        "Zark's tongue is injured. He couldn't heal himself.",
                        interaction=interaction,
                    )
                )
        else:
            if random.choice([True, False]):
                self.health_a -= random.randint(5, 15)
                await self.message.edit(
                    embed=await self.create_embed(
                        "Zark used his tongue to give you a nice blow.",
                        interaction=interaction,
                    )
                )
            else:
                await self.message.edit(
                    embed=await self.create_embed(
                        "Zark's tongue is injured. He couldn't attack you.",
                        interaction=interaction,
                    )
                )

    async def create_embed(self, message: str, interaction: discord.Interaction):
        if self.health_a > 100:
            self.health_a = 100
        if self.health_b > 100:
            self.health_b = 100
        if self.health_a < 1:
            self.health_a = 0
            view = TryAgain(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(
                    title="Zark killed you, he remains the ruler of this planet."
                ),
                view=view,
            )
            self.disable_all_items()
            self.try_again = not (await view.wait())
            await view.message.delete_original_message()
            self.stop()
        if self.health_b < 1:
            self.health_b = 0
            view = Next(self.ctx)
            view.message = await interaction.response.send_message(
                embed=Embed(
                    title="You defeated Zark and become the new ruler of this planet."
                ),
                view=view,
            )
            self.cleared = True
            await view.wait()
            await view.message.delete_original_message()
            self.stop()
        try:
            await interaction.response.defer()
        except (AttributeError, discord.errors.InteractionResponded):
            pass
        health_a_str = "⬜"
        health_b_str = "⬜"
        for _ in range(int(self.health_a / 10)):
            health_a_str += "🟩"
        for _ in range(int(self.health_b / 10)):
            health_b_str += "🟥"

        emded = (
            Embed(
                title=message,
                description="Your only option is to fight to death",
                color=self.ctx.bot.primary_theme,
            )
            .add_field(
                name=f"Your Health: {self.health_a}%", value=health_a_str, inline=False
            )
            .add_field(
                name=f"Zark Muckerberg: {self.health_b}%",
                value=health_b_str,
                inline=False,
            )
        )
        return emded

    async def play(self, message: discord.Message):
        self.message = message
        await message.edit(
            embed=await self.create_embed("The final battle", None), view=self
        )


async def start(ctx: Context):
    while True:
        cleared = False
        embed = Embed(
            title=l3_c1["title"],
            description=l3_c1["description"],
            color=ctx.bot.primary_theme,
        )
        view = Next(ctx)
        message = await ctx.send(embed=embed, view=view)
        await view.wait()
        game = Duel(ctx)
        await game.play(message)
        await game.wait()
        if not game.cleared:
            if game.try_again:
                await message.delete()
                continue
            break
        embed = Embed(
            title="Congrats! You have completed All the levels.",
            color=ctx.bot.primary_theme,
        ).set_footer(text="Use g!reset to reset your score and levels.")
        await message.edit(embed=embed, view=None)
        cleared = True
        break
    if cleared:
        user = await ctx.bot.database.fetch_user(id=ctx.author.id)
        user.score += 30
        user.tries += 1
        await ctx.bot.database.update_user(user)
    return cleared
