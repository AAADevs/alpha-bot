"""This is a cog for a discord.py bot.
It will add general commands and responses to a bot

Commands:
    gif             make the bot post a random gif for a given search term
    search          make the bot post a web-search link
    howto           make the bot post tutorials
     ├ codeblocks       how to send discord markdown codeblocks
     ├ ask              how to ask question on the server
     ├ run              how to use felix run
     └ sticker          how to apply EM's stickers
    links           make the bot post links to the engineerman github pages
    memberinfo      provide information about the given member
    question        ask a question which the bot will answer using wolframalpha
    urbandictionary look up a word on urbandictionary.com
    video           make the bot post links to EM Videos on youtube
    weather         get the weather for a specific location
    inspect         print source code of a command
    statuscat       Commands that gives the requested HTTP statuses described and visualized by cats."
"""

import re
import random
import typing
import aiohttp
import os
from inspect import getsourcelines
from datetime import datetime as dt
from urllib.parse import quote
from discord.ext import commands
from http import HTTPStatus
from discord import (
    Embed,
    DMChannel,
    Member
)


class General(commands.Cog, name='General'):
    def __init__(self, client):
        self.client = client

    # ----------------------------------------------
    # Helper Functions
    # ----------------------------------------------
    def get_year_string(self):
        now = dt.utcnow()
        year_end = dt(now.year+1, 1, 1)
        year_start = dt(now.year, 1, 1)
        year_percent = (now - year_start) / (year_end - year_start) * 100
        return f'For your information, the year is {year_percent:.1f}% over!'

    async def gif_url(self, terms):
        url = (
            f'http://api.giphy.com/v1/gifs/search' +
            f'?api_key={self.client.config["giphy_key"]}' +
            f'&q={terms}' +
            f'&limit=20' +
            f'&rating=R' +
            f'&lang=en'
        )
        async with self.client.session.get(url) as response:
            gifs = await response.json()
        if 'data' not in gifs:
            if 'message' in gifs:
                if 'Invalid authentication credentials' in gifs['message']:
                    print('ERROR: Giphy API key is not valid')
            return None
        if not gifs['data']:
            return None
        gif = random.choice(gifs['data'])['images']['original']['url']
        return gif

    # ----------------------------------------------
    # Cog Event listeners
    # ----------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, msg):
        # Ignore messages sent by bots
        if msg.author.bot:
            return

        # Ignore DM
        if isinstance(msg.channel, DMChannel):
            return

        if self.client.user_is_ignored(msg.author):
            return

        if re.search(r'(?i).*what a twist.*', msg.content):
            await msg.channel.send('` - directed by M. Night Shyamalan.`')

        if re.search(
            r'(?i)(?:the|this) (?:current )?year is ' +
            r'(?:almost |basically )?(?:over|done|finished)',
            msg.content
        ):
            await msg.channel.send(self.get_year_string())

        if re.search(
            r'(?i)send bobs and vagene',
            msg.content
        ):
            await msg.channel.send('😏 *sensible chuckle*')

        if re.search(
            r'(?i)^(?:hi|what\'s up|yo|hey|hello) felix',
            msg.content
        ):
            await msg.channel.send('hello')

        if re.search(
            r'(?i)^felix should (?:i|he|she|they|we|<@!?\d+>)',
            msg.content
        ):
            if random.random() >= 0.5:
                response = 'the answer I am getting from my entropy is: Yes.'
            else:
                response = 'the answer I am getting from my entropy is: No.'
            await msg.channel.send(response)

        if re.search(
            r'(?i)^html is a programming language',
            msg.content
        ):
            await msg.channel.send('no it\'s not, don\'t be silly')

        if re.search(
            r'(?i)^you wanna fight, me\?',
            msg.content
        ):
            await msg.channel.send('bring it on pal (╯°□°）╯︵ ┻━┻')

        if re.search(
            r'(?i)^arrays start at 0',
            msg.content
        ):
            await msg.channel.send('arrays definitely start at 0')

        if re.search(
            r'(?i)^arrays start at 1',
            msg.content
        ):
            await msg.channel.send('arrays do not start at 1, they start at 0')

        if re.search(
            r'(?i)^felix meow',
            msg.content
        ):
            await msg.channel.send('ฅ^•ﻌ•^ฅ')

    # ----------------------------------------------
    # Cog Commands
    # ----------------------------------------------

    @commands.command(
        name='gif'
    )
    async def gif_embed(self, ctx, *, gif_name):
        """Post a gif
        Displays a random gif for the specified search term"""
        await ctx.trigger_typing()
        gif_url = await self.gif_url(gif_name)
        if gif_url is None:
            await ctx.send(f'Sorry {ctx.author.mention}, no gif found 😔')
            # await ctx.message.add_reaction('❌')
        else:
            e = Embed(color=0x000000)
            e.set_image(url=gif_url)
            e.set_footer(
                text=ctx.author.display_name,
                icon_url=ctx.author.avatar_url
            )

            await ctx.send(embed=e)
    # ------------------------------------------------------------------------

    @commands.command(
        name='search',
        aliases=['lmgtfy', 'duck', 'duckduckgo', 'google']
    )
    async def search(self, ctx, *, search_text):
        """Post a duckduckgo search link"""
        await ctx.trigger_typing()
        await ctx.send(
            f'here you go! <https://duckduckgo.com/?q={quote(search_text)}>'
        )
    # ------------------------------------------------------------------------

    @commands.command(
        name='stackoverflow',
        aliases=['stacko', 'stack']
    )
    async def stackoverflow(self, ctx, *, search_text):
        """Post a stackoverflow search link"""
        await ctx.trigger_typing()
        await ctx.send(
            f'here you go! <https://stackoverflow.com/?q={quote(search_text)}>'
        )

    @commands.group(
        name="howto",
        invoke_without_command=True,
        aliases=['how-to', 'info']
    )
    async def howto(self, ctx):
        """Show useful information for newcomers"""
        await ctx.send_help('how-to')

    @howto.command(
        name='codeblocks',
        aliases=['codeblock', 'code-blocks', 'code-block', 'code']
    )
    async def codeblocks(self, ctx):
        """Instructions on how to properly paste code"""
        code_instructions = (
            "Discord has an awesome feature called **Text Markdown** which "
            "supports code with full syntax highlighting using codeblocks."
            "To use codeblocks all you need to do is properly place the "
            "backtick characters *(not single quotes)* and specify your "
            "language *(optional, but preferred)*.\n\n"
            "**This is what your message should look like:**\n"
            "*\\`\\`\\`[programming language]\nYour code here\n\\`\\`\\`*\n\n"
            "**Here's an example:**\n"
            "*\\`\\`\\`python\nprint('Hello world!')\n\\`\\`\\`*\n\n"
            "**This will result in the following:**\n"
            "```python\nprint('Hello world!')\n```\n"
            "**NOTE:** Codeblocks are also used to run code via `felix run`."
        )
        link = (
            'https://support.discordapp.com/hc/en-us/articles/'
            '210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-'
        )

        e = Embed(title='Text markdown',
                  url=link,
                  description=code_instructions,
                  color=0x2ECC71)
        await ctx.send(embed=e)

    @howto.command(
        name='ask',
        aliases=['questions', 'question']
    )
    async def ask(self, ctx):
        """How to properly ask a question"""
        ask_instructions = (
            "From time to time you'll stumble upon a question like this:\n"
            "*Is anyone good at [this]?* / *Does anyone know [topic]?*\n"
            "Please **just ask** your question.\n\n"
            "• Make sure your question is easy to understand.\n"
            "• Use the appropriate channel to ask your question.\n"
            "• Always search before you ask (the internet is a big place).\n"
            "• Be patient (someone will eventually try to help you)."
        )

        e = Embed(title='Just ask',
                  description=ask_instructions,
                  color=0x2ECC71)
        await ctx.send(embed=e)


    @howto.command(
        name='font',
        aliases=['format', 'formatting', 'write']
    )
    async def font_format(self, ctx):
        """Instructions on how to format your text"""
        font_instructions = (
            "Discord supports font formatting with the following options:\n"
            "*italics*\u1160 \u1160 \u1160 \u1160\u1160\u1160\u1160"
            "\\*italics\\* | \\_italics\\_\n"
            "**bold**\u1160 \u1160 \u1160 \u1160 \u1160 \u1160\u1160"
            "\\*\\*bold\\*\\*\n"
            "***bold italics***\u1160 \u1160 \u1160\u1160\u1160"
            "\\*\\*\\*bold italics\\*\\*\\*\n"
            "__underline__\u1160 \u1160\u1160\u1160\u1160\u1160"
            "\\_\\_underline\\_\\_\n"
            "__*underline italics*__\u1160 \u1160 \u1160 "
            "\\_\\_\\*underline italics\\*\\_\\_\n"
            "__**underline bold**__\u1160\u1160\u1160\u1160"
            "\\_\\_\\*\\*underline bold\\*\\*\\_\\_\n"
            "__***underline bold italics***__\u1160 "
            "\\_\\_\\*\\*\\*underline bold italics\\*\\*\\*\\_\\_\n"
            "~~strikethrough~~\u1160 \u1160 \u1160 \u1160"
            "\\~\\~strikethrough\\~\\~\n"
        )
        link = (
            'https://support.discordapp.com/hc/en-us/articles/'
            '210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-'
        )

        e = Embed(title='Font Formatting',
                  url=link,
                  description=font_instructions,
                  color=0x2ECC71)
        await ctx.send(embed=e)

    # ------------------------------------------------------------------------

    @commands.command(
        name='question',
        aliases=['q']
    )
    async def question(self, ctx, *, question):
        """Ask Felix a question"""
        await ctx.trigger_typing()
        url = 'https://api.wolframalpha.com/v1/result?i=' + \
            f'{quote(question)}&appid={self.client.config["wolfram_key"]}'
        async with self.client.session.get(url) as response:
            answer = await response.text()
        if 'did not understand' in answer:
            answer = 'Sorry, I did not understand that'
        await ctx.send(answer)
    # ------------------------------------------------------------------------

    @commands.command(
        name='urban',
        aliases=['ud', 'urbandictionary', 'urbandict'],
    )
    async def urbandictionary(self, ctx, *, term):
        """Ask urbandictionary
        Get the definition of a word from Urbandictionary"""
        url = f'http://api.urbandictionary.com/v0/define?term={quote(term)}'
        async with self.client.session.get(url) as response:
            answer = await response.json()
        if not answer['list']:
            await ctx.send('Sorry, I did not understand that')
            return
        definition = answer["list"][0]["definition"]
        example = answer["list"][0]["example"]
        if len(definition + example) > 1950:
            definition = definition[:1950 - len(example)] + ' (...)'
        response = (
            '\n**Definition:**\n'
            f'{definition}\n'
            '\n**Example:**\n'
            f'{example}'
        )
        embed = Embed(
            title=f'"**{term}**" according to urbandictionary.com',
            url=f'https://urbandictionary.com/define.php?term={quote(term)}',
            description=response.replace('[', '').replace(']', ''),
            color=random.randint(0, 0xFFFFFF)
        )
        embed.set_footer(
            text=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    # ------------------------------------------------------------------------

    @commands.command(
        name='weather'
    )
    async def weather(
        self, ctx,
        location: str,
        days: typing.Optional[int] = 0,
        units: typing.Optional[str] = 'm',
    ):
        """Get the current weather/forecast in a location

        Probably difficult to view on mobile

        Options:
          \u1160**location** examples:
            \u1160\u1160berlin
            \u1160\u1160~Eiffel+tower
            \u1160\u1160Москва
            \u1160\u1160muc
            \u1160\u1160@stackoverflow.com
            \u1160\u116094107
            \u1160\u1160-78.46,106.79
          \u1160**days** (0-3):  The amount of forecast days
          \u1160**units** (m/u/mM/uM): m = Metric | u = US | M = wind in M/s

          API used: https://en.wttr.in/:help"""
        if units not in ["m", "u", "mM", "uM"]:
            location = f"{location} {units}"
            units = "m"
        location = location.replace('.png', '')
        moon = location.startswith('moon')
        url = (
            'https://wttr.in/'
            f'{location}?{units}{days}{"" if days else "q"}nTAF'
        )
        async with self.client.session.get(url) as response:
            weather = await response.text()
            weather = weather.split('\n')
        if len(weather) < 8:
            weather = f'the weather api returned an invalid response, try again later'
            await ctx.send(weather)
            return
        if 'Sorry' in weather[0] or (weather[1] and not moon):
            return
        if days:
            weather = [weather[0]]+weather[7:]
            if len(weather[-1]) == 0:
                weather = weather[:-1]
            if weather[-1].startswith('Location'):
                weather = weather[:-1]
        weather_codeblock = '```\n' + '\n'.join(weather) + '```'
        if len(weather_codeblock) > 2000:
            weather_codeblock = 'Sorry - response longer than 2000 characters'
        await ctx.send(weather_codeblock)


    # ------------------------------------------------------------------------
    
    @commands.command(aliases=['coin'])
    async def flipcoin(self, ctx):
        '''Flips a coin'''
        choices = ['You got Heads', 'You got Tails']
        color = discord.Color.green()
        em = discord.Embed(color=color, title='Coinflip:', description=random.choice(choices))
        await ctx.send(embed=em)

    @commands.command()
    async def dice(self, ctx, number=1):
        '''Rolls a certain number of dice'''
        if number > 20:
            number = 20

        fmt = ''
        for i in range(1, number + 1):
            fmt += f'`Dice {i}: {random.randint(1, 6)}`\n'
            color = discord.Color.green()
        em = discord.Embed(color=color, title='Roll a certain number of dice', description=fmt)
        await ctx.send(embed=em)

    @commands.command(aliases=['xkcd', 'comic'])
    async def randomcomic(self, ctx):
        '''Get a comic from xkcd.'''
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/info.0.json') as resp:
                data = await resp.json()
                currentcomic = data['num']
        rand = random.randint(0, currentcomic)  # max = current comic
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://xkcd.com/{rand}/info.0.json') as resp:
                data = await resp.json()
        em = discord.Embed(color=discord.Color.green())
        em.title = f"XKCD Number {data['num']}- \"{data['title']}\""
        em.set_footer(text=f"Published on {data['month']}/{data['day']}/{data['year']}")
        em.set_image(url=data['img'])
        await ctx.send(embed=em)

    @commands.command(aliases=['number'])
    async def numberfact(self, ctx, number: int):
        '''Get a fact about a number.'''
        if not number:
            await ctx.send(f'Usage: `{ctx.prefix}numberfact <number>`')
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://numbersapi.com/{number}?json') as resp:
                    file = await resp.json()
                    fact = file['text']
                    await ctx.send(f"**Did you know?**\n*{fact}*")
        except KeyError:
            await ctx.send("No facts are available for that number.")

    # ------------------------------------------------------------------------------------
    @commands.command()
    async def rps(self, ctx, choice):
        choice = choice.lower()
        possible_choices = ["rock", "paper", "scissors"]
        avy = str(ctx.message.author.avatar_url)
        name = ctx.message.author.display_name
        var1 = random.choice(possible_choices)
        if choice == "rock":
            thumb = "https://pngimg.com/uploads/stone/stone_PNG13545.png"
            if var1 == "paper":
                winner = "Yay! I won!"
            elif var1 == "rock":
                winner = "It's a tie!"
            elif var1 == "scissors":
                winner = f"{name} wins!"
            else:
                winner = "woahhhhh"
        elif choice == "paper":
            thumb = "https://cdn.pixabay.com/photo/2017/10/07/21/57/pape-2828083_960_720.png"
            if var1 == "rock":
                winner = f"{name} wins!"
            elif var1 == "paper":
                winner = "It's a tie!"
            elif var1 == "scissors":
                winner = "Yay! I win!"
            else:
                winner = "woahhhhh"
        elif choice == "scissors":
            thumb = "https://pngimg.com/uploads/scissors/scissors_PNG25.png"
            if var1 == "rock":
                winner = "Yay! I won!"
            elif var1 == "paper":
                winner = f"{name} wins!"
            elif var1 == "scissors":
                winner = "It's a tie!"
        else:
            await ctx.send("You must either say rock, paper, or scissors!")
            return
        embed = await self.client.embed(description="Rock Paper Scissors!")
        embed.add_field(name=f"{name}'s Choice", value=choice, inline=False)
        embed.add_field(name="My Choice", value=var1, inline=False)
        embed.add_field(name="Results:", value=winner, inline=False)
        embed.set_thumbnail(url=thumb)
        embed.set_author(name=name, icon_url=avy)
        embed.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(General(client))
