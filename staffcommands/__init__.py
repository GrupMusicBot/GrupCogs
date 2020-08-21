from .staffcom import staffCom


def setup(bot):
    cog = staffCom(bot)
    bot.add_cog(cog)
