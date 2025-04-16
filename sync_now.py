# sync_now.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1360727779385016371

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    commands_synced = await bot.tree.sync(guild=guild)
    print(f"? Synced {len(commands_synced)} slash commands to GUILD.")
    await bot.close()

bot.run(TOKEN)
