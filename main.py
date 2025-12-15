import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Connecté en tant que {bot.user}")

async def setup():
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.logs")
    await bot.load_extension("cogs.welcome")
    await bot.start(TOKEN)

import asyncio
asyncio.run(setup())
