# slash_sync_test.py
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1360727779385016371

class TestClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        guild = discord.Object(id=GUILD_ID)
        try:
            self.tree.clear_commands(guild=guild)
            await self.tree.sync(guild=guild)
            print("? Slash commands synced manually to guild.")
        except Exception as e:
            print(f"? Sync failed: {e}")
        await self.close()

client = TestClient()
client.run(TOKEN)
