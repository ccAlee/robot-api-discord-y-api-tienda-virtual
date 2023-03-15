import random
import string
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
import yaml


from helpers import helper

from discord.ext.commands import Bot, Context
import requests


        
with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.yml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

intents = discord.Intents.default()

bot = discord.Client(intents=intents)


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label=config['balance_1']+" $", custom_id= "button-1", style=discord.ButtonStyle.blurple)
    async def button_1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "balance_1"
        self.stop()

    @discord.ui.button(label=config['balance_2']+" $", custom_id= "button-2", style=discord.ButtonStyle.blurple)
    async def button_2(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "balance_2"
        self.stop()

    @discord.ui.button(label=config['balance_3']+" $", custom_id= "button-3", style=discord.ButtonStyle.blurple )
    async def button_3(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "balance_3"
        self.stop()

    @discord.ui.button(label=config['balance_4']+" $", custom_id= "button-4", style=discord.ButtonStyle.blurple)
    async def button_4(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "balance_4"
        self.stop()

    @discord.ui.button(label=config['balance_5']+" $", custom_id= "button-5", style=discord.ButtonStyle.red)
    async def button_5(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "balance_5"
        self.stop()








class GiftCardConfig(discord.ui.Select):
    
    def __init__(self):
        
        options = [
            discord.SelectOption(
                label="Template", description="Use your template of config and generate the giftcard fast!", emoji="🐇"
            ),
            discord.SelectOption(
                label="Generate", description="Generate a giftcard here custom!", emoji="🐿️"
            )
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )


    async def callback(self, interaction: discord.Interaction):
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.yml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        color="0x"+config['color_embeds']
        color_embed = int(color,16)
        choices = {
            "template": 0,
            "generate": 1,
        }

        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]


        result_embed = discord.Embed(color=color_embed)

        if user_choice_index == 0:
            code=config['code']
            balance=config['balance']
            response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/createGiftCard?code="+code+"&balance="+balance)
            code_https=response.status_code
            data= response.json()
            if code_https == 200:
                if data['status'] == True:
                    result_embed.description = "`The giftcard was generated using the config template!`\n\n**GiftCard**: "+code+"\n**Balance**: "+balance
                    result_embed.colour = color_embed
                    result_embed.title = "GiftCard Create!"
                    await interaction.response.edit_message(embed=result_embed, content=None, view=None)
                    return
                if data['status'] == False:
                    result_embed.description = "`The GiftCard already exists!`"
                    result_embed.colour = color_embed
                    result_embed.title = "ERROR!"
                    await interaction.response.edit_message(embed=result_embed, content=None, view=None)
            else:
                result_embed.description = "`The API dont get a good response, check your store or the API`"
                result_embed.colour = color_embed
                await interaction.response.edit_message(embed=result_embed, content=None, view=None)
                return
        if user_choice_index == 1:
            buttons = Choice()
            embed_custom = discord.Embed(
                title="GiftCard Generate",
                description=f"Please choose the balance to your `GiftCard`",
                color=color_embed)


            await interaction.response.edit_message(embed=embed_custom, view=buttons)
            
            await buttons.wait()
            num_codes = 1
            num_blocks = 4
            block_size = 4
            if buttons.value == "balance_1":
                balance = config['balance_1']
                for _ in range(num_codes):
                    characters = [random.choice(string.ascii_uppercase + string.digits) for _ in range(num_blocks * block_size)]
                    blocks = [characters[i:i + block_size] for i in range(0, len(characters), block_size)]
                    code = "-".join([''.join(block) for block in blocks])
                response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/createGiftCard?code="+code+"&balance="+balance)
                if response.status_code == 200:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"Has been create the `GiftCard`! \n\n**Code**: `{code}`\n**Balance**: `{config['balance_1']} $`",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)
                else:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"ERROR!\nYou a error with your API!",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)
            if buttons.value == "balance_2":
                balance = config['balance_2']
                for _ in range(num_codes):
                    characters = [random.choice(string.ascii_uppercase + string.digits) for _ in range(num_blocks * block_size)]
                    blocks = [characters[i:i + block_size] for i in range(0, len(characters), block_size)]
                    code = "-".join([''.join(block) for block in blocks])
                response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/createGiftCard?code="+code+"&balance="+balance)
                if response.status_code == 200:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"Has been create the `GiftCard`! \n\n**Code**: `{code}`\n**Balance**: `{config['balance_2']} $`",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)
                else:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"ERROR!\nYou a error with your API!",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)

            if buttons.value == "balance_3":
                balance = config['balance_3']
                for _ in range(num_codes):
                    characters = [random.choice(string.ascii_uppercase + string.digits) for _ in range(num_blocks * block_size)]
                    blocks = [characters[i:i + block_size] for i in range(0, len(characters), block_size)]
                    code = "-".join([''.join(block) for block in blocks])
                response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/createGiftCard?code="+code+"&balance="+balance)
                if response.status_code == 200:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"Has been create the `GiftCard`! \n\n**Code**: `{code}`\n**Balance**: `{config['balance_3']} $`",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)
                else:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"ERROR!\nYou a error with your API!",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)

            if buttons.value == "balance_4":
                balance = config['balance_4']
                for _ in range(num_codes):
                    characters = [random.choice(string.ascii_uppercase + string.digits) for _ in range(num_blocks * block_size)]
                    blocks = [characters[i:i + block_size] for i in range(0, len(characters), block_size)]
                    code = "-".join([''.join(block) for block in blocks])
                response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/createGiftCard?code="+code+"&balance="+balance)
                if response.status_code == 200:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"Has been create the `GiftCard`! \n\n**Code**: `{code}`\n**Balance**: `{config['balance_4']} $`",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)
                else:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"ERROR!\nYou a error with your API!",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)
            
            if buttons.value == "balance_5":
                balance = config['balance_5']
                for _ in range(num_codes):
                    characters = [random.choice(string.ascii_uppercase + string.digits) for _ in range(num_blocks * block_size)]
                    blocks = [characters[i:i + block_size] for i in range(0, len(characters), block_size)]
                    code = "-".join([''.join(block) for block in blocks])
                response = requests.get("https://"+config['minestore_url']+"/api/"+config['minestore_api']+"/createGiftCard?code="+code+"&balance="+balance)
                if response.status_code == 200:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"Has been create the `GiftCard`! \n\n**Code**: `{code}`\n**Balance**: `{config['balance_5']} $`",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)

                    

                    
                else:
                    embed_custom = discord.Embed(
                    title="GiftCard Generate",
                    description=f"ERROR!\nYou a error with your API!",
                    color=color_embed)

                    await interaction.message.edit(embed=embed_custom, view=None, content=None)
                
                
        #await interaction.response.edit_message(embed=result_embed, content=None, view=None)


class GiftCardClass(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GiftCardConfig())






class Generate(commands.Cog, name="gc"):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.hybrid_command(
        name="generategiftcard",
        description="Generate a GifCard!"
    )
    async def cg(self, context: Context) -> None:
        
        view = GiftCardClass()
        embed1= discord.Embed(
                title="GiftCard Generate",
                description=f"Please choose how you want to generate the `GiftCard`",
                color=0xE02B2B)
        await context.send(embed=embed1, view=view)

        
        


async def setup(bot):
    await bot.add_cog(Generate(bot))
