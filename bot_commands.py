import os
import sys
import subprocess
import discord

from fugle_integration import FugleIntegration

class BotCommands:
    def __init__(self):
        fugle_config_ini = os.getenv('FUGLE_CONFIG_INI')

        self.fugle = None
        if fugle_config_ini:
            self.fugle = FugleIntegration(fugle_config_ini)

    async def handle_command(self, msg):
        command = msg.content.split()[0][1:]
        if hasattr(self, command):
            await getattr(self, command)(msg)
        else:
            await msg.channel.send("Unknown command. Type !help for a list of commands.", reference=msg)

    async def hello(self, msg):
        await msg.channel.send(f'Hello, world!', reference=msg)

    async def help(self, msg):
        help_msg = """```
Available commands:
!help - This help message
!inventory [stock_id] - Check your stock inventory```"""
        await msg.channel.send(help_msg, reference=msg)

    async def inv(self, msg):
        await self.inventory(msg)

    async def inventory(self, msg):
        stock_id = ' '.join(msg.content.split()[1:])
        inv_msg = ""
        if self.fugle:
            inv_msg = await self.fugle.get_inventories(stock_id)
        await msg.channel.send(f"```\n{inv_msg}```", reference=msg)

