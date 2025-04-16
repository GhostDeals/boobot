# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 1360727779385016371

        self.channel_map = {
            "ebay": 1360728090753630360,
            "amazon": 1360728117878198424,
            "ebuyer": 1361996933391978596,
            "scan": 1361996959405051974,
            "currys": 1361997021682335835,
            "overclockers": 1361997082977767473,
            "other": 1361997115273773139
        }

    async def fetch_deals(self, query):
        # Placeholder for real scraping logic
        return [
            {"site": "amazon", "title": f"{query} (Amazon)", "price": 39.99, "url": "https://amazon.example.com"},
            {"site": "ebuyer", "title": f"{query} (Ebuyer)", "price": 35.50, "url": "https://ebuyer.example.com"},
            {"site": "ebay", "title": f"{query} (eBay)", "price": 36.25, "url": "https://ebay.example.com"},
        ]

    @app_commands.command(name="snipe", description="Search multiple retailers for the best deal.")
    @app_commands.describe(query="Item to search for", price="Optional max price filter")
    async def snipe(self, interaction: discord.Interaction, query: str, price: float = None):
        await interaction.response.defer()

        deals = await self.fetch_deals(query)

        if price:
            deals = [deal for deal in deals if deal["price"] <= price]

        if not deals:
            await interaction.followup.send("No deals found in your price range.")
            return

        best_deal = sorted(deals, key=lambda x: x["price"])[0]
        channel_id = self.channel_map.get(best_deal["site"], self.channel_map["other"])
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            await interaction.followup.send("Could not find the target channel to post the deal.")
            return

        embed = discord.Embed(title=f"?? Deal Found [{best_deal['site'].capitalize()}]", color=discord.Color.green())
        embed.add_field(name="Item", value=best_deal['title'], inline=False)
        embed.add_field(name="Price", value=f"\u00a3{best_deal['price']:.2f}", inline=True)
        embed.add_field(name="Link", value=best_deal["url"], inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")

        await channel.send(embed=embed)
        await interaction.followup.send(f"Posted best deal to <#{channel_id}>")

async def setup(bot):
    await bot.add_cog(Snipe(bot))
    guild = discord.Object(id=1360727779385016371)
    await bot.tree.sync(guild=guild)
    print("? /snipe command registered to guild.")
