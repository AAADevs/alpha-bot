from http import HTTPStatus
import random
import discord
from discord.ext import commands


# All valid status code, which are required while returning a random image of a cat, portraying the status code.
VALID_CODE = [100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 401, 402, 403, 404, 405, 406,
              400, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 429, 431,
              444, 450, 451, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511]


class StatusCats(commands.Cog):
    """Commands that gives the requested HTTP statuses described and visualized by cats."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['statuscat'])
    async def httpcat(self, ctx: commands.Context, code=999) -> None:
        """Sends an embed with an image of a cat, portraying the status code.
           If the status code is wrong than it will return a random status cat.
           If no status code given it will return a random status cat."""
        embed = discord.Embed(title=f'**Status: {code}**')
        embed.set_footer(text=f"Image got from https://http.cat/{code}.jpg.")

        try:
            HTTPStatus(code)

        except ValueError:
            # choosing a random valid status code
            code = random.choice(VALID_CODE)
            # Over writing the previous footer and title
            embed = discord.Embed(title=f'**Status: {code}**')
            embed.set_footer(text=f"""Inputted status code does not exist. Here is a random status.
                                    Image got from https://http.cat/{code}.jpg.""")

            HTTPStatus(code)
            embed.set_image(url=f'https://http.cat/{code}.jpg')

        else:
            embed.set_image(url=f'https://http.cat/{code}.jpg')

        finally:
            await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Load the StatusCats cog."""
    bot.add_cog(StatusCats(bot))
