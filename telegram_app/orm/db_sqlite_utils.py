from telegram_app.config.settings import DATA_BASE_DIR, DATA_BASE_NAME, DEBUG

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

db_path = DATA_BASE_DIR / DATA_BASE_NAME

async_engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}', echo=DEBUG)

async_session_factory = async_sessionmaker(async_engine)
