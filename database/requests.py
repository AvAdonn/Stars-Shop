import logging
import aiogram

from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from database.models import User

logger = logging.getLogger(__name__)

async def get_user(
    session: AsyncSession,
    tg_id: int
) -> User | None:
    if not tg_id:
        return None
    
    return await session.scalar(select(User).where(User.tg_id == tg_id))


async def add_user(
    session: AsyncSession,
    tg_id: int,
    referral_id: int | None,
    language_code: str
):
    new_user = insert(User).values(tg_id=tg_id, referral_id=referral_id, language=language_code)
    new_user = new_user.on_conflict_do_nothing(index_elements=['tg_id'])
    
    try:
        await session.execute(new_user)
        await session.commit()
        logger.info(f'Нового користувача створено: {tg_id}')
    except SQLAlchemyError as e:
        await session.rollback()
        logging.warning(f'Помилка при додаванні користувача {tg_id}: {e}', exc_info=True)