import logging
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Awaitable, Dict, Any

from fluentogram import TranslatorRunner

from database.engine import async_session
from database.requests import get_user

logger = logging.getLogger(__name__)

class DBMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]    
    ) -> Any:
        
        async with async_session() as session:
            data['session'] = session
        
            tg_user = data.get('event_from_user')
            if tg_user:            
                user = await get_user(session, tg_user.id)
                data['user_in_db'] = user
            else:
                data['user_in_db'] = None
            
            return await handler(event, data)            

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]  
    ) -> Any:
        user = data['user_in_db']
        
        if user is None:
            if isinstance(event, Message) and event.text and event.text.startswith('/start'):
                return await handler(event, data)
            
            i18n: TranslatorRunner | None = data.get('i18n')
            
            if isinstance(event, (Message, CallbackQuery)) and i18n:
                text = i18n.get('reg_req')
                await event.answer(text)
            else:
                logger.error('Помилка авторизації: відсутній i18n/невідомий тип події')
            
            return
        
        return await handler(event, data)