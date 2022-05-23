from datetime import datetime
import discord
from discord.ext import commands
import time

cogs=["story"]
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

@bot.group(name="cog",help="Cog Based Commands",invoke_without_command=True)
@commands.is_owner()
async def cog(ctx):
    await ctx.reply(embed=discord.Embed(color=discord.Color.green(),description=loaded_cogs))

@cog.command(aliases=["ul"],name="unload",help="Unload cogs")
@commands.is_owner()
async def unload(ctx,cogss:str=None):
    if not cogss:
        for i in cogs:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(embed=discord.Embed(description=f"Unloaded {i}.py",color=discord.Color.green()))
    else:
        cogl=cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(embed=discord.Embed(description=f"Unloaded {i}.py",color=discord.Color.green()))


@cog.command(aliases=["l"],name="load",help="Load cogs")
@commands.is_owner()
async def load(ctx,cogss:str=None):
    if not cogss:
        for i in cogs:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(embed=discord.Embed(description=f"Loaded {i}.py",color=discord.Color.green()))
    else:
        cogl=cogss.split(", ")
        for i in cogl:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(embed=discord.Embed(description=f"Loaded {i}.py",color=discord.Color.green()))

@cog.command(aliases=["rl","re"],name="reload",help="Reload cogs")
@commands.is_owner()
async def reload(ctx,cogss:str=None):
    if not cogss:
        for i in loaded_cogs:
            bot.reload_extension(f"cogs.{i}")
            await ctx.send(embed=discord.Embed(description=f"Reloaded {i}.py",color=discord.Color.green()))
    else:
        cogl=cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.reload_extension(f"cogs.{i}")
                await ctx.send(embed=discord.Embed(description=f"Reloaded {i}.py",color=discord.Color.green()))

@bot.command(name="uptime",help="Show's bot uptime.",aliases=["ut"])
async def uptime(ctx):
    await ctx.reply(embed=discord.Embed(description="Bot is online since: <t:{0}:F>".format(bot.starttime),color=discord.Color.green()))

bot.run("ODcwNTAxNDM0NTExMjI0ODcy.GsTPXh.xg68VhrMlFkA1gDlHkD7zAEgCve1iVmIMR0-Dw") # temp token of bot "The Dev Bot"