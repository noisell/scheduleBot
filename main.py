import asyncio
import logging
import sys

from config import states
from bot import bot, dp
from handlers import main_hl, students, inline, middlewares, admin, profile
from aiogram import F, Router

router = Router()
router.message.filter(F.chat.type == "private")


async def main() -> None:
    dp.message.outer_middleware(middlewares.AntiSpamBot_Message())
    dp.callback_query.outer_middleware(middlewares.AntiSpamBot_Callback())
    dp.include_router(router)
    dp.include_router(main_hl.router)
    dp.include_router(profile.router)
    dp.include_router(students.router)
    dp.include_router(states.router)
    dp.include_router(inline.router)
    dp.include_router(admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот завершил свою работу!")
