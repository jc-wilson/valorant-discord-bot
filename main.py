import os
import discord
import asyncio
import random
import json
import requests
import valo_api
import inspect
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from valo_api import set_api_key
from valo_api.endpoints import get_mmr_details_by_name_v2_async
from valo_api.endpoints import get_account_details_by_name_v2_async

with open("valorant.json") as f:
    agents_data = json.load(f)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))
VAL_API_KEY = os.getenv("VAL_API_KEY")
valo_api.set_api_key(VAL_API_KEY)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def random_agent_func():
    global random
    r_num = random.randrange(0, 28)
    r_agent = agents_data[r_num]["Agent"]
    return r_agent

@bot.tree.command(name="random_agent", description="Gives a random agent")
async def random_agent(interaction: discord.Interaction):
    await interaction.response.send_message(f"Your random agent is {random_agent_func()}!")

@bot.tree.command(name="rank_checker", description="show rank of chosen player")
@app_commands.describe(riot_id="input Riot ID")
async def valo_rank(interaction: discord.Interaction, riot_id: str):
    hash_pos = riot_id.find("#")
    riot_name = riot_id[:hash_pos]
    riot_tag = riot_id[hash_pos + 1:]
    input_mmr = None
    input_mmr = await get_mmr_details_by_name_v2_async(version="v2", region="eu", name=f"{riot_name}", tag=f"{riot_tag}")
    if input_mmr:
        await interaction.response.send_message(f"{riot_id}'s rank is: {input_mmr.current_data.currenttierpatched}")

@bot.tree.command(name="level_checker", description="show level of chosen player")
@app_commands.describe(riot_id="input Riot ID")
async def valo_level(interaction: discord.Interaction, riot_id: str):
    hash_pos = riot_id.find("#")
    riot_name = riot_id[:hash_pos]
    riot_tag = riot_id[hash_pos + 1:]
    input_level = None
    input_level = await get_account_details_by_name_v2_async(version="v2", name=f"{riot_name}", tag=f"{riot_tag}", force_update="True")
    if input_level:
        await interaction.response.send_message(f"{riot_id}'s level is: {input_level.account_level}")


@bot.event
async def setup_hook():
    bot.tree.copy_global_to(guild=discord.Object(id=SERVER_ID))
    await bot.tree.sync(guild=discord.Object(id=SERVER_ID))

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    print("Syncing to:", SERVER_ID)
    print([cmd.name for cmd in await bot.tree.fetch_commands(guild=discord.Object(id=SERVER_ID))])



bot.run(TOKEN)



