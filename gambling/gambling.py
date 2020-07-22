import datetime
import time
import asyncio
from enum import Enum
import random
from decimal import Decimal
import aiohttp
import discord
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import escape, italics, humanize_number
from redbot.core import Config, bank, commands, errors, checks

class Gambling(commands.Cog):
    """Teaching Kids Gambling at a young age"""

    @commands.command()
    async def spin(self, ctx: commands.Context, bid: int):
        """A 1/6 chance of getting shot! But getting shot is the name of the game.
        You have a 5% chance of getting your bid multiplied by 10x
        You have a 45% chance of getting your bid multiplied by 5x
        You have a 50% chance of getting your bid multiplied by 2x"""
        author = ctx.author
        channel = ctx.channel
        then = await bank.get_balance(author)

        bonus = random.randint(1,100)
        chance = random.randint(1,6)

        if (bid > then):
            await ctx.send("You cannot have a bid larger than currently")
            return

        if (bid > 150):
            await ctx.send("Play a different game, you'll loose to much from this.")
            return

        else:
            await ctx.send("{player} spins the barrel".format(player=author))
            time.sleep(1)
            await ctx.send("{player} holds the gun up to their head. Aaaaaaaaaaaand...".format(player=author))
            time.sleep(2)
            now = bid
            if chance > 5:
                await ctx.send("BANG! :exploding_head:")
                time.sleep(1)
                if (bonus > 95):
                    await ctx.send("**Your Bid has been mulitplied 10x!**")
                    bonusbid = now * 10
                    currentbal = then + bonusbid
                    await bank.deposit_credits(author, bonusbid)
                    await ctx.send("You have been given {bid} {currency}!".format(bid=bonusbid, currency=await bank.get_currency_name(getattr(channel, "guild", None))))
                    await ctx.send("{then} --> {now}".format(then=then, now=currentbal))
                elif (bonus > 50 and bonus < 94):
                    await ctx.send("**Your bid has been multiplied by 5x!**")
                    bonusbid = now * 5
                    currentbal = then + bonusbid
                    await bank.deposit_credits(author, bonusbid)
                    await ctx.send("You have been given {bid} {currency}!".format(bid=bonusbid, currency=await bank.get_currency_name(getattr(channel, "guild", None))))
                    await ctx.send("{then} --> {now}".format(then=then, now=currentbal))
                else:
                    bonusbid = now * 2
                    currentbal = then + bonusbid
                    await ctx.send("**You have been awarded {credits} {currency} for dying!**".format(credits=bonusbid, currency=await bank.get_currency_name(getattr(channel, "guild", None))))
                    await bank.deposit_credits(author, bonusbid)
                    await ctx.send("{then} --> {now}".format(then=then, now=currentbal))


            else:

                await ctx.send("CLICK! :metal: :pensive:")
                time.sleep(1)
                await ctx.send("Unfortunely you live for another day")
                time.sleep(1)
                losebonus = now * 3
                current = then - losebonus
                await bank.withdraw_credits(author,losebonus)
                await ctx.send("You have lost a total of {credits} {currency} for not dying!".format(credits=losebonus, currency=await bank.get_currency_name(getattr(channel, "guild", None))))
                await ctx.send("{then} --> {now}".format(then=then, now=current))
