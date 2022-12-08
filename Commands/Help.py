import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Feeling lost? Get some help")
    async def help(self, interaction: discord.Interaction):
        help_embed = discord.Embed(
            title=""
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Help(bot))