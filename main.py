from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
import handlers
from loguru import logger
from database import dbworker

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    dbworker.create_tables()
    bot.infinity_polling()
    logger.add('logs/logs_{time}.log', level='DEBUG', format="{time} {level} {message}", rotation="06:00",
               compression="zip")
    logger.debug('Error')
    logger.info('Information message')
    logger.warning('Warning')
