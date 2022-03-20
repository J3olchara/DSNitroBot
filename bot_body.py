from aiogram import Bot 
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token = 'THERE IS BOT TOKEN')
dp = Dispatcher(bot, storage = storage)