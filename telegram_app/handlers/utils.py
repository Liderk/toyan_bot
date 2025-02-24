import asyncio
import logging

from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..init_bot import bot
from ..keyboards.admin import create_admin_kb
from ..utils.constants import MsgAction

logger = logging.getLogger(__file__)


class UniversalMessageSender:
    def __init__(self, text: str = None, photo_id: str = None, document_id: str = None,
                 video_id: str = None, audio_id: str = None, voice_id: str = None,
                 caption: str = None, content_type: str = None):
        self.text: (str, None) = text
        self.photo_id: (str, None) = photo_id
        self.document_id: (str, None) = document_id
        self.video_id: (str, None) = video_id
        self.audio_id: (str, None) = audio_id
        self.voice_id: (str, None) = voice_id
        self.caption: (str, None) = caption
        self.content_type: (str, None) = content_type

    @classmethod
    def init_from_message(cls, message: Message):
        return cls(
            text=message.text,
            photo_id=message.photo[-1].file_id if message.photo else None,
            document_id=message.document.file_id if message.document else None,
            video_id=message.video.file_id if message.video else None,
            audio_id=message.audio.file_id if message.audio else None,
            voice_id=message.voice.file_id if message.voice else None,
            caption=message.caption,
            content_type=message.content_type,
        )

    async def send_message(self, chat_id: int) -> Message:
        if self.content_type == ContentType.TEXT:
            return await bot.send_message(chat_id=chat_id, text=self.text)
        elif self.content_type == ContentType.PHOTO:
            return await bot.send_photo(chat_id=chat_id, photo=self.photo_id, caption=self.caption)
        elif self.content_type == ContentType.DOCUMENT:
            return await bot.send_document(chat_id=chat_id, document=self.document_id, caption=self.caption)
        elif self.content_type == ContentType.VIDEO:
            return await bot.send_video(chat_id=chat_id, video=self.video_id, caption=self.caption)
        elif self.content_type == ContentType.AUDIO:
            return await bot.send_audio(chat_id=chat_id, audio=self.audio_id, caption=self.caption)
        elif self.content_type == ContentType.VOICE:
            return await bot.send_voice(chat_id=chat_id, voice=self.voice_id, caption=self.caption)

    async def broadcast_message(self, users_ids: list[int]) -> tuple[int, int]:
        good_send: int = 0
        bad_send: int = 0
        # бот для закрытого, узкоспециализированного сообщества, на 100 человек максимум,
        # поэтому не строим сложные конструкции и используем for
        for chat_id in users_ids:
            try:
                await self.send_message(chat_id)
                good_send += 1
            except Exception as e:
                logger.error(e)
                bad_send += 1
            finally:
                await asyncio.sleep(1)
        return good_send, bad_send

    async def message_with_discussion(self, channel_id: int) -> Message:
        return await self.send_message(chat_id=channel_id)

    async def message_without_discussion(self, channel_id: int, group_id: int) -> Message:
        msg = await self.send_message(chat_id=channel_id)
        InMemoryMessageIdStorage.add_msg(msg.message_id, MsgAction.delete)

        return msg


async def admin_universe_broadcast(message: Message, state: FSMContext, user_ids: list[int]):
    await message.answer(f'Начинаю рассылку на {len(user_ids)} пользователей.')

    sender = UniversalMessageSender.init_from_message(message)
    good_send, bad_send = await sender.broadcast_message(users_ids=user_ids)

    await state.clear()
    await message.answer(f'Рассылка завершена. Сообщение получило <b>{good_send}</b>, '
                         f'НЕ получило <b>{bad_send}</b> пользователей.', reply_markup=create_admin_kb())


async def simple_universe_broadcast(message: Message, user_ids: list[int]):
    sender = UniversalMessageSender.init_from_message(message)
    await sender.broadcast_message(users_ids=user_ids)
    await message.answer('Ваше сообщение отправлено. Возможно его даже прочитают!')


class InMemoryMessageIdStorage:
    message_id = {}

    @classmethod
    def add_msg(cls, msg_id: int, action: str):
        cls.message_id[msg_id] = action

    @classmethod
    def delete_msg(cls, msg_id: int):
        del cls.message_id[msg_id]

    @classmethod
    def check_msg(cls, msg_id: int):
        return cls.message_id.get(msg_id)
