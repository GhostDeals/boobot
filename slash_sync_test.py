import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"? Logged in as {bot.user.name}")
    
    # Load GhostGrab Cog
    try:
        await bot.load_extension("ghostgrab")
        print("?? ghostgrab.py loaded successfully.")
    except Exception as e:
        print(f"? Failed to load ghostgrab: {e}")

    # Sync Slash Commands
    guild = discord.Object(id=1360727779385016371)
    synced = await tree.sync(guild=guild)
    print(f"? Synced {len(synced)} slash commands to guild.")

    # Print all synced command names
    for cmd in synced:
        print(f"?? Registered: /{cmd.name}")

    await bot.close()

bot.run(os.getenv("DISCORD_TOKEN"))
