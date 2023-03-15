import asyncio
import os
import platform
import random
import sys
import string

import time

from colorama import Fore

import yaml

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

import requests

import exceptions




if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.yml"):
    sys.exit("'config.yml' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.yml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)



if config['minestore_url'] == "store.example.com":    
    for i in range(10):
        print(Fore.LIGHTRED_EX+"THE BOT WILL NOT WORK CORRECTLY IF YOU DO NOT PUT THE URL OF YOUR STORE IN TE CONFIG.YML!")
    print(Fore.WHITE+"STOPING BOT NOW!")
    exit()


intents = discord.Intents.default()




bot = Bot(command_prefix=commands.when_mentioned_or(
    "!"), intents=intents, help_command=None)




bot.config = config


@bot.event
async def on_ready() -> None:
    # ANTI MULTI BOT FOR SEGURITY
    if len(bot.guilds) >= 3:
        print(Fore.LIGHTRED_EX+"The bot only can active in 2 servers :(")
        print(Fore.LIGHTRED_EX+"The bot only can active in 2 servers :(")
        print(Fore.LIGHTRED_EX+"The bot only can active in 2 servers :(")
        print(Fore.LIGHTRED_EX+"The bot only can active in 2 servers :(")
        print(Fore.WHITE+"Shutdown bot in 5 seconds...")
        time.sleep(5)
        await bot.close()
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print(f"Active in: {len(bot.guilds)} Servers")
    print("-------------------")
    status_task.start()
    if config['channel_donation'] == True:
        channel_goal.start()    
        

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    statuses = config['status_bot']
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

@tasks.loop(seconds=float(config['update_time']))
async def channel_goal() -> None:
    response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/donation_goal")
    data = response.json()
    goal = "{}/{}".format(data['goal_sum'], data['goal'])
    channel = bot.get_channel(int(config['channel_id']))
    if channel != None:
        await channel.edit(name=config['donation_name']+" "+goal)
    else:
        print("Channel to Goal not exist!")


@bot.event
async def on_message(message: discord.Message) -> None:
    
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_completion(context: Context) -> None:
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
    else:
        print(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")







@bot.event
async def on_command_error(context: Context, error) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserNotOwner):
        embed = discord.Embed(
            title="Error!",
            description="You are not have permissions for this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="I am missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to fully perform this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)

    
    raise error


async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/commands"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"commands.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


asyncio.run(load_cogs())
bot.run(config['token_bot'])
