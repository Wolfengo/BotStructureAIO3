from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram import types

from bot_script.bot import dp


class States(StatesGroup):
    name = State()
    album_middleware = State()

