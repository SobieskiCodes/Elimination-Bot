from discord.ext import commands
import random
import discord


class Elimination(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, team: str = None):
        url = f"https://api.torn.com/torn/?selections=competition&key={random.choice(self.bot.api_keys)}"
        async with self.bot.aiohttp.get(url) as resp:
            if resp.status == 200:
                check_if_running = await resp.json()
                if check_if_running.get('competition').get('competition') == 'Elimination':
                    teams = [x['name'].lower() for x in check_if_running.get('competition').get('teams')]
                    for x in teams:
                        if team and team.lower() in x:
                            e = discord.Embed(title=f"Stats for {x}", colour=discord.Colour(0x278d89))
                            for t in check_if_running.get('competition').get('teams'):
                                if t['name'].lower() in x:
                                    for i in t:
                                        e.add_field(name=i, value=t[i] if t[i] else "None")
                            await ctx.send(embed=e)
                            return

                    e = discord.Embed(title=f"Stats for Elimination 2020", colour=discord.Colour(0x278d89))
                    teams, score, lives = '', '', ''
                    for team in check_if_running.get('competition').get('teams'):
                        teams += f"{team['name']} \n"
                        score += f"{team['score']} \n"
                        lives += f"{team['lives']} \n"
                    e.add_field(name='Team', value=teams)
                    e.add_field(name='Score', value=score)
                    e.add_field(name='Lives', value=lives)
                    await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Elimination(bot))
