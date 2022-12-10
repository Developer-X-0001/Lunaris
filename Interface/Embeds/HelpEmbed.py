import discord

help_embed = discord.Embed(
    title=f"Lunaris Help",
    description="<:lunaris:1050333875613732894> **Lunaris!** A beautifully designed Meteorological Utility.",
    url="https://discord.com/api/oauth2/authorize?client_id=1043494805071745084&permissions=414464724032&scope=bot%20applications.commands",
    color=discord.Color.blurple()
)
help_embed.set_thumbnail(url="https://i.imgur.com/fC3ZjuV.png")
help_embed.add_field(name="<:command:1050333239866302534> Commands:", value="**Help** Shows this message.\n**Weather** Shows weather of a specified city.", inline=False)
