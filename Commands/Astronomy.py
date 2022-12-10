import pycountry
import requests
import discord
import datetime
import config
from discord.ext import commands
from discord import app_commands

class Astro(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="astronomy", description="Get up to date information for sunrise, sunset, moonrise, moonset, moon phase and illumination.")
    @app_commands.describe(location="Type the city name", hidden="Choose wether to show information publicly or privately.")
    @app_commands.choices(
        hidden=[
            app_commands.Choice(name="True", value=1),
            app_commands.Choice(name="False", value=0)
        ]
    )
    async def astronomy(self, interaction: discord.Interaction, location: str, hidden: app_commands.Choice[int]):
        date = str(datetime.datetime.now().date())
        request_url = requests.get(f"http://api.weatherapi.com/v1/astronomy.json?key={config.WEATHER_API_KEY}&q={location}&dt={date}")
        response = request_url.json()
        
        location = response["location"]

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
        get_time = location["localtime_epoch"]
        localtime = datetime.datetime.fromtimestamp(get_time).strftime("%I:%M %p")

        # ---------- Astronomical Data ----------
        astroData = response["astronomy"]
        sunrise = astroData["astro"]["sunrise"]
        sunset = astroData["astro"]["sunset"]
        moonrise = astroData["astro"]["moonrise"]
        moonset = astroData["astro"]["moonset"]
        moon_phase = astroData["astro"]["moon_phase"]
        moon_illumination = astroData["astro"]["moon_illumination"]

        if moon_phase == "New Moon":
            moon_emoji = "<:newmoon:1051171346203279360>"
        if moon_phase == "Waxing Crescent":
            moon_emoji = "<:waxingcrescent:1051171333641355284>"
        if moon_phase == "First Quarter":
            moon_emoji = "<:firstquarter:1051171330797609060>"
        if moon_phase == "Waxing Gibbous":
            moon_emoji = "<:waxinggibbous:1051171327903547443>"
        if moon_phase == "Full Moon":
            moon_emoji = "<:fullmoon:1051171348333985885>"
        if moon_phase == "Waning Gibbous":
            moon_emoji = "<:waninggibbous:1051171343086927872>"
        if moon_phase == "Last Quarter":
            moon_emoji = "<:lastquarter:1051171336619307149>"
        if moon_phase == "Waning Crescent":
            moon_emoji = "<:waningcrescent:1051171340218007592>"

        astro_embed = discord.Embed(
            title=f"{city}, {country}",
            url=f"https://en.wikipedia.org/wiki/{city.replace(' ', '_')}",
            description=f"Showing astronomical information of {city} {region}, {country}.",
            color=discord.Color.blurple()
        )
        astro_embed.add_field(
            name="<:city:1050876004597510224> **__City Information:__**",
            value=f"Name: {city}\nRegion: {region}\nCountry: {country} :flag_{str(get_country.alpha_2).lower()}:\nLocation: {latitude} Latitude, {longitude} Longitude\nTimezone: {timezone}\nLocal Time: {localtime}",
            inline=False
        )
        astro_embed.add_field(
            name="<:astronomy:1051175887258787871> **__Astronomical Information:__**",
            value=f"Sunrise: {sunrise}\nSunset: {sunset}\n\nMoonrise: {moonrise}\nMoonset: {moonset}\nMoon Phase: {moon_phase} {moon_emoji}\nMoon Illumination: {moon_illumination}%",
            inline=False
        )
        astro_embed.set_thumbnail(url=f"https://countryflagsapi.com/png/{get_country.alpha_2}")

        if hidden.value == 1:
            await interaction.response.send_message(embed=astro_embed, ephemeral=True)
        if hidden.value == 0:
            await interaction.response.send_message(embed=astro_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Astro(bot))