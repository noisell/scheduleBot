from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config.database import Database

bot = Bot(token="REMOVED_PRIVATE_VALUE", default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
db = Database('config/database.db')