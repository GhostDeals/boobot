import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"?? Logged in as {bot.user.name}")
    guild = discord.Object(id=1360727779385016371)

    # Wipe all slash commands
    await bot.tree.clear_commands(guild=guild)
    print("?? Wiped existing slash commands from guild.")

    # Reload ghostgrab cog
    await bot.load_extension("ghostgrab")
    print("?? Reloaded ghostgrab.")

    # Sync new
    synced = await bot.tree.sync(guild=guild)
    print(f"? Resynced {len(synced)} commands.")
    for cmd in synced:
        print(f"?? /{cmd.name}")

    await bot.close()

bot.run(os.getenv("DISCORD_TOKEN"))
