import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import settings
from init_bot import bot, dp, scheduler
from handlers.main import main_router
from handlers.admin import admin_router
from handlers.channel import channel_router
from handlers.group import group_router
from handlers.info import info_router
from handlers.register import register_router
from orm.utils import get_admin_ids
from scheduler.utils import send_notifications
from utils.constants import Commands


async def set_commands():
    # Создаем список команд, которые будут доступны пользователям
    commands = [
        BotCommand(command=Commands.MENU, description='Меню'),

    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    pass


async def on_startup() -> None:
    await set_commands()
    admin_ids = await get_admin_ids()
    for admin_id in admin_ids:  # первый бот, для простоты использую for, далее переписать на рассылку
        await bot.send_message(chat_id=admin_id, text='Бот запущен!')


async def on_shutdown() -> None:
    admin_ids = await get_admin_ids()
    for admin_id in admin_ids:  # первый бот, для простоты использую for, далее переписать на рассылку
        await bot.send_message(chat_id=admin_id, text='Бот остановлен!')


async def main():

    scheduler.add_job(send_notifications, 'cron', hour=settings.START_HOUR, minute=settings.START_MINUTES)
    scheduler.start()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(main_router, register_router, info_router, admin_router, channel_router, group_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
