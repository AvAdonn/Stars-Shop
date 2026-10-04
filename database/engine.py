import os
import logging

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()
logger = logging.getLogger(__name__)

db_url = os.getenv('DB_URL')
if db_url is None:
    logger.critical('Відстунє посилання(Бази Даних)')
    raise ValueError('DB Url error!') 

engine = create_async_engine(
    db_url,
    echo=True
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)