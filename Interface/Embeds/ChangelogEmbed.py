import discord
import config

changelog_embed = discord.Embed(
    description="Nothing to see here 👀",
    colour=discord.Color.magenta()
)

changelog_embed.set_author(name='Last Updated on December 10, 2022', icon_url='https://i.imgur.com/fC3ZjuV.png')
changelog_embed.set_thumbnail(url='https://i.imgur.com/fC3ZjuV.png')
changelog_embed.set_footer(text=f'v{config.BOT_VERSION} | type /report to send bug reports to us')