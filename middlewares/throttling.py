from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, msg: types.Message, data: dict):
        handler_data = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler_data:
            limit = getattr(handler_data, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler_data, "throttling_key", f"{self.prefix}_{handler_data.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(msg, t)
            raise CancelHandler()

    @staticmethod
    async def message_throttled(message: types.Message, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            await message.reply("Багато запитів, бан курва!")
