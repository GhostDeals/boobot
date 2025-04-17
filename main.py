# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import error_handler
import os
from dotenv import load_dotenv
import bot_monitor
import uptime_logger
from datetime import datetime
from alert_manager import AlertManager

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
start_time = datetime.utcnow()
log_channel_id = 1361626273041874974
monitored_ids = []
alert_manager = AlertManager()

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')

@bot.event
async def setup_hook():
    await bot.load_extension("ghostgrab")
    print("? ghostgrab.py cog loaded.")

    guild = discord.Object(id=1360727779385016371)
    await bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)
    print(f"? Synced {len(synced)} command(s) to guild.")
    for cmd in synced:
        print(f" - /{cmd.name}")

    bot.loop.create_task(bot_monitor.BotMonitor(bot, monitored_ids, log_channel_id).start_monitoring())
    uptime_logger.UptimeLogger(bot, log_channel_id).start()

@bot.event
async def on_command_error(ctx, error):
    await error_handler.handle_error(error)

try:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN not found in .env")
    bot.run(token)
except Exception as e:
    import asyncio
    asyncio.run(error_handler.handle_error(e))