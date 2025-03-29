import os
from pathlib import Path

from decouple import AutoConfig

if os.environ.get('READ_FROM_ENV') == 'True':
    env_path = Path(__file__).parent.parent / '.env'
    env_config = AutoConfig(env_path)
else:
    env_config = AutoConfig()

BOT_TOKEN = env_config('TOKEN')

DEBUG = env_config('DEBUG', default=False, cast=bool)
CHAT_ID = env_config('CHAT_ID', cast=int)
GROUP_ID = env_config('GROUP_ID', cast=int)
BOT_NAME = env_config('BOT_NAME', cast=str)
PROJECT_TZ = env_config('PROJECT_TZ', cast=str, default='Asia/Novosibirsk')

# db settings
POSTGRES_DB = env_config('POSTGRES_DB', cast=str, default='postgres')
POSTGRES_USER = env_config('POSTGRES_USER', cast=str, default='postgres')
POSTGRES_PASSWORD = env_config('POSTGRES_PASSWORD', cast=str, default='postgres')
POSTGRES_HOST = env_config('POSTGRES_HOST', cast=str, default='192.168.1.90')

# media dir
MEDIA_ROOT = env_config('MEDIA_ROOT', cast=str, default='/var/www/media')

# apscheduler settings
TIMEZONE = env_config('TIMEZONE', cast=str, default='Asia/Novosibirsk')
START_HOUR = env_config('START_HOUR', cast=int, default=10)
START_MINUTES = env_config('START_MINUTES', cast=int, default=0)
