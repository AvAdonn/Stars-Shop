import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from utils.logger import setup_logger
from middleware.base import DBMiddleware, AuthMiddleware
from utils.i18n import create_translator_hub
from middleware.md_i18n import TranslatorRunnerMiddleware


setup_logger()
logger = logging.getLogger(__name__)
logger.info('Логування завершено. Підготовка запуску...')

async def starting() -> None:
    logger.info('Старт бота завершено.')
    
async def stopped() -> None:
    logger.info('Бота зупинено.')

async def main() -> None:
    load_dotenv()
    token = os.getenv('TOKEN')
    if token is None:
        logger.critical('Відсутній токен бота!')
        raise ValueError('Token error!')
        
    bot = Bot(token)
    dp = Dispatcher()
    try:
        dp.update.outer_middleware(DBMiddleware())
        
        translator_hub = create_translator_hub()
        dp.message.middleware(TranslatorRunnerMiddleware(hub=translator_hub))
        dp.callback_query.middleware(TranslatorRunnerMiddleware(hub=translator_hub))
        
        dp.message.middleware(AuthMiddleware())
        dp.callback_query.middleware(AuthMiddleware())
        
        dp.startup.register(starting)
        dp.shutdown.register(stopped)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(
            f'Критична помилка під час запуску: {e}', 
            exc_info=True
        )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Зупинено власноруч.')