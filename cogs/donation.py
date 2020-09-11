from discord.ext import commands, tasks
import discord
import re
import asyncio


class Donation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.known_events = []
        self.cog_load()

    def cog_load(self):
        self.update_.start()

    def cog_unload(self):
        self.update_.cancel()

    @tasks.loop(seconds=60, reconnect=True)
    async def update_(self):
        for key in self.bot.api_keys:
            url = f"https://api.torn.com/user/?selections=Events&key={key}"
            async with self.bot.aiohttp.get(url) as resp:
                if resp.status == 200:
                    get_events = await resp.json()
                    events = get_events.get("events")
                    last_20 = list(events.keys())[:-20]
                    for event in last_20:
                        if self.bot.keyword in events.get(event).get('event').lower():
                            if 'someone' not in events.get(event).get('event').lower():
                                if event not in self.known_events:
                                    self.known_events.append(event)
                                    full_event = events.get(event).get('event')
                                    reg = "^(?:You were sent) (?:[a-z]+)?([0-9]+[a-z]{1}|\$[0-9,]+)?\ ?([0-9a-z\-,+: ]+?)?(?:from(?:.*))(?:XID=)([0-9]+)(?:\>)(.*)(?:\<\/a>)"
                                    matches = re.search(reg, full_event, re.IGNORECASE)
                                    if matches.group(1) and not matches.group(2):
                                        send_line = f"{matches.group(4)} [{matches.group(3)}] just donated {matches.group(1)}"

                                    if matches.group(2) and not matches.group(1):
                                        send_line = f"{matches.group(4)} [{matches.group(3)}] just donated a(n) {matches.group(2)}"

                                    if matches.group(1) and matches.group(2):
                                        send_line = f"{matches.group(4)} [{matches.group(3)}] just donated {matches.group(1)} {matches.group(2)}"

                                    channel = discord.utils.get(self.bot.get_all_channels(), name=self.bot.donation_channel)
                                    await channel.send(f"{send_line}")
                                    await asyncio.sleep(.5)

    @update_.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Donation(bot))
