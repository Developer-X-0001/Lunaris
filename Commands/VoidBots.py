import config
from discord.ext import commands, tasks
import aiohttp # Use `pip install aiohttp` to install

class StatsUpload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.VoidUpload.start()

    def cog_unload(self):
        self.VoidUpload.cancel()

    @tasks.loop(minutes = 30)
    async def VoidUpload(self):
        await self.bot.wait_until_ready()
        async with aiohttp.ClientSession() as session:
            async with session.post(url = f"https://api.voidbots.net/bot/stats/{self.bot.user.id}",
            headers = {
            "content-type":"application/json",
            "Authorization": config.VOID_BOTS_TOKEN
            },
            json = {
            "server_count": len(self.bot.guilds),
            #"shard_count": len(self.bot.shards) #Uncomment this line if shards are used.
            }) as r:
                json = await r.json()
                print(json['message'])

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        StatsUpload(bot))