import topgg
import config

from discord.ext import commands, tasks

class TopggPost(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook(config.WEBHOOK_URL, "28944726853595")
        bot.topgg_webhook.run(47395)
        bot.topggpy = topgg.DBLClient(bot, config.TOPGG_TOKEN, autopost=True)

    @commands.Cog.listener()
    async def on_autopost_success(self):
        print(
            f"Posted server count"
        )
        
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on Top.gg."""
        if data["type"] == "test":
            # this is roughly equivalent to
            # `return await on_dbl_test(data)` in this case
            return self.bot.dispatch("dbl_test", data)

        print(f"Received a vote:\n{data}")
       
    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        channel = self.bot.get_channel(config.DBL_TEST_CHANNEL_ID)
        await channel.send(f"Recieved a Test Vote for Cleaner, {data}")
        """An event that is called whenever someone tests the webhook system for your bot on Top.gg."""
        print(f"Received a test vote:\n{data}")

async def setup(bot: commands.Bot):
    await bot.add_cog(
        TopggPost(bot))