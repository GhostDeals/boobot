# uptime_logger.py
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord

class UptimeLogger:
    def __init__(self, bot, log_channel_id):
        self.bot = bot
        self.log_channel_id = log_channel_id
        self.start_time = datetime.utcnow()
        self.scheduler = AsyncIOScheduler()

    def start(self):
        # ? Now runs every 6 hours
        self.scheduler.add_job(self.send_uptime_report, 'interval', hours=6)
        self.scheduler.start()

    async def send_uptime_report(self):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if not log_channel:
            print("[UptimeLogger] Log channel not found.")
            return

        uptime = datetime.utcnow() - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)

        embed = discord.Embed(
            title="?? BooBot Uptime Report",
            description=f"I've been running for: `{hours} hours, {minutes} minutes`",
            color=0x2ecc71,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Time shown is UTC")

        await log_channel.send(embed=embed)
