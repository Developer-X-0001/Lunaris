import traceback
import aiosqlite
import discord
from Interface.Buttons.SuggestionButtons import SuggestionButtons

class SubSuggestion(discord.ui.Modal, title="Suggestion"):
    heading = discord.ui.TextInput(
        label="Title of your suggestion",
        style=discord.TextStyle.short,
        placeholder="Type something catchy, for more upvotes ;)",
        required=True,
        max_length=30
    )

    suggestion = discord.ui.TextInput(
        label="Tell us what is in your brain",
        style=discord.TextStyle.long,
        placeholder="Suggest something unique ;)",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1051192443166527588)
        suggestion_embed = discord.Embed(
            title=self.heading,
            description=self.suggestion,
            color=discord.Color.magenta()
        )
        suggestion_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        suggestion_embed.set_thumbnail(url=interaction.guild.icon.url)
        suggestion_embed.set_footer(text=f"Sent from, Guild: {interaction.guild.name} | Members: {interaction.guild.member_count}")
        
        msg = await channel.send(embed=suggestion_embed, view=SuggestionButtons())
        await interaction.client.database.execute(f'INSERT INTO ReportsAndSuggestions VALUES ({interaction.guild.id}, {interaction.user.id}, {msg.id}, "{self.heading}", "{self.suggestion}", 0, 0)')
        await interaction.response.send_message("<:thankyou:1051209155144335521> Your suggestion has been recorded!", ephemeral=True)
        await interaction.client.database.commit()
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("<:error:1051184730248335410> Oops! Something went wrong.", ephemeral=True)

        traceback.print_tb(error.__traceback__)