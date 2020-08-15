
from discord.ext import commands


bot = commands.Bot(command_prefix="><", self_bot=True)
bot.load_extension("watcher")

@bot.event
async def on_ready():
    print("Chihayafuru is ready!")

bot.run("NzQ0MDM4NDI4NzY0Nzk5MDg4.XzdhkQ.4-frX8iSEzofT5wkTDJ_2L35xRA", bot=False)








