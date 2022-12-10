import discord

help_embed = discord.Embed(
    title=f"Lunaris Help",
    description="<:lunaris:1050333875613732894> **Lunaris!** A beautifully designed Meteorological Utility.",
    url="https://discord.com/api/oauth2/authorize?client_id=1043494805071745084&permissions=414464724032&scope=bot%20applications.commands",
    color=discord.Color.blurple()
)
help_embed.set_thumbnail(url="https://i.imgur.com/fC3ZjuV.png")
help_embed.add_field(name="<:command:1050333239866302534> Commands:", value="**Help** Shows this message.\n", inline=False)
help_embed.add_field(name="<:meteorology:1051212797930901604> Meteorological Commands:", value="**Weather** Get up to date current weather information.\n**Air Quality** Get up to date air quality information.\n**Astronomy** Get up to date information for sunrise, sunset, moonrise, moonset, moon phase and illumination.", inline=False)
help_embed.add_field(name="<:utilities:1051212795879895150> Utility Commands:", value="**Changelog** Check out latest updates added to the bot.\n**Information** Get information about the team behind **Lunaris**.\n**News** Check out latest announcements from the developers.\n**Report** Experiencing issues? Report it right now!\n**Suggestion** Want something new? Share your thoughts with us.\n")
