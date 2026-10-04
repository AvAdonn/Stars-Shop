from abc import abstractmethod
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorHub

class TranslatorRunnerMiddleware(BaseMiddleware):
    def __init__(self, hub: TranslatorHub):
        super().__init__()
        self.hub = hub
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]],Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any] 
    ) -> Any:
        user_in_db = data.get('user_in_db')
        if user_in_db and user_in_db.language:
            language_code = user_in_db.language
        else:
            user = data.get('event_from_user')
            language_code = user.language_code if user else 'uk'
        
        i18n_translator = self.hub.get_translator_by_locale(language_code)
        
        data['i18n'] = i18n_translator
        
        return await handler(event, data)