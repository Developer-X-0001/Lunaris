import config
import sqlite3
import discord

from discord import app_commands
from discord.ext import commands
from Interface.Buttons.HelpButtons import HelpButtons, HelpButtonsWithNotif

database = sqlite3.connect("./Databases/data.db")

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get a list of available commands")
    async def help(self, interaction: discord.Interaction):
        data = database.execute("SELECT status FROM NotificationView WHERE user_id = ?", (interaction.user.id,)).fetchone()
        if data is None:
            resp_embed = discord.Embed(
                title="Where do you want to receive the help page?",
                description="Here? or in DMs?",
                color=discord.Color.blurple()
            )
            resp_embed.set_footer(text=f"{self.bot.user.name}#{self.bot.user.discriminator} v{config.BOT_VERSION}")
            await interaction.response.send_message(content="<:notif:1051183724655554680> **You have an unread notification!**", embed=resp_embed, view=HelpButtonsWithNotif(), ephemeral=True)
        else:
            resp_embed = discord.Embed(
                title="Where do you want to receive the help page?",
                description="Here? or in DMs?",
                color=discord.Color.blurple()
            )
            resp_embed.set_footer(text=f"{self.bot.user.name}#{self.bot.user.discriminator} v{config.BOT_VERSION}")
            await interaction.response.send_message(embed=resp_embed, view=HelpButtons(), ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Help(bot))