import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import yaml

from helpers import helper


# Here we name the cog and create a new class for the cog.
class RecentDonator(commands.Cog, name="RecentDonator"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="recentdonator",
        description="Get the most recent donator",
    )
    # This will only allow non-blacklisted members to execute the command
    # This will only allow owners of the bot to execute the command -> config.json
    @helper.is_owner()
    async def testcommand(self, context: Context):
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.yml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/getMostRecent")
        data = response.json()
        color="0x"+config['color_embeds']
        color_embed = int(color,16)


        recent = "**Name**: `{}`\n**Amount**: `{}`\n**Date**: `{}`\n**Package**: `{}`\n**Discountused**: `{}`".format(data['user'], data['amount'], data['date'], data['package'], data['discountused'])

        embed = discord.Embed(
            title="Recent Donation", description=recent, color=color_embed)
        await context.send(embed=embed)

      
        pass


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(RecentDonator(bot))
