from .AlexaNotify import AlexaNotify


def setup(bot):
    bot.add_cog(AlexaNotify(bot))