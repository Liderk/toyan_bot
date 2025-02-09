import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from init_bot import bot, dp, scheduler
from handlers.main import main_router
from telegram_app.config import settings
from telegram_app.handlers.admin import admin_router
from telegram_app.handlers.channel import channel_router
from telegram_app.handlers.info import info_router
from telegram_app.handlers.register import register_router
from telegram_app.handlers.utils import message_without_discussion
from telegram_app.orm.utils import get_admin_ids
from telegram_app.utils.constants import Commands


# from work_time.time_func import send_time_msg

async def set_commands():
    # Создаем список команд, которые будут доступны пользователям
    commands = [
        BotCommand(command=Commands.INFO, description='Информация'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup() -> None:
    await set_commands()
    await message_without_discussion(settings.CHAT_ID, settings.GROUP_ID, 'Уведомление без комментов')
    # await bot.delete_message(chat_id=settings.GROUP_ID, message_id=msg.message_id)
    # admin_ids = await get_admin_ids()
    # for admin_id in admin_ids:  # первый бот, для простоты использую for, далее переписать на рассылку
    #     await bot.send_message(chat_id=admin_id, text='Бот запущен!')


async def on_shutdown() -> None:
    admin_ids = await get_admin_ids()
    for admin_id in admin_ids:  # первый бот, для простоты использую for, далее переписать на рассылку
        await bot.send_message(chat_id=admin_id, text='Бот остановлен!')


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # dp.update.outer_middleware(UserCheckMiddleware())
    dp.include_routers(main_router, register_router, info_router, admin_router, channel_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
