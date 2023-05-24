from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares.throttling import ThrottlingMiddleware

from data import config

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)
dispatcher.middleware.setup(ThrottlingMiddleware())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dispatcher

    executor.start_polling(dispatcher=dispatcher, skip_updates=True)
