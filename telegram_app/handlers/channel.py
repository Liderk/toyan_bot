import logging

from aiogram import Router, F
from aiogram.types import Message

from telegram_app.config import settings
from telegram_app.filters.access_group import AccessGroupFilter
from telegram_app.handlers.info import get_nearest_game_data, get_nearest_event_data, \
    get_data_for_games_by_current_month, get_data_for_events_by_current_month
from telegram_app.utils.constants import EventsInfo

logger = logging.getLogger(__name__)

channel_router = Router()
channel_router.message.filter(
    AccessGroupFilter(chat_type=["group", "supergroup"], allowed_group_chats=[settings.CHAT_ID, settings.GROUP_ID]),
)

bot_answer_mapping = {
    EventsInfo.nearest_game.lower(): get_nearest_game_data,
    EventsInfo.nearest_event.lower(): get_nearest_event_data,
    EventsInfo.month_games.lower(): get_data_for_games_by_current_month,
    EventsInfo.month_event.lower(): get_data_for_events_by_current_month,
}


@channel_router.message(F.text.startswith(settings.BOT_NAME))
async def channel_post_handler(message: Message):
    user_msg = message.text.replace(f'{settings.BOT_NAME} ', '').lower()
    logger.info(f"Chat ID: {message.chat.id}, Thread ID: {message.message_thread_id}")
    logger.info(f"Chat ID from settings: {settings.CHAT_ID}, Thread ID: {message.message_thread_id}")
    if user_msg not in bot_answer_mapping:
        await message.answer('Я не понимаю тебя, кожанный мешок!!', reply_to_message_id=message.message_id)
        return

    data = await bot_answer_mapping[user_msg]()
    msg_text = f'{data}\n\n' \
               f'Что то еще, собака сутулая?'
    await message.answer(msg_text, reply_to_message_id=message.message_id)
