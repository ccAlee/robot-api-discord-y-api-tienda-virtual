import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord import app_commands
import os
import yaml


from helpers import helper


# Here we name the cog and create a new class for the cog.
class CheckGiftCard(commands.Cog, name="CheckGiftCard"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="checkgiftcard",
        description="Check value of any GiftCard",
    )
    # This will only allow owners of the bot to execute the command -> config.json
    @app_commands.describe(giftcard="Put the giftcard to check")
    @helper.is_owner()
    async def testcommand(self, context: Context, giftcard: str):
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.yml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/validGiftCard?code="+giftcard)
        data = response.json()
        color="0x"+config['color_embeds']
        color_embed = int(color,16)
        if len(data) == 0:
            embed = discord.Embed(
                title="GiftCard Check", description="`The giftcard does not exist`", color=color_embed)
            await context.send(embed=embed)
        else:
    # Si el valor es una cadena, añade ** al principio y al final y conviértelo a mayúsculas

            gift = "**Code**: `{}`\n**Balance**: `{}`".format(data['code'], data['amount'])

            embed = discord.Embed(
                title="GiftCard Check", description="Info of `GiftCard`\n"+gift, color=color_embed)
            await context.send(embed=embed)


      
        pass


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(CheckGiftCard(bot))
