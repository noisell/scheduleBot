import datetime
import logging

from aiogram import F, Router, BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from bot import bot, db

user_activity = {}

def check_activity(user_id: int) -> Any:
    now_weekday = datetime.datetime.now().weekday()
    db.update_actions(int(now_weekday))
    if user_id in user_activity:
        now = datetime.datetime.now().strftime('%d:%H:%M')
        user_data = list(user_activity[user_id])
        if type(user_data[1]) == str:
            ban_user_date = datetime.datetime.strptime(user_data[-1], '%d:%H:%M')
            if ban_user_date.strftime('%d:%H:%M') < now:
                user_activity[user_id] = [str(datetime.datetime.now().strftime('%d:%H:%M')), 1]
                return 'NICE'
            else:
                return 'IGNOR'
        else:
            user_time_dict = str(user_data[0])
            user_time = datetime.datetime.strptime(str(user_time_dict), '%d:%H:%M')
            if user_time.strftime('%d:%H:%M') == now:
                if user_data[-1] >= 25:
                    ban_date = (datetime.datetime.now() + datetime.timedelta(minutes=60)).strftime('%d:%H:%M')
                    user_activity[user_id] = [str(datetime.datetime.now().strftime('%d:%H:%M')), str(ban_date)]
                    return 'BAN'
                else:
                    count_mes = int(user_data[-1] + 1)
                    user_activity[user_id] = [str(datetime.datetime.now().strftime('%d:%H:%M')), count_mes]
                    return 'NICE'
            else:
                user_activity[user_id] = [str(datetime.datetime.now().strftime('%d:%H:%M')), 1]
                return 'NICE'
    else:
        user_activity[user_id] = [str(datetime.datetime.now().strftime('%d:%H:%M')), 1]
        return 'NICE'


class AntiSpamBot_Message(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        check_ban = check_activity(event.from_user.id)
        if check_ban == 'BAN':
            await bot.send_message(event.from_user.id,
                                   '🚫 <b>ВЫ ЗАБЛОКИРОВАНЫ ЗА СПАМ!</b>\n\nБлокировка будет снята через час')
            await bot.send_message(REMOVED_PRIVATE_VALUE,
                                   f'<b>Заблокировал пользователя за спам!\nЕго id: {event.from_user.id}\nЕго username: {event.from_user.username}</b>')
            await bot.send_message(REMOVED_PRIVATE_VALUE,
                                   f'<b>Заблокировал пользователя за спам!\nЕго id: {event.from_user.id}\nЕго username: {event.from_user.username}</b>')
            return
        elif check_ban == 'NICE':
            return await handler(event, data)
        elif check_ban == 'IGNOR':
            return


class AntiSpamBot_Callback(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        check_ban = check_activity(event.from_user.id)
        try:
            if db.get_active_prem(event.from_user.id) == 1:
                end_date = db.get_end_date(event.from_user.id)
                if datetime.datetime.now() > datetime.datetime.strptime(end_date, '%d.%m.%Y %H:%M'):
                    db.set_active_prem(event.from_user.id, 0)
        except Exception as e:
            logging.error(f"{e}")
        if check_ban == 'BAN':
            await event.answer(
                text='🚫 ВЫ ЗАБЛОКИРОВАНЫ ЗА СПАМ!\n\nБлокировка будет снята через час',
                show_alert=True)
            await bot.send_message(REMOVED_PRIVATE_VALUE,
                                   f'<b>Заблокировал пользователя за спам!\nЕго id: {event.from_user.id}\nЕго username: {event.from_user.username}</b>')
            await bot.send_message(REMOVED_PRIVATE_VALUE,
                                   f'<b>Заблокировал пользователя за спам!\nЕго id: {event.from_user.id}\nЕго username: {event.from_user.username}</b>')
            return
        elif check_ban == 'NICE':
            return await handler(event, data)
        elif check_ban == 'IGNOR':
            return
