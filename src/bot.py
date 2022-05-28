import time
import os

import colorlog, logging

import discord
from discord.ext import commands

from config.config import BOT_LOG_LEVEL as BOTL, LOG_LEVEL

logging.addLevelName(BOTL, "BOT")
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s(%(name)s) %(levelname)s:%(reset)s%(cyan)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "BOT": "purple",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
    )
)
logger = colorlog.getLogger()
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)

cogs = ["story","controls","info"]
loaded_cogs = []
bot = commands.Bot(
    command_prefix="g!",
    intents=discord.Intents.all(),
    status=discord.Status.idle,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="my development."
    ),
)
bot.starttime = int(time.time())
for i in cogs:
    bot.load_extension(f"cogs.{i}")
    loaded_cogs.append(i)


@bot.event
async def on_ready():
    logger.log(BOTL, "Logged in as: {0}".format(bot.user))
    for i in loaded_cogs:
        logger.log(BOTL, f"{i}.py is Loaded!")


def is_owner():
    def predicate(ctx):
        if ctx.author.id in (823588482273902672, 748053138354864229):
            return True
        return False

    return commands.check(predicate)


@bot.command(name="ping", help="Return's Bot Latency.")
async def ping(ctx):
    await ctx.reply("Pong!")


@bot.group(name="cog", help="Cog Based Commands", invoke_without_command=True)
@is_owner()
async def cog(ctx):
    await ctx.reply(
        embed=discord.Embed(color=discord.Color.green(), description=loaded_cogs)
    )


@cog.command(aliases=["ul"], name="unload", help="Unload cogs")
@is_owner()
async def unload(ctx, *, cogss: str = None):
    if not cogss:
        for i in cogs:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Unloaded {i}.py", color=discord.Color.green()
                    )
                )
    else:
        cogl = cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Unloaded {i}.py", color=discord.Color.green()
                    )
                )


@cog.command(aliases=["l"], name="load", help="Load cogs")
@is_owner()
async def load(ctx, *, cogss: str = None):
    if not cogss:
        for i in cogs:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Loaded {i}.py", color=discord.Color.green()
                    )
                )
    else:
        cogl = cogss.split(", ")
        for i in cogl:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Loaded {i}.py", color=discord.Color.green()
                    )
                )


@cog.command(aliases=["rl"], name="reload", help="Reload cogs")
@is_owner()
async def reload(ctx, *, cogss: str = None):
    if not cogss:
        for i in loaded_cogs:
            bot.reload_extension(f"cogs.{i}")
            await ctx.send(
                embed=discord.Embed(
                    description=f"Reloaded {i}.py", color=discord.Color.green()
                )
            )
    else:
        cogl = cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.reload_extension(f"cogs.{i}")
                await ctx.send(
                    embed=discord.Embed(
                        description=f"Reloaded {i}.py", color=discord.Color.green()
                    )
                )


@bot.command(name="uptime", help="Show's bot uptime.", aliases=["ut"])
async def uptime(ctx):
    await ctx.reply(
        embed=discord.Embed(
            description="Bot is online since: <t:{0}:F>".format(bot.starttime),
            color=discord.Color.green(),
        )
    )


def get_token():
    token = os.environ.get("TOKEN")
    if not token:
        logger.critical("TOKEN environment variable not set, using default token")
        token = "OTc3NTgwMDUyMDgwMzc3OTc2.GGpKAs.fL4BL1JBzkD6Y1R_xepCV4miHTgc0JHByxMla4"
    return token


bot.run(get_token())
