import discord

from discord import app_commands
from discord.ext import commands

class News(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="news", description="Check latest news or messages sent by the developers.")
    async def news(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Latest Message | December 10, 2022",
            description="**Subject:** Lunaris Launched.\n\n<:lunaris:1050333875613732894> Introducing **Lunaris!**\nA beautifully designed Meteorological Utility.\nLunaris is packed with multiple astronomical commands, you can get latest weather information, forecast information, astronomical information, air quality information and alot more!\nJoin Lunaris support server https://discord.gg/invite/j6h9zZNPaJ and share your thoughts with us!\n\nRegards,\n*Developer X#0001*",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=interaction.client.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        News(bot))