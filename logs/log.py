import discord
import random
import time
import pymongo
import zlib
from pymongo import MongoClient
from datetime import datetime
from redbot.cogs.mod import Mod as ModClass
from redbot.core import Config, checks, commands, modlog
from redbot.core.commands.converter import TimedeltaConverter
from redbot.core.utils.chat_formatting import humanize_list, humanize_timedelta
from redbot.core.utils.mod import is_allowed_by_hierarchy
from redbot.core.utils.predicates import MessagePredicate
from steam.steamid import SteamID

class Logging(commands.Cog):
    """Logs a players punishments"""

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=1072001)
        default_guild = {"adminRole": 0, "ModRole": 0, "higherstaff" : 0}
        default_global = {"verified": []}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)
        self.bot = bot

    async def _process_request(self, ctx):
        user = ctx.author
        server = ctx.guild

        await ctx.send("{user}, Looks like you are trying to delete a users information. Are you sure you want to do this? Confirm by typing 'yes'".format(user=user))
        pred = MessagePredicate.yes_or_no(ctx)
        try:
            await self.bot.wait_for("message", timeout=15, check=pred)
        except AsyncTimeoutError:
            pass
        if not pred.result:
            await ctx.send("**Deletion Cancelled**")
            return False
        return True
        return True

    @commands.group()
    async def log(self, ctx):
        """Log your Warnings, and Mutes"""
        pass

    @log.command(name="profile", aliases=["p"])
    async def log_points(self, ctx: commands.Context, id: int):
        """View a players points for both warnings and mutes

        Additonal Syntax: `$log profile <Steam64ID>`"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        waCollection = db["WarnLogs"]
        muCollection = db["MuteLogs"]
        plCollection = db["PlayerLogs"]

        link = "https://steamcommunity.com/profiles/" + str(id)

        results = waCollection.find({"_id":id})
        muteResults = muCollection.find({"_id":id})
        playerResults = plCollection.find({"_id":id})

        try:
            embed = discord.Embed(
            title='Profile Found',
            description = 'Here is the information about the user',
            colour = discord.Colour.green())
            for result in results:
                steamID = (result["_id"])
                warnPoints = (result["MasterWarnPoints"])
                warnReason = (result["FirstWarnReason"])

                embed.add_field(name='Steam64 ID', value=steamID, inline=False)
                embed.add_field(name='Warning Points', value=warnPoints, inline=True)
                embed.add_field(name='Warning Reason', value=warnReason, inline=True)
            for plResult in playerResults:
                AddInfo = (plResult["AdditionalInformation"])
                embed.add_field(name='Additional Information:', value=AddInfo, inline=False)
            for muteResult in muteResults:
                mutePoints = (muteResult["MasterMutePoints"])
                muteReason = (muteResult["muteReason"])
                embed.add_field(name='Mute Points', value=mutePoints, inline=True)
                embed.add_field(name='Mute Reason', value=muteReason, inline=True)
            embed.add_field(name="Steam Profile URL:", value=link, inline=False)
            await ctx.send(embed=embed)
        except pymongo.errors.PyMongoError:
            embed = discord.Embed(
            title='User Profile not found',
            description = 'User does not have any warnings!',
            colour = discord.Colour.green())
            await ctx.send(embed=embed)

    @log.command(name="warn", aliases=["warning"])
    @checks.mod_or_permissions(manage_messages=True)
    async def log_warn(self, ctx: commands.Context, id: int, warnPoints:int, * , warnReason: str = ""):
        """Log your warnings"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        waCollection = db["WarnLogs"]
        wCollection = db["Warnings"]
        plCollection = db["PlayerLogs"]

        author = ctx.author

        adminRole = ctx.guild.get_role(await self.config.guild(ctx.guild).adminRole())
        modRole = ctx.guild.get_role(await self.config.guild(ctx.guild).ModRole())

        diceroll = random.randint(1,15)

        if diceroll == 15:
            await ctx.send("This message has been brought to you by Merp \n Merp! \n ||Jokes Aside, try the command again||")
            return


        blackListedID = [76561198872466187,76561198162423440]

        if id in blackListedID:
            embed=discord.Embed(title="Warning Failure", description="That user has been blacklisted, any further action against the user is prohibited ", color=0x272626)
            await ctx.send(embed=embed)
            return

        author = ctx.author.id

        if warnPoints > 5:
            if modRole in author.roles:
                embed = discord.Embed(
                title='Warning Failure',
                description = 'You cannot enter in more than 5 points at a time without an admin+',
                colour = discord.Colour.red())
                await ctx.send(embed=embed)
                return
        if warnPoints > 10:
            if adminRole in author.roles:
                embed = discord.Embed(
                title='Warning Failure',
                description = 'You cannot enter more than 10 points at a time without Higher Staff Approval',
                colour = discord.Colour.red())
                await ctx.send(embed=embed)
                return
            else:
                pass


        try:
            createWarnLog = {"_id":id, "MasterWarnPoints":warnPoints, "FirstWarnReason": warnReason}
            createWarning = {"_id":id, "Moderator":author}
            waCollection.insert_one(createWarnLog)
            wCollection.insert_one(createWarning)
            embed = discord.Embed(
            title='Warning Success',
            description = 'Warning has been registered!',
            colour = discord.Colour.green())
            await ctx.send(embed=embed)
        except pymongo.errors.DuplicateKeyError:
            AddWarning = waCollection.update_one({"_id":id}, {"$inc":{"MasterWarnPoints":warnPoints}})
            UpdateReason = waCollection.update_one({"_id":id}, {"$set":{"FirstWarnReason": warnReason}})
            embed = discord.Embed(
            title='Warning Success',
            description = 'Player had a previous warning, so the points have been updated!',
            colour = discord.Colour.green())

            warnResults = waCollection.find({"_id":id})
            for result in warnResults:
                warnPoints = (result["MasterWarnPoints"])
                if warnPoints >= 10:
                    embed.add_field(name='Warn Points Alert!', value="That user has over 10+ points. Alert a Higher Staff Member!", inline=False)
                elif warnPoints >= 9:
                    embed.add_field(name='Warn Points Alert!', value="That user has 9+ points. Issue the user a 7 Day Ban!", inline=False)
                elif warnPoints >= 8:
                    embed.add_field(name='Warn Points Alert!', value="That user has 8+ points. Issue the user a 3 Day Ban!", inline=False)
                elif warnPoints >= 6:
                    embed.add_field(name='Warn Points Alert!', value="That user has 6+ points. Issue the user a 5 Hour Ban!", inline=False)
                elif warnPoints >= 3:
                    embed.add_field(name='Warn Points Alert!', value="That user has 3+ points. Issue the user a 1 Hour Ban!", inline=False)
                else:
                    pass
            await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("Are you forgetting the users warning points?")
            return


    @log.command(name="delete", aliases=["del"])
    @checks.mod_or_permissions(manage_messages=True)
    async def log_delete(self, ctx: commands.Context, Type: str, id:int):
        """Delete a user's information

        Additonal Syntax: `$log delete <(warn/mute/mic)> <Steam64ID>`"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        waCollection = db["WarnLogs"]
        wCollection = db["Warnings"]
        mCollection = db["Mutes"]
        muCollection = db["MuteLogs"]

        if Type == "mute" or Type == "mic":
            try:
                muteDelete = mCollection.delete_one({"_id": id})
                muteLogDelete = muCollection.delete_one({"_id": id})
                embed = discord.Embed(
                title='Mute Deleted',
                description = 'Players mute information has been deleted!',
                colour = discord.Colour.green())
                await ctx.send(embed=embed)
            except pymongo.errors.PyMongoError:
                embed = discord.Embed(
                title='Mute Deletion Failed',
                description = 'Ask a developer for help!',
                colour = discord.Colour.red())
                await ctx.send(embed=embed)
        elif Type == "warn":
            try:
                warnDelete = wCollection.delete_one({"_id": id})
                warningLogDelete = waCollection.delete_one({"_id":id})
                embed = discord.Embed(
                title='Warning Deleted',
                description = 'Players Warning information has been deleted!',
                colour = discord.Colour.green())
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                title='Warning Deletion Failed',
                description = 'Ask a developer for help!',
                colour = discord.Colour.red())
                await ctx.send(embed=embed)

    @log.command(name="mute", aliases=["mic"])
    @checks.mod_or_permissions(manage_messages=True)
    async def log_mute(self, ctx: commands.Context, id : int, mutePoints : int, * ,muteReason : str = ""):
        """Log your mutes"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        mCollection = db["Mutes"]
        muCollection = db["MuteLogs"]
        plCollection = db["PlayerLogs"]

        author = ctx.author.id

        link = "https://steamcommunity.com/profiles/" + str(id)

        blackListedID = [76561198162423440,76561198872466187]

        if mutePoints > 10:
            embed = discord.Embed(
            title='Mute Failure',
            description = 'You cannot enter more than 10 points at a time',
            colour = discord.Colour.red())
            await ctx.send(embed=embed)
            return


        if id in blackListedID:
            embed=discord.Embed(title="Mute Failure", description="That user has been blacklisted, any further action against the user is prohibited ", color=0x272626)
            await ctx.send(embed=embed)
            return

        try:
            createMuteLog = {"_id":id, "MasterMutePoints":mutePoints, "muteReason":muteReason}
            createMute = {"_id":id, "URL":link, "Moderator" : author}
            MuteLog = muCollection.insert_one(createMuteLog)
            Muting = mCollection.insert_one(createMute)
            embed = discord.Embed(
            title='Mute Success',
            description = 'Mute has been registered!',
            colour = discord.Colour.green())
            await ctx.send(embed=embed)
        except pymongo.errors.DuplicateKeyError:
            AddMute = muCollection.update_one({"_id":id}, {"$inc":{"MasterMutePoints":mutePoints}})
            EditReason = muCollection.update_one({"_id":id}, {"$set":{"muteReason":muteReason}})
            embed = discord.Embed(
            title='Mute Success',
            description = 'Player had a previous mute, so the points have been updated!',
            colour = discord.Colour.green()
            )

            muteResults = muCollection.find({"_id":id})
            for result in muteResults:
                mutePoints = (result["MasterMutePoints"])
                if mutePoints >= 10:
                    embed.add_field(name='Mute Points Alert!', value="That user has over 10+ points. Alert a Higher Staff Member!", inline=False)
                elif mutePoints >= 9:
                    embed.add_field(name='Mute Points Alert!', value="That user has 9+ points. Mute them for a week!", inline=False)
                elif mutePoints >= 6:
                    embed.add_field(name='Mute Points Alert!', value="That user has 6+ points. Mute them for a day!", inline=False)
                elif mutePoints >= 3:
                    embed.add_field(name='Mute Points Alert!', value="That user has 3+ points. Mute them for a single round!", inline=False)
                else:
                    pass
            await ctx.send(embed=embed)

    @log.command(name="list")
    @checks.mod_or_permissions(administrator=True)
    async def log_list(self, ctx: commands.Context, Type : str):
        """Lists all the warns and mutes"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        waCollection = db["WarnLogs"]
        muCollection = db["MuteLogs"]

        if Type == "warns":
            await ctx.send("**MongoDB Current Warn List**\nOnly Use for Debugging Purposes!")
            result = waCollection.find({})

            for x in result:
                await ctx.send(x)
        if Type == "mutes" or Type == "mic":
            await ctx.send("**MongoDB Current Mute List**\nOnly Use for Debugging Purposes!")
            result = muCollection.find({})

            for x in result:
                await ctx.send(x)

    @log.command(name="info")
    @checks.mod_or_permissions(manage_messages=True)
    async def log_info(self, ctx: commands.Context, id : int, * , Information : str = ""):
        """Give the player additional information"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        plCollection = db["PlayerLogs"]

        blackListedID = [76561198872466187,76561198162423440]

        if id in blackListedID:
            embed=discord.Embed(title="Log Failure", description="That user has been blacklisted, any further action against the user is prohibited ", color=0x272626)
            await ctx.send(embed=embed)
            return

        try:
            AddInformation = {"_id":id, "AdditionalInformation":Information}
            PlayerInfo = plCollection.insert_one(AddInformation)
            embed = discord.Embed(
            title='Info Success!',
            description = 'Info Reason has been updated',
            colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)
        except pymongo.errors.DuplicateKeyError:
            UpdateReason = plCollection.update_one({"_id":id}, {"$set":{"AdditionalInformation":Information}})
            embed = discord.Embed(
            title='Info Success!',
            description = 'Info Reason has been updated',
            colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)

    @log.command(name="who")
    @checks.mod_or_permissions(manage_messages=True)
    async def log_who(self, ctx: commands.Context, id : int):
        """Finds the moderator who warned a user"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        waCollection = db["Warnings"]

        results = waCollection.find({"_id":id})

        try:
            for result in results:
                moderator = (result["Moderator"])
                await ctx.send("Here is the moderators ID: {id}".format(id=moderator))
        except pymongo.errors.PyMongoError:
            await ctx.send("Profile Not Setup, or User never warned")

    @log.command(name="link")
    @checks.admin()
    async def log_link(self, ctx: commands.Context, DiscordID : int , DiscordName: str, SteamID: int, * , SteamName : str):
        """Create and Link Players Accounts"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        plCollection = db["PlayerInfo"]

        try:
            createPlayer = {"_id":DiscordID, "DiscordName": DiscordName, "SteamID":SteamID, "SteamName":SteamName}
            LogPlayerInfo = plCollection.insert_one(createPlayer)
            embed = discord.Embed(
            title='Done!',
            description = 'Account Linked',
            colour = discord.Colour.green()
            )
            await ctx.send(embed=embed)
        except pymongo.errors.DuplicateKeyError:
            embed = discord.Embed(
            title='Failed!',
            description = 'Account Already Exists!',
            colour = discord.Colour.red()
            )
            await ctx.send(embed=embed)

    @log.command(name="help")
    @checks.mod_or_permissions(manage_messages=True)
    async def log_help(self, ctx):
        """More Indepth look into the commands"""
        await ctx.send("**Logging Command Help**\n\n __**Logging a warning**__\n You can log a warning with the command `$log warn <SteamID> <Points> <Reason>` Here is an example below: \n ```$log warn 76561198146812074 1 Killing Cuffed D-Class``` \n\n __**Logging a mute**__\nYou can log a mute with the following command: `$log mute <SteamID> <Points> <Reason>` Here is an example below:\n```$log mute 76561198146812074 2 Earrape in DeadChat```\n\n __**Deleting a Warning or Mute**__\nIf you ever need to delete a user's Warning or Mute History: `$log delete <mute/warn> <SteamID>` Here is an example of that:\n```$log delete mute 76561198146812074```\n\n __**Logging Long Term Bans**__\nIf you ever ban a player for a period longer than 1 week you use the following command: `$log info <SteamID> <Ban Information>` Here is an example below:\n```$log info 76561198146812074 1 Ban on Record: 2 Weeks```\n\n __**Viewing a Players Profile**__\nTo view a players previous Warning and Mute history use the following command: `$log profile <SteamID>`Here is example below:\n```$log profile 76561198146812074```\n\n__**Finding a Players Moderator**__\nIf you are unsure who warned a player use the following command: `$log who <SteamID>`\n\n__**Listing all Mutes and Warnings**__\nOnly use this for debugging purposes! `$log list <mutes/warns>`\n\n__**Linking A Players Discord and Steam**__\nThis is to keep track of players with Special Roles such as Donators or Staff who get promoted or demoted. `$log link <DiscordID> <DiscordName> <SteamID> <SteamName>`")

    @commands.group()
    @checks.admin()
    async def link(self, ctx):
        """Linking and Finding Players"""
        pass

    @link.command(name="find")
    @checks.admin()
    async def link_player(self, ctx: commands.Context, Type: str, ID : int):
        """Find a player"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        plCollection = db["PlayerInfo"]

        discord = "discord"
        steam = "steam"

        if Type.lower() == discord:
            results = plCollection.find({"_id":ID})
            try:
                for result in results:
                    DiscordID = (result["_id"])
                    DiscordName = (result["DiscordName"])
                    SteamID = (result["SteamID"])
                    SteamName = (result["SteamName"])

                    embed = discord.Embed(
                    title='Found!',
                    description = 'Account Found',
                    colour = discord.Colour.green()
                    )

                    embed.add_field(name='DiscordID', value=DiscordID, inline=False)
                    embed.add_field(name='Discord Name', value=DiscordName, inline=False)
                    embed.add_field(name='SteamID', value=SteamID, inline=False)
                    embed.add_field(name='Steam Name', value=SteamName, inline=False)
                    await ctx.send(embed=embed)
            except pymongo.errors.PyMongoError:
                await ctx.send("Profile Not Setup, or User never warned")
        elif Type.lower() == discord:
            results = plCollection.find({"SteamID":ID})
            try:
                for result in results:
                    DiscordID = (result["_id"])
                    DiscordName = (result["DiscordName"])
                    SteamID = (result["SteamID"])
                    SteamName = (result["SteamName"])

                    embed = discord.Embed(
                    title='Found!',
                    description = 'Account Found',
                    colour = discord.Colour.green()
                    )

                    embed.add_field(name='DiscordID', value=DiscordID, inline=False)
                    embed.add_field(name='Discord Name', value=DiscordName, inline=False)
                    embed.add_field(name='SteamID', value=SteamID, inline=False)
                    embed.add_field(name='Steam Name', value=SteamName, inline=False)
                    await ctx.send(embed=embed)
            except pymongo.errors.PyMongoError:
                await ctx.send("Profile Not Setup, or User never warned")
        else:
            await ctx.send("That's not a type, sorry")

    @log.command(name="amount")
    @checks.mod_or_permissions(manage_messages=True)
    async def log_amount(self, ctx: commands.Context):
        """Find out how many warnings and mutes have been entered"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        WLCollection = db["WarnLogs"]
        MLCollection = db["MuteLogs"]

        author = ctx.author

        adminRole = ctx.guild.get_role(await self.config.guild(ctx.guild).adminRole())
        modRole = ctx.guild.get_role(await self.config.guild(ctx.guild).ModRole())
        higherstaff = ctx.guild.get_role(await self.config.guild(ctx.guild).higherstaff())

        if modRole in author.roles:
            await ctx.send("This command has been disabled for Moderators!")
            return
        elif adminRole in author.roles:
            await ctx.send("This command has been disabled for Admins!")
            return
        elif higherstaff in author.roles:
            pass
        else:
            await ctx.send("This command has been disabled for any non-staff!")
            return

        WLMod = WLCollection.find().count()
        MLMod = MLCollection.find().count()

        embed = discord.Embed(
        title='Amounts of Warns/Mutes!',
        description = 'Here it is',
        colour = discord.Colour.green()
        )
        embed.add_field(name='Warnings', value=WLMod, inline=False)
        embed.add_field(name='Mutes', value=MLMod, inline=False)
        await ctx.send(embed=embed)

    @log.command(name="mod")
    @checks.mod_or_permissions(manage_messages=True)
    async def log_mod(self, ctx: commands.Context, user: discord.Member):
        """How many Warnings has a moderator done?"""
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        WLCollection = db["Warnings"]
        MLCollection = db["Mutes"]

        author = ctx.author

        adminRole = ctx.guild.get_role(await self.config.guild(ctx.guild).adminRole())
        modRole = ctx.guild.get_role(await self.config.guild(ctx.guild).ModRole())
        higherstaff = ctx.guild.get_role(await self.config.guild(ctx.guild).higherstaff())

        if modRole in author.roles:
            await ctx.send("This command has been disabled for Moderators!")
            return
        elif adminRole in author.roles:
            await ctx.send("This command has been disabled for Admins!")
            return
        elif higherstaff in author.roles:
            pass
        else:
            await ctx.send("This command has been disabled for any non-staff!")
            return

        DiscordID = user.id

        WLAmount = WLCollection.find({"Moderator" : DiscordID}).count()
        MLAmount = MLCollection.find({"Moderator": DiscordID}).count()

        try:
            embed = discord.Embed(
            title='Amount of Warnings',
            description = 'Here it is',
            colour = discord.Colour.green()
            )
            embed.add_field(name='Warnings', value=WLAmount, inline=False)
            embed.add_field(name='Mutes (Added as of 8/8/20)', value=MLAmount, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("That user does not exist, or has not entered any warnings")

    @log.command(name="purge")
    @checks.admin()
    async def log_purge(self , ctx : commands.Context, id : int):
        """Purge a users info"""
        author = ctx.author
        mongo_url = "mongodb+srv://DiscordRed:bigbob03@discord.wykzn.mongodb.net/discord?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["PLDatabase"]
        WLCollection = db["WarnLogs"]
        WACollection = db["Warnings"]
        MLCollection = db["MuteLogs"]
        MUCollection = db["Mutes"]

        try:
            muteDelete = MLCollection.delete_one({"_id": id})
            muteLogDelete = MUCollection.delete_one({"_id": id})
            warnDelete = WLCollection.delete_one({"_id": id})
            warningLogDelete = WACollection.delete_one({"_id":id})
            await ctx.send("Done, User's information has been purged!")
            return
        except:
            await ctx.send("Error: Unknown Error has occured.")
            return



    @commands.group(name="logsettings")
    @checks.admin()
    async def logsettings(self , ctx):
        """Edit the Logging Commands for Roles and Users"""
        pass

    @logsettings.command(name="roles")
    @checks.admin()
    async def logsettings_roles(self , ctx : commands.Context , RoleName : str,  role : discord.Role):
        """Set the Roles for Admins, Moderators, and Higher Staff"""

        if RoleName == "moderator":
            await self.config.guild(ctx.guild).ModRole.set(role.id)
            await ctx.send("The Moderator Role is now set to : {}".format(role.name))
        elif RoleName == "admin":
            await self.config.guild(ctx.guild).adminRole.set(role.id)
            await ctx.send("The Admin Role is now set to : {}".format(role.name))
        elif RoleName == "infinity":
            await self.config.guild(ctx.guild).higherstaff.set(role.id)
            await ctx.send("The Higer Staff Role is now set to : {}".format(role.name))
        else:
            await ctx.send("Unknown Role")
            return
