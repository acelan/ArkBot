import os
import sys
import subprocess
import discord
import logging

from esun_integration import EsunIntegration
from stock_tools import StockTools

logger = logging.getLogger('ArkBot')

class BotCommands:
    def __init__(self):
        esun_config_ini = os.getenv('ESUN_CONFIG_INI')

        self.esun = None
        if esun_config_ini:
            self.esun = EsunIntegration(esun_config_ini)

        self.stock_tools = StockTools()

    def _normalize_symbol(self, symbol: str) -> str:
        if symbol.isdigit():
            return f"{symbol}.TW"
        return symbol

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
!inventory [stock_id] - Check your stock inventory
!stock [symbol] - Quick stock info (e.g., !stock AAPL or !stock 2330.TW)
!price [symbol] [period] - Price history (period: 1d, 1mo, 3mo, 1y, etc.)```"""
        await msg.channel.send(help_msg, reference=msg)

    async def inv(self, msg):
        await self.inventory(msg)

    async def inventory(self, msg):
        stock_id = ' '.join(msg.content.split()[1:])
        inv_msg = ""
        if self.esun:
            inv_msg = await self.esun.get_inventories(stock_id)
        await msg.channel.send(f"```\n{inv_msg}```", reference=msg)

    async def stock(self, msg):
        parts = msg.content.split()
        if len(parts) < 2:
            await msg.channel.send("請提供股票代號，例如: !stock AAPL 或 !stock 2330", reference=msg)
            return

        symbol = self._normalize_symbol(parts[1])
        logger.debug(f"!stock command: user={msg.author.name}, symbol={symbol}")

        try:
            info = self.stock_tools.get_stock_info(symbol)
            logger.debug(f"!stock result for {symbol}: {len(info)} characters")
            await msg.channel.send(f"```\n{info}```", reference=msg)
        except Exception as e:
            error_msg = f"獲取股票 {symbol} 資訊時發生錯誤: {str(e)}"
            logger.error(f"!stock command failed for {symbol}: {e}", exc_info=True)
            await msg.channel.send(f"```\n{error_msg}```", reference=msg)

    async def price(self, msg):
        parts = msg.content.split()
        if len(parts) < 2:
            await msg.channel.send("請提供股票代號，例如: !price AAPL 1mo 或 !price 2330 3mo", reference=msg)
            return

        symbol = self._normalize_symbol(parts[1])
        period = parts[2] if len(parts) > 2 else "1mo"
        logger.debug(f"!price command: user={msg.author.name}, symbol={symbol}, period={period}")

        try:
            history = self.stock_tools.get_price_history(symbol, period)
            logger.debug(f"!price result for {symbol}: {len(history)} characters")
            await msg.channel.send(f"```\n{history}```", reference=msg)
        except Exception as e:
            error_msg = f"獲取股票 {symbol} 價格歷史時發生錯誤: {str(e)}"
            logger.error(f"!price command failed for {symbol}: {e}", exc_info=True)
            await msg.channel.send(f"```\n{error_msg}```", reference=msg)

