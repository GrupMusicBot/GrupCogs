import asyncio
import logging
import math
import operator
import platform
import random
import re
import textwrap
import time
from asyncio import TimeoutError as AsyncTimeoutError
from collections import OrderedDict
from datetime import timedelta
from tabulate import tabulate
from io import BytesIO
from typing import TYPE_CHECKING, Union, Tuple, List, Optional, Iterable, Sequence, Dict, Set

import aiohttp
import discord
from discord.utils import find
from fontTools.ttLib import TTFont
from redbot.core import bank
from redbot.core import checks
from redbot.core import commands
from redbot.core import Config
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.predicates import MessagePredicate

class SpecialTools(commands.Cog):
    """Special Commands for a special group of people"""

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @checks.mod_or_permissions(manage_messages=True)
    async def stream(self, ctx: commands.Context):
        """Alert Stream Annoucements"""

        if await self._process_request(ctx):
            await ctx.send("<@&688236803731619865> it's streaming time!")

    async def _process_request(self, ctx):
        user = ctx.author
        server = ctx.guild

        await ctx.send("{user}, You are about to ping Stream Annoucements. Are you sure? Confirm by typing 'yes'".format(user=user))
        pred = MessagePredicate.yes_or_no(ctx)
        try:
            await self.bot.wait_for("message", timeout=15, check=pred)
        except AsyncTimeoutError:
            pass
        if not pred.result:
            await ctx.send("**Request Cancelled**")
            return False
        return True
        return True
