import requests
import discord
import datetime
from discord import app_commands
from discord.ext import commands
import config

class Weather(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="weather", description="View weather of a location.")
    @app_commands.describe(location="Type the city name")
    @app_commands.choices(
        units=[
            app_commands.Choice(name="Imperial", value="imperial"),
            app_commands.Choice(name="Metric", value="metric")
        ]
    )
    async def weather(self, interaction: discord.Interaction, location: str, units: app_commands.Choice[str]):
        embed = discord.Embed(
            title="Rawalpindi Punjab, Pakistan",
        )
        embed.set_author(name="Rawalpindi")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Weather(bot))

#self.bot.application_info()