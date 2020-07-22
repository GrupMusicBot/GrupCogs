import discord
import random
import time
import pymongo
from re import search
from pymongo import MongoClient
from datetime import datetime
from redbot.core import commands
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import escape, italics, humanize_number
from steam.steamid import SteamID

class SCP(commands.Cog):
    """Lookup SCP Articles, but better"""

    @commands.command()
    async def scp(self, ctx: commands.Context, SCP_Number :  str):
        """Lookup an SCP Article of your choice, but better optimized

        Joke SCP's are included. An Example Syntax is:
        `$scp 049-j`
        """

        embedNameTitle = "SCP-" + SCP_Number
        embedURL = "http://www.scp-wiki.net/scp-" + SCP_Number

        embed=discord.Embed(title=embedNameTitle, url=embedURL, description="I found this about that specific SCP", color=0x57b774)
        await ctx.send(embed=embed)
