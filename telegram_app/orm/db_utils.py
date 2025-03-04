from sqlalchemy import URL

from config.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB, DEBUG
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

url_object = URL.create(
    'postgresql+psycopg',
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
)


async_engine = create_async_engine(url_object, echo=DEBUG)

async_session_factory = async_sessionmaker(async_engine)
