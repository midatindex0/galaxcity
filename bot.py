from datetime import datetime
import discord
from discord.ext import commands
import time

cogs=[]
loaded_cogs=[]
bot=commands.Bot(command_prefix="g!",intents=discord.Intents.all(),status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching,name="my development."))
bot.starttime=int(time.time())
for i in cogs:
    bot.load_extension(f"cogs.{i}")
    loaded_cogs.append(i)

@bot.event
async def on_ready():
    print("Logged in as: {0}".format(bot.user.name))
    for i in loaded_cogs:print(f"{i}.py is Loaded!")

@bot.command(name="ping",help="Return's Bot Latency.")
async def ping(ctx):
    await ctx.reply("Pong!")

@bot.group(name="cog",help="Cog Based Commands")
@commands.is_owner()
async def cog(ctx):
    await ctx.reply(embed=discord.Embed(color=discord.Color.green()))

@cog.command(aliases=["l"])
@commands.is_owner()
async def load(ctx,cogss:str=None):
    if not cogl:
        for i in cogss:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(embed=discord.Embed(description=f"Loaded {i}.py",color=discord.Color.green()))
    cogl=cogss.split(", ")
    for i in cogl:
        if i not in loaded_cogs:
            bot.load_extension(f"cogs.{i}")
            loaded_cogs.append(i)
            await ctx.send(embed=discord.Embed(description=f"Loaded {i}.py",color=discord.Color.green()))

@bot.command(name="uptime",help="Show's bot uptime.",aliases=["ut"])
async def uptime(ctx):
    await ctx.reply(embed=discord.Embed(description="Bot is online since: <t:{0}:F>".format(bot.starttime),color=discord.Color.green()))

bot.run("ODcwNTAxNDM0NTExMjI0ODcy.GsTPXh.xg68VhrMlFkA1gDlHkD7zAEgCve1iVmIMR0-Dw") # temp token of bot "The Dev Bot"