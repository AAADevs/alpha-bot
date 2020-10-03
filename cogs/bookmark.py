import logging
import random
from discord import (
	Message,
	Embed,
	Forbidden
	)
from discord.ext import commands


log = logging.getLogger(__name__)

class Bookmark(commands.Cog):
    """Creates personal bookmarks by relaying a message link to the user's DMs."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="bookmark", aliases=("bm", "pin"))
    async def bookmark(self, ctx: commands.Context, target_message: Message, *, title: str = "Bookmark") -> None:
        """Send the author a link to `target_message` via DMs."""
        # Prevent users from bookmarking a message in a channel they don't have access to
        permissions = ctx.author.permissions_in(target_message.channel)
        if not permissions.read_messages:
            log.info(f"{ctx.author} tried to bookmark a message in #{target_message.channel} but has no permissions")
            embed = Embed(
                title="Error",
                color=0xcd6d6d,
                description="You don't have permission to view this channel."
            )
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title=title,
            colour=0x68c290,
            description=target_message.content
        )
        embed.add_field(name="Wanna give it a visit?", value=f"[Visit original message]({target_message.jump_url})")
        embed.set_author(name=target_message.author, icon_url=target_message.author.avatar_url)
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/zl4oDwcmxUILY7sD9ZWE2fU5R7n6QcxEmPYSE5eddbg/%3Fv%3D1/https/cdn.discordapp.com/emojis/654080405988966419.png?width=20&height=20")

        try:
            await ctx.author.send(embed=embed)
        except Forbidden:
            error_embed = Embed(
                title="Error",
                description=f"{ctx.author.mention}, please enable your DMs to receive the bookmark",
                colour=0xcd6d6d
            )
            await ctx.send(embed=error_embed)
        else:
            log.info(f"{ctx.author} bookmarked {target_message.jump_url} with title '{title}'")
            await ctx.message.add_reaction("\U0001F4E8")


def setup(bot: commands.Bot) -> None:
    """Load the cog."""
    bot.add_cog(Bookmark(bot))
