import asyncio
from ctypes import Union

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import SendMessage, EditMessageText

from bot_script.bot import bot


class SenderMessage:
    def __init__(self, message, old_message_id=None):
        self.message = message
        self.user_in = message.from_user.id
        self.old_message_id = old_message_id
        try:
            self.message_id = message.message_id
            self.text_in = message.text
        except AttributeError:
            self.message_id = message.message.message_id
            self.text_in = message.message.text
        except Exception as e:
            print(f"Произошла ошибка получения данных message_id и text: {e}")

    async def new_message(self, text, button=None):
        await bot(SendMessage(chat_id=self.user_in, text=text, reply_markup=button))

    async def new_message_other_user(self, text, button=None):
        await bot(SendMessage(chat_id=self.user_in, text=text, reply_markup=button))

    async def update_message(self, text=None, button=None):
        try:
            await bot(EditMessageText(
                chat_id=self.user_in,
                message_id=self.message_id,
                text=self.text_in if text is None else text,
                reply_markup=button))
        except TelegramBadRequest:
            return

    async def answer_update(self, text_out, text_in=None, button_in=None, button_out=None):
        await bot(EditMessageText(
            chat_id=self.user_in,
            message_id=self.message_id if self.old_message_id is None else self.old_message_id,
            text=self.text_in if text_in is None else text_in,
            reply_markup=button_in))
        await bot(SendMessage(chat_id=self.user_in, text=text_out, reply_markup=button_out))

    async def notification(self, text):
        await self.message.answer(text)


