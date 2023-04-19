import os
import config
import discord
import sqlite3

from discord.ext import commands
from Interface.Buttons.ReportButtons import ReportButtons
from Interface.Buttons.SuggestionButtons import SuggestionButtons

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

class Lunar(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=config.PREFIX,
            intents= intents,
            status=discord.Status.idle,
            activity=discord.Game(name=f"/help | v{config.BOT_VERSION}"),
            application_id = config.APPLICATION_ID
        )

    async def setup_hook(self):
        sqlite3.connect("./Databases/data.db").execute(
            '''
                CREATE TABLE IF NOT EXISTS ReportsAndSuggestions (
                    guild_id INTEGER,
                    user_id INTEGER,
                    message_id INTEGER,
                    title TEXT,
                    content TEXT,
                    upvotes INTEGER,
                    downvotes INTEGER,
                    PRIMARY KEY (message_id)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS DataTransfer (
                    guild_id INTEGER,
                    variable_1 TEXT,
                    variable_2 TEXT,
                    variable_3 TEXT,
                    PRIMARY KEY (guild_id)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS PremiumGuilds (
                    guild_id INTEGER,
                    owner_id INTEGER,
                    PRIMARY KEY(guild_id)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS NotificationView (
                    user_id INTEGER,
                    status TEXT,
                    PRIMARY KEY (user_id)
                )
            '''
        ).close()
        self.add_view(SuggestionButtons())
        self.add_view(ReportButtons())
        for filename in os.listdir("./Commands"):
            if filename.endswith('.py'):
                await self.load_extension(f"Commands.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            if filename.startswith('__'):
                pass
        
        for filename in os.listdir("./Tasks"):
            if filename.endswith('.py'):
                await self.load_extension(f"Tasks.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            if filename.startswith('__'):
                pass
        
        await bot.tree.sync()

bot = Lunar()

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord, current latency is {round(bot.latency * 1000)}ms")

@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx: commands.Context, folder:str, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.reload_extension(f"{folder}.{cog}")
    await ctx.send(f"🔁 {cog} reloaded!")

@bot.command(name="load")
@commands.is_owner()
async def load(ctx: commands.Context, folder:str, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.load_extension(f"{folder}.{cog}")
    await ctx.send(f"🆙 {cog} loaded!")

@bot.command()
@commands.is_owner()
async def notif_reset(ctx: commands.Context, user: discord.Member=None):
    database = sqlite3.connect("./Databases/data.db")
    if user is None:
        database.execute("DROP TABLE NotificationView")
        database.commit()
        database.close()
        await ctx.send("✅ Success")
    else:
        try:
            database.execute(f"DELETE FROM NotificationView WHERE user_id = {user.id}")
            database.commit()
            database.close()
            await ctx.send("✅ Success")
        except:
            await ctx.send("Can't find user in NotificationView table")

@bot.command()
async def count(ctx: commands.Context, type: str):
    if type == "member":
        count = 0
        for guild in bot.guilds:
            count += guild.member_count
        
        await ctx.send(count)
    
    if type == "guild":
        await ctx.send(bot.guilds.count)
    
    else:
        pass

@bot.command()
async def guilds(ctx: commands.Context):
    for guild in bot.guilds:
        try:
            invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
        except:
            invite = None

        await ctx.send(f'**Name:**{guild.name}\n**Member Count:**{guild.member_count}\n**Invites:**{invite}')
    
bot.run(config.TOKEN)
