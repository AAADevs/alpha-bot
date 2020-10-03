import discord
from discord.ext import commands
import math
from io import BytesIO
from discord.ext.commands.cooldowns import BucketType
import aiohttp



async def check_answer(ctx, answer):
    print(str(answer))
    if len(str(answer)) > 2000:
        try:
            url = await ctx.bot.post_to_mystbin(answer)
            await ctx.send(f"Your result was too long for discord, so I put it here instead! {url}")
        except (aiohttp.ContentTypeError, AssertionError):
            fp = discord.File(BytesIO(str(answer).encode("utf-8")), "out.txt")
            await ctx.send("Your file was too long for discord, so I put it here instead!", file=fp)
            return None
    elif str(answer) == "inf":
        await ctx.send("This number is too large for Python to handle!")
        return None
    else:
        return True


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def square(self, ctx, number):
        """Shows the square of a number"""
        square = float(number) ** 2
        if await check_answer(ctx, square):
            await ctx.send(f"{number}² is {square}")

    @commands.command()
    async def root(self, ctx, number):
        """Shows the square root of a number"""
        answer = math.sqrt(float(number))
        if await check_answer(ctx, answer):
            await ctx.send(f"The square root of {number} is {answer}")

    @commands.command()
    async def multiply(self, ctx, number1, number2):
        """Shows the multiplication of 2 numbers"""
        multiplied_value = float(number1) * float(number2)
        if await check_answer(ctx, multiplied_value):
            await ctx.send(f"{number1} multiplied by {number2} is {multiplied_value}")


    @commands.command()
    async def exp(self, ctx, number1, number2):
        """"Shows the exponent a number raised to the 2nd number"""
        answer = float(number1) ** float(number2)
        if await check_answer(ctx, answer):
            await ctx.send(f"{number1} to the power of {number2} is {answer}")

    @commands.command()
    async def sine(self, ctx, number):
        """Shows the sine of a number"""
        answer = math.sin(float(number))
        if await check_answer(ctx, answer):
            await ctx.send(f"The sine of {number} is {answer}")

    @commands.command()
    async def cos(self, ctx, number):
        """Shows the cos of a number"""
        answer = math.cos(float(number))
        if await check_answer(ctx, answer):
            await ctx.send(f"The cosine of {number} is {answer}")

    @commands.command()
    async def tan(self, ctx, number):
        """Shows the tan of a number"""
        answer = math.tan(float(number))
        if await check_answer(ctx, answer):
            await ctx.send(f"The tangent of {number} is {answer}")

    @commands.command()
    async def divide(self, ctx, number1, number2):
        """Shows the division of 2 numbers"""
        answer = float(number1) / float(number2)
        if await check_answer(ctx, answer):
            await ctx.send(f"{number1} divided by {number2} is {answer}")

    @commands.command()
    async def add(self, ctx, number1, number2):
        """Shows the addition of 2 numbers"""
        added_value = float(number1) + float(number2)
        if await check_answer(ctx, added_value):
            await ctx.send(f"{number1} + {number2} is {added_value}")

    @commands.command()
    async def subtract(self, ctx, number1, number2):
        """Shows the subtraction of 2 numbers"""
        subtracted_value = float(number1) - float(number2)
        if await check_answer(ctx, subtracted_value):
            await ctx.send(f"{number1} - {number2} is {subtracted_value}")

    @commands.command()
    async def average(self, ctx, *args: int):
        """Shows the average of a list of numbers"""
        answer = sum(args) / len(args)
        if await check_answer(ctx, answer):
            await ctx.send(f"The average is {answer}")


def setup(client):
    client.add_cog(Math(client))