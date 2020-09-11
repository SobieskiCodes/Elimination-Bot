from discord.ext import commands
import json
import aiohttp
from pathlib import Path
import os

bot = commands.Bot(command_prefix='?')
with open("config.json", "r") as f:
    config = json.load(f)


@bot.event
async def on_ready():
    print("Logged in")


async def create_aiohttp():
    bot.aiohttp = aiohttp.ClientSession()


def load_extensions():
    bot.startup_extensions = []
    path = Path('./cogs')
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.strip('./') == str(path):
            for cog in filenames:
                if cog.endswith('.py'):
                    extension = 'cogs.'+cog[:-3]
                    bot.startup_extensions.append(extension)

    if __name__ == "__main__":
        for extension in bot.startup_extensions:
            try:
                bot.load_extension(extension)
                print(f'Loaded {extension}')
            except Exception as e:
                exc = f'{type(e).__name__}: {e}'
                print(f'Failed to load extension {extension}\n{exc}')


bot.loop.create_task(create_aiohttp())
load_extensions()
bot.api_keys = config['api_keys']
bot.donation_channel = config['channel']
bot.keyword = config['keyword']
bot.run(config['token'])
