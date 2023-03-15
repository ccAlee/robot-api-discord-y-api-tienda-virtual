import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import yaml

from helpers import helper


# Here we name the cog and create a new class for the cog.
class Coupons(commands.Cog, name="Coupons"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="coupons",
        description="Get the frist 5 coupons",
    )
    # This will only allow non-blacklisted members to execute the command
    # This will only allow owners of the bot to execute the command -> config.json
    @helper.is_owner()
    async def testcommand(self, context: Context):
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.yml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/couponList")
        data = response.json()
        color="0x"+config['color_embeds']
        color_embed = int(color,16)
        coupons_list=""
        if len(data) == 0:
            embed = discord.Embed(
                title="Coupons", description="`No coupons available`", color=color_embed)
            embed.set_thumbnail(url='https://i.imgur.com/eKfQTqn.png')
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            title="Coupons", description=coupons_list, color=color_embed)

        for element in data:
            i=0
            coupons_list = "**Coupon**: `{}`\n**Discount**: `{}%`".format(element['name'], element['discount'])
            if i < 5:
                embed.add_field(name="Info", value=coupons_list, inline=True)
            if i == len(data):
                break
        
        coupons_list="List of `Coupons`:\n"+coupons_list
        embed.set_thumbnail(url='https://i.imgur.com/eKfQTqn.png')
        await context.send(embed=embed)

      
        pass


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Coupons(bot))
