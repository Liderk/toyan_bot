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

