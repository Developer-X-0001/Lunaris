import aiosqlite
import os
import discord
from discord.ext import commands
from Interface.Buttons.SuggestionButtons import SuggestionButtons
from Interface.Buttons.ReportButtons import ReportButtons
import config

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
        self.database = await aiosqlite.connect("./Databases/data.db")
        self.add_view(SuggestionButtons())
        self.add_view(ReportButtons())
        for filename in os.listdir("./Commands"):
            if filename.endswith('.py'):
                await self.load_extension(f"Commands.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            if filename.startswith('__'):
                pass
        
        for filename in os.listdir("./Events"):
            if filename.endswith('.py'):
                await self.load_extension(f"Events.{filename[:-3]}")
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
    await bot.database.execute("CREATE TABLE IF NOT EXISTS ReportsAndSuggestions (guild_id, user_id, message_id, title, content, upvotes, downvotes, PRIMARY KEY (message_id))")
    await bot.database.execute("CREATE TABLE IF NOT EXISTS DataTransfer (guild_id, variable_1, variable_2, variable_3, PRIMARY KEY (guild_id))")
    await bot.database.execute("CREATE TABLE IF NOT EXISTS PremiumGuilds (guild_id, owner_id, PRIMARY KEY(guild_id))")
    await bot.database.execute("CREATE TABLE IF NOT EXISTS NotificationView (user_id, status, PRIMARY KEY (user_id))")
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
async def database_reload(ctx: commands.Context):
    await bot.database.execute("CREATE TABLE IF NOT EXISTS ReportsAndSuggestions (guild_id, user_id, message_id, title, content, upvotes, downvotes, PRIMARY KEY (message_id))")
    await bot.database.execute("CREATE TABLE IF NOT EXISTS DataTransfer (guild_id, variable_1, variable_2, variable_3, PRIMARY KEY (guild_id))")
    await bot.database.execute("CREATE TABLE IF NOT EXISTS PremiumGuilds (guild_id, owner_id, PRIMARY KEY(guild_id))")
    await bot.database.execute("CREATE TABLE IF NOT EXISTS NotificationView (user_id, status, PRIMARY KEY (user_id))")
    
    await ctx.send("<:Database:1009548177113894943> **Databases** ready!")

@bot.command()
@commands.is_owner()
async def notif_reset(ctx: commands.Context, user: discord.Member=None):
    database = await aiosqlite.connect("./Databases/data.db")
    if user is None:
        await database.execute("DROP TABLE NotificationView")
        await database.commit()
        await database.close()
        await ctx.send("✅ Success")
    else:
        try:
            await database.execute(f"DELETE FROM NotificationView WHERE user_id = {user.id}")
            await database.commit()
            await database.close()
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

bot.run(config.TOKEN)
