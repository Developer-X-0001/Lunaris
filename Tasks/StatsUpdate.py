from discord.ext import commands, tasks

class StatsUpdate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(minutes=10)
    async def update(self):
        await self.bot.wait_until_ready()
        guildcount_channel = self.bot.get_channel(1051190914145603704)
        shardcount_channel = self.bot.get_channel(1098210629191471214)
        membercount_channel = self.bot.get_channel(1051191049453838447)
        latency_channel = self.bot.get_channel(1051191221042810980)

        await guildcount_channel.edit(name=f"Server Count: {len(self.bot.guilds)}")
        await shardcount_channel.edit(name=f"Shard Count: {self.bot.shard_count}")
        membercount = 0
        for guild in self.bot.guilds:
            membercount += guild.member_count

        await membercount_channel.edit(name=f"Member Count: {membercount}")
        await latency_channel.edit(name=f"Latency: {round(self.bot.latency * 1000)}ms")
    
async def setup(bot: commands.Bot):
    await bot.add_cog(
        StatsUpdate(bot))