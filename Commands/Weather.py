import requests
import discord
import pycountry
from discord import app_commands
from discord.ext import commands
import config

class Weather(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="weather", description="Get up to date current weather information.")
    @app_commands.describe(location="Type the city name", hidden="Choose wether to show information publicly or privately.")
    @app_commands.choices(
        units=[
            app_commands.Choice(name="Imperial", value="imperial"),
            app_commands.Choice(name="Metric", value="metric")
        ],
        hidden=[
            app_commands.Choice(name="True", value=1),
            app_commands.Choice(name="False", value=0)
        ]
    )
    async def weather(self, interaction: discord.Interaction, location: str, units: app_commands.Choice[str], hidden: app_commands.Choice[int]):
        request_url = requests.get(f"http://api.weatherapi.com/v1/current.json?key={config.WEATHER_API_KEY}&q={location}&aqi=no")
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

        # ---------- Weather Data ----------
        condition = weather["condition"]["text"]
        humidity = str(round(weather["humidity"])) + "%"
        windspeed = str(round(weather["wind_kph"])) + "km/h"
        winddirection = weather["wind_dir"]
        pressure = str(round(weather["pressure_mb"])) + "mBar"
        visibility = str(round(weather["vis_km"])) + "km"
        uv = int(weather["uv"])
        if 2 >= uv >= 1:
            uv = str(weather["uv"]) + " (Low)"
        elif 5 >= uv >= 3:
            uv = str(weather["uv"]) + " (Medium)"
        elif 7 >= uv >= 6:
            uv = str(weather["uv"]) + " (High)"
        elif 10 >= uv >= 8:
            uv = str(weather["uv"]) + " (Very High)"
        elif uv >= 11:
            uv = str(weather["uv"]) + " (Extremely High)"
        if units.value == "imperial":
            windspeed = str(round(weather["wind_mph"])) + "mp/h"
            pressure = str(round(weather["pressure_in"])) + "in"
            visibility = str(round(weather["vis_miles"])) + "miles"

        # ---------- Temperature Data ----------
        temperature = str(round(weather["temp_c"])) + "℃"
        feelslike = str(round(weather["feelslike_c"])) + "℃"
        if units.value == "imperial":
            temperature = str(round(weather["temp_f"])) + "℉"
            feelslike = str(round(weather["feelslike_f"])) + "℉"

        day = "<:day:1050879646469734470> Day"
        if weather["is_day"] == 0:
            day = "<:night:1050879649208598639> Night"

        weather_embed = discord.Embed(
            title=f"{city}, {country}",
            url=f"https://en.wikipedia.org/wiki/{city.replace(' ', '_')}",
            description=f"Showing weather of {city} {region}, {country}.\nIt's currently {day} time there.",
            color=discord.Color.blurple()
        )
        weather_embed.add_field(
            name="<:city:1050876004597510224> **__City Information:__**",
            value=f"Name: {city}\nRegion: {region}\nCountry: {country} :flag_{str(get_country.alpha_2).lower()}:\nLocation: {latitude} Latitude, {longitude} Longitude\nTimezone: {timezone}\nLocal Time: {localtime}",
            inline=False
        )
        weather_embed.add_field(
            name="<:weather:1050876912383295590> **__Weather Information:__**",
            value=f"Temperature: {temperature}\nFeels Like: {feelslike}\nCondition: {condition}\nHumidity: <:humidity:1050879211923062844> {humidity}\nUV Index: {uv}",
            inline=False
        )
        weather_embed.add_field(
            name="<:atmosphere:1050876002814926990> **__Atmospheric Information:__**",
            value=f"Wind Speed: {windspeed}\nWind Direction: {winddirection}\nPressure: {pressure}\nVisibility: {visibility}",
            inline=False
        )
        weather_embed.set_thumbnail(url=f"https://countryflagsapi.com/png/{get_country.alpha_2}")

        if hidden.value == 1:
            await interaction.response.send_message(embed=weather_embed, ephemeral=True)
        if hidden.value == 0:
            await interaction.response.send_message(embed=weather_embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Weather(bot))

#self.bot.application_info()