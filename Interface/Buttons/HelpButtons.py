import sqlite3
import discord
import config

from discord.ui import View, button, Button
from Interface.Embeds.HelpEmbed import help_embed
from Interface.Embeds.NotificationEmbed import notification_embed

database = sqlite3.connect("./Databases/data.db")

class HelpButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label = "Here", style=discord.ButtonStyle.green, custom_id="help_yes")
    async def help_yes(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=None, embed=help_embed, view=None)
    
    @button(label = "DMs", style=discord.ButtonStyle.blurple, custom_id="help_no")
    async def help_no(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.user.send(embed=help_embed)
            await interaction.response.edit_message(content="<:done:1051184732173520916> Check your DMs", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="<:error:1051184730248335410> Your DMs are closed!", embed=None, view=None)

class HelpButtonsWithNotif(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label = "Here", style=discord.ButtonStyle.green, custom_id="help_yes_2")
    async def help_yes_2(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=None, embed=help_embed, view=None)
    
    @button(label = "DMs", style=discord.ButtonStyle.blurple, custom_id="help_no_2")
    async def help_no_2(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.user.send(embed=help_embed)
            await interaction.response.edit_message(content="<:done:954610357727543346> Check your DMs", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="<:error:954610357761105980> Your DMs are closed!", embed=None, view=None)
    
    @button(label="View Notification", style=discord.ButtonStyle.red, emoji="<:notif:1051183724655554680>", custom_id="help_notif")
    async def help_notif(self, interaction: discord.Interaction, button: Button):
        notification_embed.set_thumbnail(url=interaction.client.user.avatar.url)
        database.execute("INSERT INTO NotificationView VALUES (?, ?) ON CONFLICT (user_id) DO UPDATE SET status = ? WHERE user_id = ?", (interaction.user.id, 'viewed', 'viewed', interaction.user.id,)).connection.commit()
        await interaction.response.edit_message(content="<:done:1051184732173520916> **Notification Viewed**", embed=notification_embed, view=HelpGoBackButtons())
        
class HelpGoBackButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Go Back", style=discord.ButtonStyle.gray, custom_id="go_back_help")
    async def go_back_help(self, interaction: discord.Interaction, button: Button):
        resp_embed = discord.Embed(
            title="Where do you want to receive the help page?",
            description="Here? or in DMs?",
            color=discord.Color.blurple()
        )
        resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
        await interaction.response.edit_message(embed=resp_embed, view=HelpButtons())