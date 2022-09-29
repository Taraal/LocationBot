import os
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord import app_commands
from modules.utils import *

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents) -> None:
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()


intents = discord.Intents.default()
client = Bot(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print('--------------')


@client.tree.command()
async def storeloc(interaction: discord.Interaction, coordinates: str):
    uid = str(interaction.user.id)

    time = datetime.now().timestamp()
    current_loc = {"time": time,
                   "coordinates": coordinates.replace(" ", "")
                   }

    data = get_file_data()
    if uid in data:
        data[uid].append(current_loc)
    else:
        data[uid] = [current_loc]
    write_file_data(data)

    await interaction.response.send_message(f"Location stored successfully : {coordinates} ")


@client.tree.command()
async def getloc(interaction: discord.Interaction, user: discord.Member):

    uid = str(user.id)

    data = get_file_data()

    try:
        locations = data[uid]
        if not locations:
            raise KeyError
        print(locations)
        url = get_map_url(locations)

        await interaction.response.send_message(url)
    except KeyError as e:
        await interaction.response.send_message(f'User {user.name} has not registered any location')


@client.tree.command()
async def purge(interaction: discord.Interaction):

    uid = str(interaction.user.id)

    data = get_file_data()

    if uid in data:
        data[uid] = []

    write_file_data(data)

    await interaction.response.send_message(f"Locations for user {interaction.user.name} successfully deleted")

client.run(TOKEN)
