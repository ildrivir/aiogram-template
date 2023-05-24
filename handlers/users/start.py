from aiogram import types
from aiogram.dispatcher.filters import Command

from app import dispatcher
from utils.misc.throttling import rate_limit


@rate_limit(limit=3, key='start')(dispatcher.message_handler(Command('start')))
async def start(msg: types.Message) -> None:
    await msg.answer('Hello!')
