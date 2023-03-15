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
class Profile(commands.Cog, name="Profile"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    

    @commands.hybrid_command(
        name="profile",
        description="Check profile user",
    )
    # This will only allow non-blacklisted members to execute the command
    # This will only allow owners of the bot to execute the command -> config.json
    @app_commands.describe(user="Put the giftcard to check")
    @helper.is_owner()
    async def testcommand(self, context: Context, user: str):
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.yml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/user_info/"+user)
        data = response.json()
        color="0x"+config['color_embeds']
        color_embed = int(color,16)
        avatar="https://api.mineatar.io/face/"+user
        if data['amount_spent'] == 0 and len(data['recent_purchases']) > 0:
            embed = discord.Embed(
                    title="Profile LookUp", description="`"+user+"` spend in the Store: `"+str(data['amount_spent'])+"`\nBut have purchases with `GiftCards`", color=color_embed)
            for i in range(len(data['recent_purchases'])):
                
                purchase = data['recent_purchases'][i]
                r=("**Name**: `{}` \n **Price**: `{}`".format(purchase['name'], purchase['price']))
                if len(data['recent_purchases']) == 1:
                    embed.add_field(name="1 Most Recent", value=r)
                if i < 5:
                    number=i+1
                    embed.add_field(name=str(number)+" Most Recent", value=r, inline=True)   
            embed.set_thumbnail(url=avatar)
            await context.send(embed=embed)
            return
        elif data['amount_spent'] > 0 and len(data['recent_purchases']) > 0:
            embed = discord.Embed(
                    title="Profile LookUp", description="`"+user+"` spend in the Store: `"+str(data['amount_spent'])+"`", color=color_embed)
            for i in range(len(data['recent_purchases'])):                
                purchase = data['recent_purchases'][i]
                r=("**Name**: `{}` \n **Price**: `{}`".format(purchase['name'], purchase['price']))
                if len(data['recent_purchases']) == 1:
                    embed.add_field(name="1 Most Recent", value=r)
                if i < 5:
                    number=i+1
                    embed.add_field(name=str(number)+" Most Recent", value=r, inline=True)
                if i == 4:
                    embed.set_thumbnail(url=avatar)
                    await context.send(embed=embed)
                    return
        
        if data['amount_spent'] == 0 and len(data['recent_purchases']) == 0 :
            embed = discord.Embed(
                title="Profile LookUp", description="`This user has no registered purchase`", color=color_embed)
            embed.set_thumbnail(url=avatar)
            await context.send(embed=embed)
            return

            
            embed.set_thumbnail(url=avatar)
            await context.send(embed=embed)


      
        pass


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Profile(bot))
