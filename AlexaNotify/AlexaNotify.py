import logging
import requests 
from collections import namedtuple

import discord
from redbot.core import checks, Config, commands, bot, message


accessCode = namedtuple("accessCode", "text link")


class AlexaNotify(commands.Cog):
    """Send notifications to your Alexa device when pinged."""
    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.conf = Config.get_conf(self, force_registration=True)
        self.conf.register_user(accessCode="", Alexa_activated=False)
        self.conf.register_guild()
    

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        guild = message.guild
        if not guild or not message.mentions or message.author.bot:
            return
        if not message.channel.permissions_for(guild.me).send_messages:
            return

        for author in message.mentions:
            if (await self.conf.user(author).Alexa_activated == True) and (await self.conf.user(author).accessCode == True):
                message = message.clean_content
                res = requests.post('https://api.notifymyecho.com/v1/NotifyMe', data={"notification": message, "accessCode": accessCode}, port=443, method="POST")


    @commands.command(name="activatealexa")
    async def activate_alexa(self, ctx: commands.Context):
        """Enable messages mentioning you to be sent to your Alexa device as a notification"""
        if (await self.conf.user(ctx.author).accessCode == True):
            await self.conf.user(ctx.author).Alexa_activated.set(True)
            await ctx.send("Your notifications has been enabled!")

        else:
            the_prefix_used = ctx.prefix
            await ctx.send("Make sure you have an access code. Do {}setaccesscode in your DMS. ".format(the_prefix_used))

    @commands.command(name="deactivatealexa")
    async def deactivate_alexa(self, ctx: commands.Context):
        """Enable messages mentioning you to be sent to your Alexa device as a notification"""
        if (await self.conf.user(ctx.author).Alexa_activated == False):
            await self.conf.user(ctx.author).Alexa_activated.set(False)
            await ctx.send("Your notifications has been disabled!")

        else:
            await ctx.send("Your notifications is already disabled.")
       
       
    @commands.command(name="setaccesscode")
    async def set_access_code(self, ctx: commands.Context, *args):
        """
        What's this command for?
        To set your access code, necessary for Alexa Notifications to work.

        **Help** 
        --------
        Go to your Amazon Alexa app on your mobile device and add "NotifyMe" or "Notify Me" to your Alexa's list of skills. 
        - Your linked Amazon email will be sent an access code. 
        Use the access code for this.  

        **Usage**
        [Prefix]setaccesscode [access code]
        
        
        """
        guild = message.guild
        if (guild == True) or message.author.bot:
            await ctx.send("Please do this command again in your Direct Messages (DMS). For Privacy reasons.")
            return

        if len(args) != 1:
            await ctx.send("Please Go to your Amazon Alexa app on your mobile device and add 'NotifyMe' or 'Notify Me' to your Alexa's list of skills. Your linked Amazon email will be sent an access code. se the access code for this. ")
            return 
        await self.conf.user(ctx.author).accessCode.set(args[0])
        await ctx.send("Your access code has been set.")

    @commands.command(name="removeaccesscode")
    async def remove_access_code(self, ctx: commands.Context):
        """
        Remove your access code.
    
        """
        if (await self.conf.user(ctx.author).accessCode == True):
            await self.conf.user(ctx.author).accessCode.set("")
            await ctx.send("Your access code has been removed.")
        else:
            await ctx.send("You don't have an access code saved.")


       
