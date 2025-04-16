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

@tree.command(name="ping", description="Test the bot's responsiveness.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="error", description="Trigger an error for testing webhook logging.")
async def error(interaction: discord.Interaction):
    try:
        raise ValueError("Test error for webhook logging!")
    except Exception as e:
        await interaction.response.send_message("Triggered error for webhook test.")
        await error_handler.handle_error(e)

@tree.command(name="uptime", description="Show how long BooBot has been running.")
async def uptime(interaction: discord.Interaction):
    now = datetime.utcnow()
    uptime = now - start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)
    await interaction.response.send_message(
        f"BooBot has been running for `{hours}` hours, `{minutes}` minutes."
    )

@tree.command(name="clear", description="Clear messages in the current channel.")
@discord.app_commands.describe(amount="Number of messages to delete", full="Wipe full history (up to 1000)")
async def clear(interaction: discord.Interaction, amount: int = 10, full: bool = False):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("Permission denied.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    try:
        limit = 1000 if full else amount
        deleted = await interaction.channel.purge(limit=limit)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send("Failed to delete messages.", ephemeral=True)
        await error_handler.handle_error(e)

@tree.command(name="alert_add", description="Add a keyword to track.")
async def alert_add(interaction: discord.Interaction, keyword: str):
    if alert_manager.add_keyword(keyword):
        await interaction.response.send_message(f"Tracking keyword: `{keyword}`")
    else:
        await interaction.response.send_message("Keyword already tracked or invalid.")

@tree.command(name="alert_list", description="List tracked keywords.")
async def alert_list(interaction: discord.Interaction):
    keywords = alert_manager.list_keywords()
    if not keywords:
        await interaction.response.send_message("No tracked keywords.")
    else:
        await interaction.response.send_message("Tracked keywords:\n" + "\n".join(f"- `{kw}`" for kw in keywords))

@tree.command(name="alert_test", description="Simulate a match for test purposes.")
async def alert_test(interaction: discord.Interaction, message: str):
    matches = alert_manager.keyword_match(message)
    if matches:
        for kw in matches:
            alert_manager.log_alert(kw, message)
        await interaction.response.send_message(f"Match found: {', '.join(matches)} — alert logged.")
    else:
        await interaction.response.send_message("No keywords matched.")

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')
    try:
        await bot.tree.sync(guild=None)
        guild = discord.Object(id=1360727779385016371)
        await bot.tree.sync(guild=guild)
        print("Slash commands synced to guild.")
    except Exception as e:
        print(f"Slash sync failed: {e}")

@bot.event
async def on_connect():
    guild = discord.Object(id=1360727779385016371)
    bot.loop.create_task(bot.tree.sync(guild=guild))
    print("Forced sync on connect.")

@bot.event
async def on_command_error(ctx, error):
    await error_handler.handle_error(error)

@bot.event
async def setup_hook():
    bot.loop.create_task(bot_monitor.BotMonitor(bot, monitored_ids, log_channel_id).start_monitoring())
    uptime_logger.UptimeLogger(bot, log_channel_id).start()

try:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN not found in .env")
    bot.run(token)
except Exception as e:
    import asyncio
    asyncio.run(error_handler.handle_error(e))
