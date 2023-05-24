from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter

from app import dispatcher
from utils.misc.throttling import rate_limit


@rate_limit(limit=3)(dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT)))
async def echo(msg: types.Message) -> None:
    await msg.answer(msg.text)
