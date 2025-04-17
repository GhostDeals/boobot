# wipe_and_sync.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from ghostgrab import GhostGrab

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
GUILD_ID = 1360727779385016371

@bot.event
async def on_ready():
    print(f"? Logged in as {bot.user}")

    try:
        await bot.load_extension("ghostgrab")
        print("? ghostgrab.py loaded successfully.")
    except Exception as e:
        print(f"? Failed to load ghostgrab: {e}")
        return

    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"?? Wiped and synced {len(synced)} slash commands.")
        for cmd in synced:
            print(f"? Registered: /{cmd.name}")
    except Exception as e:
        print(f"? Slash sync failed: {e}")

    await bot.close()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN not found in .env file")
    bot.run(token)
