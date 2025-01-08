import asyncio
import logging

from aiogram.enums import ContentType

from telegram_app.init_bot import bot

logger = logging.getLogger(__file__)


async def broadcast_message(users_ids: list, text: str = None, photo_id: int = None, document_id: int = None,
                            video_id: int = None, audio_id: int = None, voice_id: int = None,
                            caption: str = None, content_type: str = None):
    good_send = 0
    bad_send = 0
    # бот для закрытого, узкоспециализированного сообщества, на 100 человек максимум,
    # поэтому не строим сложные конструкции и используем for
    for chat_id in users_ids:
        try:
            if content_type == ContentType.TEXT:
                await bot.send_message(chat_id=chat_id, text=text)
            elif content_type == ContentType.PHOTO:
                await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=caption)
            elif content_type == ContentType.DOCUMENT:
                await bot.send_document(chat_id=chat_id, document=document_id, caption=caption)
            elif content_type == ContentType.VIDEO:
                await bot.send_video(chat_id=chat_id, video=video_id, caption=caption)
            elif content_type == ContentType.AUDIO:
                await bot.send_audio(chat_id=chat_id, audio=audio_id, caption=caption)
            elif content_type == ContentType.VOICE:
                await bot.send_voice(chat_id=chat_id, voice=voice_id, caption=caption)
            good_send += 1
        except Exception as e:
            logger.error(e)
            bad_send += 1
        finally:
            await asyncio.sleep(1)
    return good_send, bad_send
