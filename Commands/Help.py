import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Feeling lost? Get some help")
    async def help(self, interaction: discord.Interaction):
        help_embed = discord.Embed(
            title=f"{self.bot.user.name} Help",
            description="<:lunaris:1050333875613732894> **Lunaris!** A beautifully designed Meteorological Utility.",
            url="https://discord.com/api/oauth2/authorize?client_id=1043494805071745084&permissions=414464724032&scope=bot%20applications.commands",
            color=0x120415
        )
        help_embed.set_thumbnail(url=self.bot.user.avatar.url)
        help_embed.add_field(name="<:command:1050333239866302534> Commands:", value="**Help** Shows this message.\n**Weather** Shows weather of a specified city.", inline=False)

        await interaction.response.send_message(embed=help_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Help(bot))