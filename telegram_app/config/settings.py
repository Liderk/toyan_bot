import os
from pathlib import Path

from decouple import AutoConfig

if os.environ.get('READ_FROM_ENV') == 'True':
    env_path = Path(__file__).parent.parent / '.env'
    env_config = AutoConfig(env_path)
else:
    env_config = AutoConfig()

BOT_TOKEN = env_config('TOKEN')

DATA_BASE_DIR = Path(env_config('DATA_BASE_DIR', cast=str))
DATA_BASE_NAME = env_config('DATA_BASE_NAME', default='airsoft_bot.sqlite3', cast=str)

DEBUG = env_config('DEBUG', default=False, cast=bool)
CHAT_ID = env_config('CHAT_ID', cast=int)
GROUP_ID = env_config('GROUP_ID', cast=int)
BOT_NAME = env_config('BOT_NAME', cast=str)

# db settings
POSTGRES_DB = env_config('POSTGRES_DB', cast=str)
POSTGRES_USER = env_config('POSTGRES_USER', cast=str)
POSTGRES_USER_PASSWORD = env_config('POSTGRES_USER_PASSWORD', cast=str)
POSTGRES_HOST = env_config('POSTGRES_PASSWORD', cast=str, default='192.168.1.90')
