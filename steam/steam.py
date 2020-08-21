import discord
from redbot.core import Config, checks, commands, modlog
from steam.steamid import SteamID

class Steam(commands.Cog):
    """Commands that utilize the Steam API"""

    @commands.group(name="steam")
    async def steam(self, ctx):
        """A List of Commands that use the SteamAPI"""
        pass

    @steam.command(name="idfromprofile", aliases=["convert"])
    async def steam_idfp(self, ctx : commands.Context, SteamProfile : str):
        """Enter a user's Steam Profile URL, and it will respond with their ID"""
        convert = SteamID.from_url(SteamProfile)
        try:
            await ctx.send("User's Steam64ID: \n {}".format(convert))
            return
        except:
            await ctx.send("Profile Unavaible, or doesn't exist")
            return

    @steam.command(name="profilefromid",aliases=["steamconvert"])
    async def steam_pfid(self , ctx : commands.Context, Steam64ID : int):
        """Enter a user's Steam64ID, and it will respond with their profile link"""
        steamLink = ("https://steamcommunity.com/profiles/{Steam64ID}".format(Steam64ID=Steam64ID))
        await ctx.send(steamLink)
