import os
import discord
import asyncio
import logging
from arkbrain import ArkBrain
from bot_commands import BotCommands

log_format = '%(levelname)s %(asctime)s - %(message)s'
log_datefmt='%m/%d/%Y %I:%M:%S %p'
logger = logging.getLogger('ArkBot')
log_level = logging.DEBUG if os.getenv('LOG_LEVEL') == "DEBUG" else logging.INFO
logging.basicConfig(level=log_level, format=log_format, datefmt=log_datefmt)

class ArkBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.brain = ArkBrain()
        self.my_commands = BotCommands()

    async def on_ready(self):
        logger.info(f'Logged on as {self.user}!')
        logger.info('------')

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if str(msg.channel.id) not in self.active_channels:
            logger.warning(f"Message from {msg.author} which is not in active channels({msg.channel.id}): {msg.content}")
            if msg.author.name != "acelan.":
                return

        if msg.content.startswith('!'):
            if msg.content == "!kick":
                await msg.channel.send("唉呀，我跳進來啦。怎樣？我又跳出去了，唉呀，我又跳進來啦！打我啊笨蛋。", reference=msg)
                await super().close()
            else:
                await self.my_commands.handle_command(msg)
                return

        if not self.user.mentioned_in(msg):
            return

        user_input = msg.content.replace(f'<@{self.user.id}>', '').strip()

        reference_id = msg.id
        ref_msg = msg
        while ref_msg.reference:
            reference_id = ref_msg.reference.message_id
            ref_msg = await ref_msg.channel.fetch_message(reference_id)

        async def thinking(message, timeout=999):
            try:
                await message.add_reaction('🤔')
                async with message.channel.typing():
                    await asyncio.sleep(timeout)
            except Exception:
                pass
            finally:
                await message.remove_reaction('🤔', message.guild.me)

        logger.debug(f"on_message() - {reference_id}: {msg.author.name}: {user_input}")
        task = asyncio.create_task(thinking(msg))
        response = await self.brain.thinking(reference_id, user_input)
        task.cancel()
        await msg.reply(response)
