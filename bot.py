import imp
import json
import os
from datetime import datetime
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

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print('--------------')


@client.tree.command()
async def storeloc(interaction: discord.Interaction, lon: str, lat: str):
    uid = str(interaction.user.id)

    time = datetime.now().timestamp()
    current_loc = {"time": time,
    "lon": lon,
    "lat": lat
    }

    with open('loc.json', 'r') as f:

        data = json.load(f)

    print(data)
    if uid in data:
        print("WHAT")
        data[uid].append(current_loc)
    else :
        data[uid] = [current_loc]

    print(data)
    with open('loc.json', 'w') as f:
        json.dump(data, f)

    await interaction.response.send_message(f"Location stored successfully : {lon} ; {lat} ")

client.run(TOKEN)