from aiogram import Bot, Dispatcher
import asyncio

from aiogram.fsm import middleware
from aiogram.fsm.storage.redis import RedisStorage

from scripts.config import BOT_TOKEN
from scripts.middelewares.cortage import AlbumMiddleware
from scripts.services.sql import Changer, Database

from scripts.config import db_host, db_port, db_password_postgres, db_name, db_user, db_password

bot = Bot(BOT_TOKEN)
storage = RedisStorage.from_url('redis://localhost:6379/0')
dp = Dispatcher()
dp.message.middleware(AlbumMiddleware())


async def main():
    from handlers.user import dp, handler_registration
    Changer(db_name, db_password_postgres, db_host, db_port)
    db = Database(db_name, db_user, db_password, db_host, db_port)
    db.create_user_table()
    print('Бот запущен')
    await handler_registration()
    try:
        await dp.start_polling(bot)
        print("Бот завершил работу!")
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')

