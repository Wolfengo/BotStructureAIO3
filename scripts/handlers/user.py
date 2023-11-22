from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage

from scripts.bot import bot, dp, storage
from scripts.handlers.messager import SenderMessage
from scripts.keyboards.user_inline_button import inline
from scripts.middelewares.throttling import ThrottlingMiddleware
from scripts.states.user import States


async def func_to_register(message: types.Message):
    await message.answer('Func', reply_markup=await inline())


async def test(message: types.Message, state: FSMContext):
    send = SenderMessage(message)
    await send.update_message('Новое сообщение', await inline())
    await send.notification('NOTIFICATION')
    await state.set_state(States.name)
    await state.update_data(id=message.message.message_id)
    # response_text = str(message)
    # max_length = 4096
    #
    # # Splitting the message into parts if it's too long
    # while response_text:
    #     text_chunk = response_text[:max_length]
    #     response_text = response_text[max_length:]
    #
    #     await bot(SendMessage(chat_id=message.from_user.id, text=text_chunk))


async def test2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text, user=message.from_user.id)
    data = await state.get_data()
    send = SenderMessage(message, data['id'])
    await send.answer_update('Спасибо!', 'Кнопки удалены после ввода текста')
    await state.clear()


async def handler_registration():
    dp.message.middleware.register(ThrottlingMiddleware(storage=storage))
    dp.message.register(func_to_register, Command("start"))
    dp.callback_query.register(test, F.data.startswith('test1'))
    dp.message.register(test2, States.name)
