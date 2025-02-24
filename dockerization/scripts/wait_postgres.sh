#!/bin/sh

set -e

cmd="$@"

postgres_ready() {
python << END
import sys
import asyncio
import os
from psycopg import AsyncConnection

async def connect_to_db():
    try:
        POSTGRES_USER = os.getenv('POSTGRES_USER')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        POSTGRES_PORT = os.getenv('POSTGRES_PORT', default='5432')
        POSTGRES_DB = os.getenv('POSTGRES_DB')

        # Формируем DSN из переменных окружения
        dsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

        # Подключение к базе данных
        conn = await AsyncConnection.connect(dsn)
        await conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

async def main():
    if await connect_to_db():
        sys.exit(0)
    else:
        sys.exit(-1)

# Запуск асинхронного кода
asyncio.run(main())
END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

exec $cmd
