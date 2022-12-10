import discord
from discord import app_commands
from discord.ext import commands

class News(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="news", description="Check latest news or messages sent by the developers.")
    async def news(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Latest Message | August 27, 2022",
            description="**Subject:** 🎉 Celebrating 2k Servers!\n\n<:cleaner:954598059952734268> **Cleaner#8788** is reaching 2000 servers, keeping them clean and providing quality services. On September 3rd, 2022 we are going to have live stream on our Stage Channel in [Cleaner's Support Server](https://discord.gg/QrFEfNuC5m). Make sure to join us, I (Developer X) will be there to answer your questions and also we may play some games together 😉. So yeah stay tuned with us!\n\nRegards,\n*Developer X#0001*",
            color=discord.Color.magenta()
        )
        embed.set_thumbnail(url=interaction.client.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        News(bot))