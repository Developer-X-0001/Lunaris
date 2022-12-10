import pycountry
import requests
import discord
import config
from discord.ext import commands
from discord import app_commands

class AirQuality(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="air-quality", description="get up to date air quality information.")
    @app_commands.describe(location="Type the city name", hidden="Choose wether to show information publicly or privately.")
    @app_commands.choices(
        hidden=[
            app_commands.Choice(name="True", value=1),
            app_commands.Choice(name="False", value=0)
        ]
    )
    async def aqi(self, interaction: discord.Interaction, location: str, hidden: app_commands.Choice[int]):
        request_url = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config.WEATHER_API_KEY}&q={location}&aqi=yes")
        response = request_url.json()
        
        location = response["location"]
        weather = response["current"]

        # ---------- Location Data ----------
        city = location["name"]
        region = location["region"]
        country = location["country"]
        if country == "United States of America":
            country = "United States"
        get_country = pycountry.countries.get(name=country)

        # ---------- Co-Ordinates Data ----------
        latitude = str(round(location["lat"], ndigits=2)) + "º"
        longitude = str(round(location["lon"], ndigits=2)) + "º"

        # ---------- Time Data ----------
        timezone = location["tz_id"]
        localtime = location["localtime"]

        # ---------- Air Quality Data ----------
        airQuality = response["current"]["air_quality"]
        co = round(airQuality["co"], ndigits=2)
        no2 = round(airQuality["no2"], ndigits=2)
        o3 = round(airQuality["o3"], ndigits=2)
        so2 = round(airQuality["so2"], ndigits=2)
        pm2_5 = round(airQuality["pm2_5"], ndigits=2)
        pm10 = round(airQuality["pm10"], ndigits=2)
        index = round(airQuality["us-epa-index"], ndigits=2)
        if index == 1:
            quality = "Good"
        if index == 2:
            quality = "Moderate"
        if index == 3:
            quality = "Unhealthy for sensitive groups"
        if index == 4:
            quality = "Unhealthy"
        if index == 5:
            quality = "Very Unhealthy"
        if index == 6:
            quality = "Hazardous"

        day = "<:day:1050879646469734470> Day"
        if weather["is_day"] == 0:
            day = "<:night:1050879649208598639> Night"

        aqi_embed = discord.Embed(
            title=f"{city}, {country}",
            url=f"https://en.wikipedia.org/wiki/{city.replace(' ', '_')}",
            description=f"Showing weather of {city} {region}, {country}.\nIt's currently {day} time there.",
            color=discord.Color.blurple()
        )
        aqi_embed.add_field(
            name="<:city:1050876004597510224> **__City Information:__**",
            value=f"Name: {city}\nRegion: {region}\nCountry: {country} :flag_{str(get_country.alpha_2).lower()}:\nLocation: {latitude} Latitude, {longitude} Longitude\nTimezone: {timezone}\nLocal Time: {localtime}",
            inline=False
        )
        aqi_embed.add_field(
            name="<:airquality:1051152810785378314> **__Air Quality Information:__**",
            value=f"Carbon Monoxide: {co}µg/m³\nNitrogen Dioxide: {no2}µg/m³\nOzone: {o3}µg/m³\nSulphur Dioxide: {so2}µg/m³\nPM 2.5: {pm2_5}µg/m³\nPM 10: {pm10}µg/m³\n\nAir Quality Index: {index}\nOverall Air Quality: {quality}",
            inline=False
        )
        aqi_embed.set_thumbnail(url=f"https://countryflagsapi.com/png/{get_country.alpha_2}")

        if hidden.value == 1:
            await interaction.response.send_message(embed=aqi_embed, ephemeral=True)
        if hidden.value == 0:
            await interaction.response.send_message(embed=aqi_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        AirQuality(bot))