import discord
import random
import time
from redbot.core import commands
from redbot.core import bank, commands

class Killing(commands.Cog):
    """https://i.imgflip.com/3unemz.jpg"""

    def getActors(self, bot, killer, target):
        return {'id': bot.id, 'nick': bot.display_name, 'formatted': bot.mention}, {'id': killer.id, 'nick': killer.display_name, 'formatted': "<@{}>".format(killer.id)}, {'id': target.id, 'nick': target.display_name, 'formatted': target.mention}

    @commands.command()
    async def slap(self, ctx, *, user: discord.Member):
        """Slap a user!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(1,100)

        if target['id'] == bot['id']:

            if diceroll < 95:
                message1 = "{} attempts to slap {} but misses".format(killer['nick'], bot['nick'])
                message2 = "{} the slaps {} out of the universe with no effort".format(bot['nick'], killer['nick'])
            else:
                message1 = "{} attempts to slap {}...".format(killer['nick'], bot['nick'])
                message2 = "{} slaps a flashdrive? Why would they ever do that?".format(killer['nick'])

            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)

        elif target['id'] == killer['id']:
            message1 = "{} has the sudden urge to slap themself...".format(killer['nick'])
            message2 = "So they proceed to do so, for seemingly no reason"

            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)

        else:
            if diceroll > 99:
                message1 = "{} reaches over to slap {}, but misses somehow hitting {}'s cheeks instead... :blush: :heart: ".format(killer['nick'], target['nick'], target['nick'])
                message2 = "{} responds with No Homo".format(killer['nick'])
            elif diceroll > 98:
                message1 = "{} raises their hand to slap {}...".format(killer['nick'], target['nick'])
                message2 = "{} slaps {} at the speed of sound".format(killer['nick'], target['nick'])
            elif diceroll > 50:
                message1 = "{} raises their hand to slap {}...".format(killer['nick'], target['nick'])
                message2 = "{} slaps {} harder than ever, leaving a red mark".format(killer['nick'], target['nick'])
            elif diceroll > 10:
                message1 = "{} raises their hand to slap {}...".format(killer['nick'], target['nick'])
                message2 = "{} lightly slaps {} on the cheek".format(killer['nick'], target['nick'])
            else:
                message1 = "{} raises their hand to slap {}...".format(killer['nick'], target['nick'])
                message2 = "And gives {} a romantic spanking... :heart: :heart:".format(target['nick'])

            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)

    @commands.command()
    async def punch(self, ctx, *, user: discord.Member):
        """Punch a user"""

        bot, killer, target = self.getActors(
                ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(1,100)

        if target['id'] == bot['id']:  # tryng to punch the bot, eh?

            message1 = "{} waves their fists at {}... 🤖 ✊🧐".format(
            killer['nick'], bot['nick'])
            message2 = "but {} casts Igni on {}! 🤖 🔥😫🔥".format(
            bot['nick'], killer['formatted'])

            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)

        elif killer['id'] == target['id']:  # wants to punch themselves

            message1 = "{} looks at their own fist... 😒✊".format(
            killer['nick'])

            if diceroll > 89:
                message2 = "and bashes their head through the nearest wall! 😫▮💥"
            elif diceroll > 69:
                message2 = "and bashes their head against it until its broken! 😡💫🤟"
            elif diceroll > 10:
                message2 = "and repeatedly hits themselves with their pathetic little hands 🤜😣🤛"
            else:
                message2 = "tries to throw a punch, but misses and breaks their ankle! ☹️🦵"
            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)

        else:

            message1 = "{} raises their fist and throws it at {}...".format(killer['nick'], target['nick'])

            if diceroll > 95:
                message2 = "hitting them directly in the heart killing them instantly! 💥🤯💥"
            elif diceroll > 90:
                message2 = "hitting them in the face, knocking them out! 🤜💥😣"
            elif diceroll > 80:
                message2 = "knocking down {} onto the concrete pavement".format(target['nick'])
            elif diceroll > 50:
                message2 = "hitting them in the ribcage breaking every bone!"
            elif diceroll > 45:
                message2 = "hitting them in the pelvis! {} cries out in pain 😫".format(target['nick'])
            elif diceroll > 30:
                message2 = "hitting them in the face and loosing a tooth!"
            elif diceroll > 10:
                message2 = "hitting them in the face!"
            await ctx.send(message1)
            time.sleep(1)
            await ctx.send(message2)

    @commands.command()
    async def stab(self, ctx, *, user: discord.Member):
        """Turn a user into shish kebab!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # tryng to shoot the bot, eh?

            message1 = "{} raises their dagger at Geraldo... 😠🔪 🤖".format(
                killer['nick'])
            message2 = "but Geraldo teleports behind {} and strikes! 😵💫 ⚔️🤖 {}".format(
                killer['formatted'], '`"Nothing personell, kid"`')

        elif killer['id'] == target['id']:  # wants to slap themselves

            message1 = "{} holds a knife against their abdomen...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and cuts their own head off! How is that even possible!? 🙃👕"
            elif diceroll > 10:
                message2 = "and commits sudoku! 🔪😵"
            else:
                message2 = "and accidentally cuts their finger on a hentai magazine! 📕😫 {}-no skebe!".format(
                    target['nick'])

        else:  # wants to slap another user

            message1 = "Ever since Julius Caesar took over Rome, you can't stab anyone"

        await ctx.send(message1)


    @commands.command()
    async def shoot(self, ctx, *, user: discord.Member):
        """Shoot another user (or yourself) dead!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if (target['id'] == bot['id']):  # tryng to shoot the bot, eh?

            message1 = "{} aims their gun, pulls the trigger...".format(
                killer['nick'])
            message2 = "but {} shot first! 😵 💥🔫🤖".format(bot['nick'])

        elif killer['id'] == target['id']:  # wants to kill themselves

            message1 = "{} holds a gun to their head, pulls the trigger...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and explodes! Boom! Splat! What a mess! 💥😵💥"
            elif diceroll > 30:
                message2 = "and commits sudoku! 💥😵🔫"
            elif diceroll > 20:
                message2 = "and KYSed themselves! 💥😵🔫"
            elif diceroll > 10:
                message2 = "and somehow didn't miss! At least this idiot is good for something! 💥😵🔫"
            else:
                message2 = "and misses! What an idiot! Should've aimed at the temple! 💥🔫😯"


        else:  # wants to kill other user

            message1 = "{} aims their gun, pulls the trigger...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and {} explodes into a red, gut-ridden, eyeball-strewn paste. Fun!!! 💥🔴 🔫🤠".format(
                    target['formatted'])
            elif diceroll > 75:
                message2 = "and shoots {} in the head! Bang! 💥😵 🔫😆".format(
                    target['formatted'])
            elif diceroll > 10:
                message2 = "and shoots {} dead! 😱 💥🔫😁".format(
                    target['formatted'])
            elif diceroll > 5:
                message2 = "and misses {}! Doh! 😗 💨🔫😣".format(
                    target['formatted'])
            else:
                message2 = "and shoots themselves instead of {}! LOL! 🤣 💥😵🔫".format(
                    target['formatted'])

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    @commands.command()
    async def love(self, ctx, *, user: discord.Member):
        """Show some affection for once!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # love the bot
            message = "{} loves 2306!".format(killer['nick'])
        elif killer['id'] == target['id']:  # loves themselves
            message = "{} loves themselves, because nobody else does 😕".format(
                killer['nick'])
        else:
            if diceroll > 99:
                message = "Three cummie, four cummie, five cummie, six, {} loves {} but they also love dicks 💦".format(
                    killer['formatted'], target['formatted'])
            elif diceroll > 60:
                message = "{} wants to spoon {} aww... how adorable😍 😊".format(killer['nick'], target['nick'])
            elif diceroll > 10:
                message = "{} loves {} aww... 😍 😊".format(
                    killer['formatted'], target['formatted'])
            else:
                message = "{} loves {}, but not in return 😭 😑".format(
                    killer['formatted'], target['formatted'])

        await ctx.send(message)


    @commands.command()
    async def sex(self, ctx, *, user: discord.Member):
        """Bang a User"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # love the bot
            message = "You can't mount a USB".format(killer['nick'])
        elif killer['id'] == target['id']:  # loves themselves
            message = "{} loves themselves, because nobody else does 😕".format(
                killer['nick'])
        else:
            if diceroll > 99:
                message = "{} gets ontop of {}'s chest and then some NSFW stuff happens'".format(
                    killer['formatted'], target['formatted'])
            elif diceroll > 60:
                message = "{} pulls out their pickle, and compares it to {}".format(killer['nick'], target['nick'])
            elif diceroll > 10:
                message = "{} bangs {} 💦💦".format(
                    killer['formatted'], target['formatted'])
            else:
                message = "{} isn't in the mood for sexy time".format(
                    target['formatted'])

        await ctx.send(message)
