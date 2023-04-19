import discord
import config

changelog_embed = discord.Embed(
    title="Last Updated on April 19, 2023",
    description="<:number1l:1098215706690080778> **Autocomplete feature:** Now when you search for the weather or use any other command using Lunaris, the bot will suggest city and location names that match your search query.\n\n<:number2l:1098215704299307020> **Improved performance:** We've optimized the code to ensure that Lunaris runs faster and smoother than ever before.",
    colour=discord.Color.blurple()
)

changelog_embed.set_thumbnail(url='https://i.imgur.com/fC3ZjuV.png')
changelog_embed.set_footer(text=f'v{config.BOT_VERSION} | type /report to send bug reports to us')