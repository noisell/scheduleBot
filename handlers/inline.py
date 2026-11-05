import datetime
import logging
import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from bot import db, bot
from config import texts, markups

router = Router()

def list_teacher():
    inline_list = []
    teachers = db.get_teach_list()
    for i in teachers:
        fio = i.split()
        inline_list.append(
            InlineQueryResultArticle(
                id=i,
                title=i,
                description=f'Преподаватель {teachers[i][0]} корпуса | {fio[0]} {fio[1][0]}.{fio[2][0]}.',
                input_message_content=InputTextMessageContent(
                    message_text=f'/teacher {teachers[i][1]}'
                ),
                thumbnail_url=random.choice(texts.teachers_photo)
            )
        )
    return inline_list


def list_group():
    inline_list = []
    groups = texts.list_groups
    for i in groups:
        prof, url = groups[i]
        inline_list.append(
            InlineQueryResultArticle(
                id=i,
                title=i,
                description=prof,
                input_message_content=InputTextMessageContent(
                    message_text=f'/set_group {i}'
                ),
                thumbnail_url=url
            )
        )
    return inline_list


@router.inline_query(lambda inline: inline.query.startswith('group'))
async def inline_mod_group(inline_query: InlineQuery):
    result = list_group()
    res = []
    if ' ' in inline_query.query:
        find = inline_query.query.replace("group ", "")
    else:
        find = inline_query.query.replace("group", "")
    if len(inline_query.query) > 0:
        for i in result:
            if find.lower() in i.title.lower():
                res.append(i)
        if not [] == res:
            await inline_query.answer(res[:50], is_personal=True)
        else:
            await inline_query.answer([
                InlineQueryResultArticle
                (
                    id='-1',
                    title='Ничего не найдено',
                    description='Проверьте правильность введенного ФИО',
                    input_message_content=InputTextMessageContent(
                        message_text='Ничего не найдено!',
                        parse_mode='HTML'),
                    thumbnail_url='https://cdn-icons-png.flaticon.com/512/11805/11805376.png'
                )
            ], is_personal=True, cache_time=10)
    else:
        await inline_query.answer(result[:50], is_personal=True, cache_time=10000)


@router.inline_query()
async def inline_mod(inline_query: InlineQuery):
    result = list_teacher()
    res = []
    if len(inline_query.query) > 0:
        for i in result:
            if inline_query.query.lower() in i.title.lower():
                res.append(i)
        if not [] == res:
            await inline_query.answer(res[:50], is_personal=True)
        else:
            await inline_query.answer([
                InlineQueryResultArticle(
                    id='-1',
                    title='Ничего не найдено',
                    description='Проверьте правильность введенного ФИО',
                    input_message_content=InputTextMessageContent(
                        message_text='Ничего не найдено!',
                        parse_mode='HTML'),
                    thumbnail_url='https://cdn-icons-png.flaticon.com/512/11805/11805376.png'
                )
            ], is_personal=True)
    else:
        await inline_query.answer(result[:50], is_personal=True)


@router.message(Command('teacher'))
async def teacher(message: Message):
    msg = message.text.replace('/teacher ', '')
    try:
        if 0 < int(msg) <= 78:
            today_date = datetime.datetime.today()
            current_weekday = today_date.weekday()
            if current_weekday != 0:
                tod_date = today_date - datetime.timedelta(days=current_weekday)
            else:
                tod_date = today_date
            db.update_date(tod_date.strftime('%d.%m.%Y'), message.from_user.id)
            fio = str(db.get_teach_fio(int(msg))).split()
            teachers = f'{fio[0]} {fio[1][0]}.{fio[2][0]}.'
            db.set_cur_teach(teachers, message.from_user.id)
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
                await message.delete()
            except Exception as e:
                logging.error(f"Произошла ошибка при удалении сообщения: {e}")
            await message.answer_photo(photo=texts.rasp_photo,
                                       caption=f"<b>✅ Учитель {teachers}</b>\n"
                                               f"<b>📅 Выбери желаемую дату расписания</b>",
                                       reply_markup=markups.update_keyboard_dates_teach(date=tod_date.strftime('%d.%m.%Y'),
                                                                                        set_group=teachers),
                                       protect_content=True)
        else:
            await message.delete()
            await message.answer('<b>Неправильный запрос!</b>')
    except ValueError:
        await message.delete()
        await message.answer('<b>Неправильный запрос!</b>')

@router.message(Command('set_group'))
async def set_group(message: Message):
    msg = message.text.replace('/set_group', '').split()
    if msg[0] in texts.list_groups:
        db.set_group(msg[0].upper(), message.from_user.id)
        today_date = datetime.datetime.today()
        current_weekday = today_date.weekday()
        if current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        db.update_date(tod_date.strftime('%d.%m.%Y'), message.from_user.id)
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.delete()
        except Exception as e:
            logging.error(f"Произошла ошибка при удалении сообщения: {e}")
        await message.answer_photo(photo=texts.rasp_photo,
                                   caption=f"<b>✅ Текущая группа {msg[0].upper()}</b>\n"
                                           f"<b>📅 Выбери желаемую дату расписания</b>",
                                   reply_markup=markups.update_keyboard_dates(date=tod_date.strftime('%d.%m.%Y'),
                                                                              set_group=msg[0].upper()),
                                   protect_content=True)

    else:
        await message.delete()
        await message.answer('<b>Неправильный запрос!</b>')