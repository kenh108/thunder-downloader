import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from .config import Config

class TelegramNotifier:
    def __init__(self):
        self.bot = None
        self.logger = logging.getLogger(__name__)
        
        if Config.TELEGRAM_ENABLED and Config.TELEGRAM_BOT_TOKEN:
            try:
                self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
                self.logger.info("Telegram bot initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Telegram bot: {e}")

    async def send_message_async(self, message):
        """Send message to Telegram (async)"""
        if not self.bot or not Config.TELEGRAM_ENABLED:
            return False
            
        try:
            await self.bot.send_message(
                chat_id=Config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode='HTML'
            )
            self.logger.info("Telegram message sent")
            return True
        except TelegramError as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False

    def send_message(self, message):
        """Sync wrapper for async message sending"""
        if not self.bot or not Config.TELEGRAM_ENABLED:
            return False
        try:
            asyncio.run(self.send_message_async(message))
            return True
        except Exception as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False

    def game_downloaded(self, game_name):
        """Notify when a game is downloaded"""
        message = (
            f"<b>New {Config.TEAM_NAME} Game Downloaded!</b>\n\n"
            f"{game_name}\n\n"
            f"Ready to watch!"
        )
        return self.send_message(message)
