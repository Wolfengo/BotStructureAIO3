from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject, Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        language = event.from_user.language_code
        user = f'user {event.from_user.id}'
        check_user = await self.storage.redis.get(name=user)

        if not event.media_group_id:
            if '/' in event.text:
                if check_user:
                    if int(check_user.decode()) == 1:
                        await self.storage.redis.set(name=user, value=0, ex=10)
                        return await event.answer('Спам-трекер заблокировал вас на 10 секунд'
                                                  if 'ru' in language else 'Spam blocked. Wait a 10 sec')
                    return
                await self.storage.redis.set(name=user, value=1, ex=10)

        return await handler(event, data)

