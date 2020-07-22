from .special import SpecialTools

def setup(bot):
    cog = SpecialTools(bot)
    bot.add_cog(cog)
