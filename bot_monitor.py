# ?? bot_monitor.py
import discord
import asyncio
from datetime import datetime

class BotMonitor:
    def __init__(self, bot, monitored_ids, log_channel_id):
        self.bot = bot
        self.monitored_ids = monitored_ids  # List of bot user IDs
        self.log_channel_id = log_channel_id
        self.previous_status = {}

    async def start_monitoring(self):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(self.log_channel_id)
        if not log_channel:
            print("[BotMonitor] Log channel not found.")
            return

        while not self.bot.is_closed():
            for bot_id in self.monitored_ids:
                user = self.bot.get_user(bot_id)
                if not user:
                    continue

                is_online = any(
                    member.status != discord.Status.offline
                    for member in self.bot.guilds[0].members
                    if member.id == bot_id
                )

                # Check for status change
                last_known = self.previous_status.get(bot_id)
                if last_known != is_online:
                    self.previous_status[bot_id] = is_online
                    status = "?? Online" if is_online else "?? Offline"
                    embed = discord.Embed(
                        title=f"Bot Status Changed",
                        description=f"<@{bot_id}> is now **{status}**",
                        color=0x00ff00 if is_online else 0xff0000,
                        timestamp=datetime.utcnow()
                    )
                    await log_channel.send(embed=embed)
            await asyncio.sleep(60)  # Check every 60 seconds
