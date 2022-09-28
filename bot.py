from dis import dis, disco
import imp
import json
import os
from datetime import datetime
from pydoc import cli
from dotenv import load_dotenv
import discord
from discord import app_commands

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

def get_file_data():
    with open('loc.json', 'r') as f:
        data = json.load(f)
    return data

def write_file_data(data):
    with open('loc.json', 'w') as f:
        json.dump(data, f)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print('--------------')


@client.tree.command()
async def storeloc(interaction: discord.Interaction, coordinates: str):
    uid = str(interaction.user.id)

    time = datetime.now().timestamp()
    current_loc = {"time": time,
    "coordinates" : coordinates.replace(" ", "")
    }

    data = get_file_data()
    if uid in data:
        data[uid].append(current_loc)
    else :
        data[uid] = [current_loc]
    write_file_data(data)

    await interaction.response.send_message(f"Location stored successfully : {coordinates} ")

def get_map_url(locations):
    SEARCH_URL = "https://www.google.com/maps/search/?api=1&query="
    DIRECTIONS_URL = " https://www.google.com/maps/dir/?api=1&"
    if len(locations) == 1:
        return f"{SEARCH_URL}{locations[0]['coordinates']}"

    if len(locations) == 2:
        return f"{DIRECTIONS_URL}origin={locations[0]['coordinates']}&destination={locations[1]['coordinates']}"

    if len(locations) > 2:
        origin = locations[0]['coordinates']
        destination = locations[-1]['coordinates']
        waypoints = []
        for location in locations[1:-1]:
            waypoints.append(location['coordinates'])
        waypoints_url = "|".join(waypoints)
        print(waypoints)
        return f"{DIRECTIONS_URL}origin={origin}&destination={destination}&waypoints={waypoints_url}"



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