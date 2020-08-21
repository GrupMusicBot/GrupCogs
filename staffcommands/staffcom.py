import discord
import random
import time
from redbot.cogs.mod import Mod as ModClass
from redbot.core import Config, checks, commands, modlog
from redbot.core.commands.converter import TimedeltaConverter
from redbot.core.utils.chat_formatting import humanize_list, humanize_timedelta
from redbot.core.utils.mod import slow_deletion, mass_purge
from redbot.core.utils.predicates import MessagePredicate

class staffCom(commands.Cog):
    """A Command for all staff members to use for various applications"""

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=1072001)
        default_guild = {"adminRole": 0, "adminOnLeave" : 0, "ModRole": 0, "ModOnLeave" : 0, "offduty" : 0, "higherstaff" : 0, "developer" : 0, "headmod" : 0, "tmod" : 0}
        default_global = {"verified": []}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)
        self.bot = bot

    async def _process_request(self, ctx):
        user = ctx.author
        server = ctx.guild

        await ctx.send("{user}, looks like you are going on leave? Type 'yes' to confirm".format(user=user))
        pred = MessagePredicate.yes_or_no(ctx)
        try:
            await self.bot.wait_for("message", timeout=15, check=pred)
        except AsyncTimeoutError:
            pass
        if not pred.result:
            await ctx.send("**Cancelled**")
            return False
        return True
        return True

    @commands.group(name="staff")
    async def staff(self, ctx):
        """A command hub for all staff members"""
        pass

    @staff.command(name="absence")
    @checks.mod_or_permissions(manage_messages=True)
    async def staff_modleave(self , ctx : commands.Context, Duration: int , Steam64ID : int , * , Reason : str = ""):
        """Allows staff member to go on temporary leave"""
        author = ctx.author

        adminRole = ctx.guild.get_role(await self.config.guild(ctx.guild).adminrole())
        modRole = ctx.guild.get_role(await self.config.guild(ctx.guild).ModRole())

        durationFixed = ("{Duration} days".format(Duration=Duration))
        steamIDFixed = ("{steam}@steam".format(steam=Steam64ID))

        if adminRole in author.roles:
            try:
                embed = discord.Embed(
                title='Admin On Leave',
                description = 'You have gone on leave, the rest of the information is for higher staff',
                colour = discord.Colour.green())
                embed.add_field(name='Admin Leaving', value=author, inline=True)
                embed.add_field(name='Duration of Leave', value=durationFixed, inline=True)
                embed.add_field(name='Reason for Leave', value=Reason, inline=False)
                embed.add_field(name='SteamID', value=steamIDFixed, inline=False)
                if not await self.config.guild(ctx.guild).adminOnLeave() == 0:
                    await author.add_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).adminOnLeave()),
                        reason="Admin going on leave, removing role",)
                if not await self.config.guild(ctx.guild).adminrole() == 0:
                    await author.remove_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).adminrole()),
                        reason="Removing Admin due to leave",)
                await ctx.send(embed=embed)
            except:
                await ctx.send("An error has occured, try again later")
                return
        elif modRole in author.roles:
            try:
                embed = discord.Embed(
                title='Moderator On Leave',
                description = 'You have gone on leave, the rest of the information is for higher staff',
                colour = discord.Colour.green())
                embed.add_field(name='Moderator Leaving', value=author, inline=True)
                embed.add_field(name='Duration of Leave', value=durationFixed, inline=True)
                embed.add_field(name='Reason for Leave', value=Reason, inline=False)
                embed.add_field(name='SteamID', value=steamIDFixed, inline=False)
                if not await self.config.guild(ctx.guild).ModOnLeave() == 0:
                    await author.add_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).ModOnLeave()),
                        reason="Moderator going on leave, removing role",)
                if not await self.config.guild(ctx.guild).ModRole() == 0:
                    await author.remove_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).ModRole()),
                        reason="Removing Moderator due to leave",)
                await ctx.send(embed=embed)

            except:
                await ctx.send("There has been an error, try again later")
                return
        else:
            await ctx.send("You cannot go on leave with the current role you have!")
            return

    @staff.command(name="return")
    @checks.mod_or_permissions(manage_messages=True)
    async def staff_return(self , ctx : commands.Context):
        """Allows staff to return"""
        author = ctx.author

        adminRole = ctx.guild.get_role(await self.config.guild(ctx.guild).adminOnLeave())
        modRole = ctx.guild.get_role(await self.config.guild(ctx.guild).ModOnLeave())

        if adminRole in author.roles:
            try:
                embed = discord.Embed(
                title='Admin Returning',
                description = 'You have returned from your leave, Welcome Back!',
                colour = discord.Colour.green())
                if not await self.config.guild(ctx.guild).adminOnLeave() == 0:
                    await author.remove_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).adminOnLeave()),
                        reason="Admin Returning from Leave, removing AOL",)
                if not await self.config.guild(ctx.guild).adminrole() == 0:
                    await author.add_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).adminrole()),
                        reason="Admin Returning from Leave, Giving Admin Role",)
                await ctx.send(embed=embed)
            except:
                await ctx.send("An error has occured, try again later")
                return
        elif modRole in author.roles:
            try:
                embed = discord.Embed(
                title='Moderator Returning',
                description = 'You have returned from your leave, Welcome Back!',
                colour = discord.Colour.green())
                if not await self.config.guild(ctx.guild).ModOnLeave() == 0:
                    await author.remove_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).ModOnLeave()),
                        reason="Moderator Returning, removing MOL",)
                if not await self.config.guild(ctx.guild).ModRole() == 0:
                    await author.add_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).ModRole()),
                        reason="Moderator Returning from leave, giving Moderator Role",)
                await ctx.send(embed=embed)
            except:
                await ctx.send("There has been an error, try again later")
                return
        else:
            await ctx.send("You do not have leaving roles.")
            return

    @staff.command(name="offduty")
    @checks.mod_or_permissions(manage_messages=True)
    async def offduty(self , ctx : commands.Context):
        """Allows admins to go offduty"""
        author = ctx.author

        blacklistedID = 204265341549805568

        if author.id == blacklistedID:
            await ctx.send("You cannot go off-duty")
            return
        else:
            pass

        adminRole = ctx.guild.get_role(await self.config.guild(ctx.guild).adminrole())

        if adminRole in author.roles:
            try:
                if not await self.config.guild(ctx.guild).offduty() == 0:
                    await author.add_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).offduty()),
                        reason="User has gone off duty",)
                if not await self.config.guild(ctx.guild).adminrole() == 0:
                    await author.remove_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).adminrole()),
                        reason="Removing Admin due to Off-Duty",)
                await ctx.send("Done!")
            except:
                return
        else:
            await ctx.send("You are not an admin, therefore cannot go off-duty!")
            return

    @staff.command(name="onduty")
    @checks.mod_or_permissions(manage_messages=True)
    async def onduty(self , ctx : commands.Context):
        """Allows admins to go onduty"""
        author = ctx.author
        adminRole = ctx.guild.get_role(await self.config.guild(ctx.guild).offduty())

        if adminRole in author.roles:
            try:
                if not await self.config.guild(ctx.guild).offduty() == 0:
                    await author.remove_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).offduty()),
                        reason="User is going back on-duty",)
                if not await self.config.guild(ctx.guild).adminrole() == 0:
                    await author.add_roles(
                        ctx.guild.get_role(await self.config.guild(ctx.guild).adminrole()),
                        reason="Adding Admin, user is returning from off-duty",)
                await ctx.send("Done!")
            except:
                return
        else:
            await ctx.send("You are not an admin, therefore cannot go off-duty!")
            return

    @staff.group(name="role")
    async def staffRole(self , ctx):
        """Staff Role Options"""
        pass

    @staffRole.command(name="save")
    @checks.admin()
    async def staffRole_save(self, ctx: commands.Context, RoleName : str, role : discord.Role):
        """
        - higherstaff
        - developer
        - headmod
        - admin
        - moderator
        - trialmoderator
        - adminonleave
        - modonleave"""

        if RoleName == "higherstaff":
            await self.config.guild(ctx.guild).higherstaff.set(role.id)
            await ctx.send("The Higher Staff Role is now : {}".format(role.name))
        elif RoleName == "developer":
            await self.config.guild(ctx.guild).ModRole.set(role.id)
            await ctx.send("The Developer role is now : {}".format(role.name))
        elif RoleName == "headmod":
            await self.config.guild(ctx.guild).headmod.set(role.id)
            await ctx.send("The Head Moderator role is now : {}".format(role.name))
        elif RoleName == "admin":
            await self.config.guild(ctx.guild).eventRole.set(role.id)
            await ctx.send("The Admin role is now : {}".format(role.name))
        elif RoleName == "moderator":
            await self.config.guild(ctx.guild).ModRole.set(role.id)
            await ctx.send("The Moderator role is now : {}".format(role.name))
        elif RoleName == "trialmoderator":
            await self.config.guild(ctx.guild).tmod.set(role.id)
            await ctx.send("The Trial Moderator role is now : {}".format(role.name))
        elif RoleName == "adminonleave":
            await self.config.guild(ctx.guild).adminOnLeave.set(role.id)
            await ctx.send("The Admin On Leave role is now : {}".format(role.name))
        elif RoleName == "modonleave":
            await self.config.guild(ctx.guild).ModOnLeave.set(role.id)
            await ctx.send("The Moderator On Leave role is now : {}".format(role.name))
        else:
            await ctx.send("No")
