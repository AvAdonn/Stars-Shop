import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from fluentogram import TranslatorRunner

from database.models import User

import database.requests as req

import keyboards.reply as kb 

router = Router(name='basic')
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def cmd_start(
    message: Message,
    session: AsyncSession,
    command: CommandObject,
    user_in_db: User | None,
    i18n: TranslatorRunner
):
    if user_in_db:
        text = i18n.get('welcome_back')
        await message.answer(
            text,
            parse_mode='HTML',
            reply_markup=kb.main
        )
        return
    
    if not message.from_user:
        return
    
    user_id = message.from_user.id
    
    args = command.args
    referral_id = None
    
    if args and args.isdigit():
        parsed_id = int(args)
        if parsed_id != user_id:
            referral_id = parsed_id
        else:
            logging.warning(f'Спроба самореферала від {user_id}')

    language = message.from_user.language_code or 'eu'
    
    await req.add_user(session, user_id, referral_id, language)
    text = i18n.get('account_created')
    await message.answer(
        text, 
        parse_mode='HTML',
        reply_markup=kb.main
    )
