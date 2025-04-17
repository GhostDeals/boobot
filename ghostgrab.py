# -*- coding: utf-8 -*-
import discord
from discord import app_commands
from discord.ext import commands
from playwright.async_api import async_playwright

MOCK_RRP = {
    "controller": 59.99,
    "headset": 79.99,
    "monitor": 199.99,
    "ssd": 99.99,
}

WATCHED_KEYWORDS = ["controller", "ssd", "headset", "monitor"]

def calculate_booboost(deal):
    score = 50
    query = deal["title"].lower()

    if any(kw in query for kw in WATCHED_KEYWORDS):
        score += 10

    rrp = MOCK_RRP.get(deal["query"].lower(), deal["price"] + 10)
    undercut = max(0, (rrp - deal["price"]) / rrp)
    score += int(undercut * 30)

    if "bundle" in query or "pack" in query:
        score += 5

    if "only" in query and "left" in query:
        score += 5

    return min(score, 100)

class GhostGrab(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def fetch_deals(self, query):
        deals = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(f"https://www.amazon.co.uk/s?k={query.replace(' ', '+')}")
            await page.wait_for_timeout(3000)

            items = await page.query_selector_all('div[data-component-type="s-search-result"]')
            for item in items[:5]:
                title = await item.query_selector_eval("h2 a span", "el => el.innerText") if await item.query_selector("h2 a span") else "No title"
                url = await item.query_selector_eval("h2 a", "el => el.href") if await item.query_selector("h2 a") else "No URL"
                price_whole = await item.query_selector_eval(".a-price .a-price-whole", "el => el.innerText") if await item.query_selector(".a-price .a-price-whole") else None
                price_frac = await item.query_selector_eval(".a-price .a-price-fraction", "el => el.innerText") if await item.query_selector(".a-price .a-price-fraction") else "00"

                if price_whole:
                    price_str = price_whole.replace(",", "") + "." + price_frac
                    try:
                        price = float(price_str)
                    except:
                        continue
                    deals.append({
                        "site": "amazon",
                        "title": title,
                        "price": price,
                        "url": url,
                        "query": query
                    })

            await browser.close()
        return deals

    @app_commands.command(name="ghostgrab", description="Search Amazon for the best deal and post it with BooBoost score.")
    @app_commands.describe(query="What are you looking for?", price="Max price (optional)")
    async def ghostgrab(self, interaction: discord.Interaction, query: str, price: float = None):
        await interaction.response.defer()

        try:
            deals = await self.fetch_deals(query)
            if price is not None:
                deals = [d for d in deals if d["price"] <= price]

            if not deals:
                await interaction.followup.send("? No deals found.")
                return

            for deal in deals:
                deal["score"] = calculate_booboost(deal)

            best = sorted(deals, key=lambda x: -x["score"])[0]

            embed = discord.Embed(
                title=f"?? GhostGrab Deal [{best['site'].capitalize()}]",
                color=discord.Color.green()
            )
            embed.add_field(name="Item", value=best["title"], inline=False)
            embed.add_field(name="Price", value=f"\u00A3{best['price']:.2f}", inline=True)
            embed.add_field(name="BooBoost™", value=f"{best['score']} / 100", inline=True)
            embed.add_field(name="Link", value=best["url"], inline=False)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}")

            amazon_channel_id = 1360728117878198424
            channel = interaction.guild.get_channel(amazon_channel_id)

            await channel.send(embed=embed)
            await interaction.followup.send(f"? Posted deal to <#{amazon_channel_id}>")

        except Exception as e:
            print(f"[ERROR] /ghostgrab failed: {e}")
            await interaction.followup.send("?? Something went wrong.")

async def setup(bot: commands.Bot):
    await bot.add_cog(GhostGrab(bot))
