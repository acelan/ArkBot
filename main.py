import os
import discord
import logging
from dotenv import load_dotenv
from arkbot import ArkBot

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
active_channels = os.getenv('ACTIVE_CHANNELS').split(',')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

log_format = '%(levelname)s %(asctime)s - %(message)s'
log_datefmt='%m/%d/%Y %I:%M:%S %p'
logger = logging.getLogger('ArkBot')
log_level = logging.DEBUG if os.getenv('LOG_LEVEL') == "DEBUG" else logging.INFO
logging.basicConfig(level=log_level, format=log_format, datefmt=log_datefmt)

client = ArkBot(intents=intents)
client.active_channels = active_channels

if __name__ == "__main__":
    client.run(discord_token)
