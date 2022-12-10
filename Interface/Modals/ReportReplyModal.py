import aiosqlite
import discord
from discord.ui import Modal

class ReplyModal(Modal, title="Report/Suggestion Reply"):
    def __init__(self):
        super().__init__(timeout=None)
    
    reply = discord.ui.TextInput(
        label="Your reply",
        style=discord.TextStyle.long,
        placeholder="Type your reply here...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        async with interaction.client.database.execute(f"SELECT user_id, title, content, upvotes, downvotes FROM ReportsAndSuggestions WHERE message_id = {interaction.message.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            await interaction.response.send_message("<:error:1051184730248335410> Oops! Something went wrong...", ephemeral=True)
            return
        else:
            user = await interaction.client.fetch_user(data[0])
            try:
                await user.send(content=f"<:notif:1051183724655554680> **You have a new reply on your report/suggestion post!**\n\n**{interaction.user.name}** has replied to your following post:\n\n> **{data[1]}**\n> {data[2]}\n\n**Votes:** <:upvote:1026912667824312350> `{data[3]}` <:downvote:1026912669812412437> `{data[4]}`\n\n**Reply:** {self.reply}")
            except discord.errors.Forbidden:
                await interaction.response.send_message(f"<:error:1051184730248335410> I'm unable to DM {user.name}, instead I've sent the message to their mailbox.", ephemeral=True)