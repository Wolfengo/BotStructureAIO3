from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline():
    button_one = InlineKeyboardButton(text='test1', callback_data='test1')
    button_two = InlineKeyboardButton(text='test2', callback_data='test2')
    keyboard = InlineKeyboardBuilder()
    keyboard.add(button_one, button_two)
    return keyboard.as_markup()

