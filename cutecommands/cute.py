import datetime
import time
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

class CuteComs(commands.Cog):
    """Really hecking cute commands for all bots"""

    def getActors(self, bot, killer, target):
        return {'id': bot.id, 'nick': bot.display_name, 'formatted': bot.mention}, {'id': killer.id, 'nick': killer.display_name, 'formatted': "<@{}>".format(killer.id)}, {'id': target.id, 'nick': target.display_name, 'formatted': target.mention}

    @commands.command()
    async def headpat(self, ctx, *, user: discord.Member):
        """Give headpats to your cat girls"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        if target['id'] == killer['id']:
            message1 = "{} tries to headpat themself, they start crying from loneliness... :broken_heart: ".format(killer['nick'])
            await ctx.send(message1)
        elif target['id'] == bot['id']:
            message1 = "{} attempts to headpat SCP-2306...".format(killer['nick'])
            message2 = "**`[SCP-2306]`** Thank you {}, you will be remembered".format(killer['nick'])
            message3 = "**`[Saving {} to the Do-Not-Kill Database...]`**".format(killer['nick'])
            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)
            time.sleep(1)
            await ctx.send(message3)
        else:
            message1 = "{} pats {} with lots of love :heart: :heart:".format(killer['nick'], target['nick'])
            await ctx.send(message1)


    @commands.command()
    async def vibecheck(self, ctx, *, user: discord.Member):
        """
        Unleash the vibecheck on someone
        """

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        special = random.randint(1,100)

        if target['id'] == killer['id']:
            message1 = "**`You cannot vibe check yourself.. That's just sad`**".format(killer['nick'])
            await ctx.send(message1)

        elif target['id'] == bot['id']:
            message1 = "**You cannot vibe check the bot**"

            await ctx.send(message1)

        else:
            message1 = "**`Checking the vibe for {}`**".format(target['nick'])
            if special > 50:
                message2 = "**`{} has passes the vibe check!`**".format(target['nick'])
            else:
                message2 = "**`{} has failed the vibe check...`**".format(target['nick'])

            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)

    @commands.command()
    @checks.mod_or_permissions(manage_roles=True)
    async def rawr(self, ctx: commands.Context):
        """Release your inner degenerate"""

        message1 = "Rawr x3 nuzzles how are you pounces on you you're so warm o3o notices you have a bulge o: someone's happy ;) nuzzles your necky wecky~ murr~ hehehe rubbies your bulgy wolgy you're so big :oooo rubbies more on your bulgy wolgy it doesn't stop growing ·///· kisses you and lickies your necky daddy likies (; nuzzles wuzzles I hope daddy really likes $: wiggles butt and squirms I want to see your big daddy meat~ wiggles butt I have a little itch o3o wags tail can you please get my itch~ puts paws on your chest nyea~ its a seven inch itch rubs your chest can you help me pwease squirms pwetty pwease sad face I need to be punished runs paws down your chest and bites lip like I need to be punished really good~ paws on your bulge as I lick my lips I'm getting thirsty. I can go for some milk unbuttons your pants as my eyes glow you smell so musky :v licks shaft mmmm~ so musky drools all over your cock your daddy meat I like fondles Mr. Fuzzy Balls hehe puts snout on balls and inhales deeply oh god im so hard~ licks balls punish me daddy~ nyea~ squirms more and wiggles butt I love your musky goodness bites lip please punish me licks lips nyea~ suckles on your tip so good licks pre of your cock salty goodness~ eyes role back and goes balls deep mmmm~ moans and suckles"

        await ctx.send(message1)

    @commands.command()
    @checks.mod_or_permissions(manage_messages=True)
    async def ahegao(self, ctx: commands.Context):
        """Make an ahegao face"""

        choose = random.randint(1,14)

        author = ctx.author
        embed = discord.Embed(
        title='Ahegao Picture Sent',
        description = '',
        colour = discord.Colour.gold()
        )

        if (choose == 1):
            embed.set_image(url="https://cdn.discordapp.com/attachments/695351641985253427/730286663221379092/hate.png")
        if (choose == 2):
            embed.set_image(url="https://cdn.discordapp.com/attachments/695351641985253427/730286664672346182/i.jpg")
        if (choose == 3):
            embed.set_image(url="https://cdn.discordapp.com/attachments/695351641985253427/730286665683304528/it.jpg")
        if (choose == 4):
            embed.set_image(url="https://pics.me.me/thumb_hentai-ahegao-face-nude-gallery-49318944.png")
        if (choose == 5):
            embed.set_image(url="https://cdn.discordapp.com/attachments/695351641985253427/730287729715314738/icon.png")
        if (choose == 6):
            embed.set_image(url="https://coubsecure-s.akamaihd.net/get/b13/p/coub/simple/cw_timeline_pic/f5e36be31bd/2e938fd268a6c0346e6e7/med_1568816291_image.jpg")
        if (choose == 7):
            embed.set_image(url="https://pm1.narvii.com/6872/27e4ea09f6bba4f3ea03ea2e3e71c08b5540d3a9r1-365-358v2_uhq.jpg")
        if (choose == 8):
            embed.set_image(url="https://art.pixilart.com/thumb/ceeb3581920739c.png")
        if (choose == 9):
            embed.set_image(url="https://www.uokpl.rs/fpng/d/103-1032905_ahegao-face-hd.png")
        if (choose == 10):
            embed.set_image(url="https://ctl.s6img.com/society6/img/yN3-2NcLOCL1OAFHok0w46vzndI/w_550/prints/~artwork/s6-original-art-uploads/society6/uploads/misc/97aa09b6a4ad404590a0dd257ad11b26/~~/ahegao-face2265338-prints.jpg")
        if (choose == 11):
            embed.set_image(url="https://assets.change.org/photos/9/sa/rk/YdSaRKQXtqjDOnP-800x450-noPad.jpg?1552523223")
        if (choose == 12):
            embed.set_image(url="https://www.meme-arsenal.com/memes/6a87775ed5b52ebac30ad48641a6b8aa.jpg")
        if (choose == 13):
            embed.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/47e23cb4-3295-4c94-adc3-76bf3b0a6aa5/dc77wc4-481fbd06-cc88-4d68-a9b7-c47c003bc0b4.jpg/v1/fill/w_1024,h_1024,q_75,strp/ahegao_face_by_zetsuwido_dc77wc4-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvNDdlMjNjYjQtMzI5NS00Yzk0LWFkYzMtNzZiZjNiMGE2YWE1XC9kYzc3d2M0LTQ4MWZiZDA2LWNjODgtNGQ2OC1hOWI3LWM0N2MwMDNiYzBiNC5qcGciLCJoZWlnaHQiOiI8PTEwMjQiLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS53YXRlcm1hcmsiXSwid21rIjp7InBhdGgiOiJcL3dtXC80N2UyM2NiNC0zMjk1LTRjOTQtYWRjMy03NmJmM2IwYTZhYTVcL3pldHN1d2lkby00LnBuZyIsIm9wYWNpdHkiOjk1LCJwcm9wb3J0aW9ucyI6MC40NSwiZ3Jhdml0eSI6ImNlbnRlciJ9fQ.yVtaQ6cj7rKY0_IsBbERxMW-4cFPoSojjyZbJI95WpA")
        if (choose == 14):
            embed.set_image(url="https://www.memesmonkey.com/images/memesmonkey/29/297343f45e6f8553a9bab1c5f6226865.jpeg")
        await ctx.send(embed=embed)
