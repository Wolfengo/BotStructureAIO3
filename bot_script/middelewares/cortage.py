from aiogram import types, BaseMiddleware

import asyncio
from typing import Union, List, Callable, Any, Awaitable

from aiogram.types import Message


# class AlbumMiddleware(BaseMiddleware):
#     """Пример работы AlbumMiddleware с кортежами
#
# async def echo(message: Message, album: list[Message]):
#     media_group = []
#     for msg in album:
#         if msg.photo:
#             file_id = msg.photo[-1].file_id
#             media_group.append(InputMediaPhoto(media=file_id))
#         else:
#             obj_dict = msg.dict()
#             file_id = obj_dict[msg.content_type]['file_id']
#             media_group.append(InputMedia(media=file_id))
#
#     await message.answer_media_group(media_group)"""
#     album_data: dict = {}
#
#     def __init__(self, latency: Union[int, float] = 0.01):
#         self.latency = latency
#
#     async def __call__(
#             self,
#             handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
#             message: Message,
#             data: dict[str, Any]
#     ) -> Any:
#         if not message.media_group_id:
#             await handler(message, data)
#             return
#         try:
#             self.album_data[message.media_group_id].append(message)
#         except KeyError:
#             self.album_data[message.media_group_id] = [message]
#             await asyncio.sleep(self.latency)
#
#             data['_is_last'] = True
#             data["album"] = self.album_data[message.media_group_id]
#             await handler(message, data)
#
#         if message.media_group_id and data.get("_is_last"):
#             del self.album_data[message.media_group_id]
#             del data['_is_last']

class AlbumMiddleware(BaseMiddleware):
    """Пример работы AlbumMiddleware с кортежами

async def echo(message: Message, album: list[Message]):
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(InputMediaPhoto(media=file_id))
        else:
            obj_dict = msg.dict()
            file_id = obj_dict[msg.content_type]['file_id']
            media_group.append(InputMedia(media=file_id))

    await message.answer_media_group(media_group)"""
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        if message.media_group_id:
            try:
                self.album_data[message.media_group_id].append(message)
            except KeyError:
                self.album_data[message.media_group_id] = [message]
                await asyncio.sleep(self.latency)

            data['_is_last'] = True
            try:
                data["album"] = self.album_data[message.media_group_id]
                if data.get("_is_last"):
                    del self.album_data[message.media_group_id]
                    del data['_is_last']
            except KeyError:
                if data.get("_is_last"):
                    del data['_is_last']
        else:
            data["album"] = [message]
            print(data)
        try:
            return await handler(message, data)
        except TypeError:
            pass