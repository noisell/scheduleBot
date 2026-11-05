import logging
from urllib.parse import urlencode
from schedule import campus_1, campus_2, is_upper_week, parsing_changes, first_course, second_course, third_course, fourth_course, fc2, sc2, tc2, add_db_changes, create_schedule
from config import markups, texts

import requests
import re
import os
import datetime
import asyncio
from bot import bot, db

YANDEX_TOKEN = os.environ["YANDEX_TOKEN"]

def state_group():
    state_text = '<b>👥 Статистика по группам:</b>\n\n'
    count = 0
    all_std = 0
    text_course = ''

    for group in first_course:
        counts = db.count_users_group(str(group).upper())
        if count < 3:
            if counts <= 9:
                text_course += f'<code>{str(group).upper()}:</code> {counts}    '
                count += 1
            else:
                text_course += f'<code>{str(group).upper()}:</code> {counts}  '
                count += 1
        else:
            text_course += f'<code>{str(group).upper()}:</code> {counts}\n'
            count = 0
        all_std += counts

    state_text += f"🌟 <b>  1 КОРПУС  🌟</b>\n\n<code>👨‍🎓 1 КУРС – СТУДЕНТОВ:</code> <b>{all_std}</b>\n{text_course}"
    count = 0
    all_std = 0
    text_course = ''

    for group in second_course:
        counts = db.count_users_group(str(group).upper())
        if count < 3:
            if counts <= 9:
                text_course += f'<code>{str(group).upper()}:</code> {counts}    '
                count += 1
            else:
                text_course += f'<code>{str(group).upper()}:</code> {counts}  '
                count += 1
        else:
            text_course += f'<code>{str(group).upper()}:</code> {counts}\n'
            count = 0
        all_std += counts

    state_text += f"\n<code>👨‍🎓 2 КУРС – СТУДЕНТОВ:</code> <b>{all_std}</b>\n{text_course}"
    count = 0
    all_std = 0
    text_course = ''

    for group in third_course:
        counts = db.count_users_group(str(group).upper())
        if count < 1:
            if counts <= 9:
                text_course += f'<code>{str(group).upper()}:</code> {counts}    '
                count += 1
            else:
                text_course += f'<code>{str(group).upper()}:</code> {counts}  '
                count += 1
        else:
            text_course += f'<code>{str(group).upper()}:</code> {counts}\n'
            count = 0
        all_std += counts

    state_text += f"\n<code>👨‍🎓 3 КУРС – СТУДЕНТОВ:</code> <b>{all_std}</b>\n{text_course}"
    count = 0
    all_std = 0
    text_course = ''
    for group in fourth_course:
        counts = db.count_users_group(str(group).upper())
        if count < 2:
            if counts <= 9:
                text_course += f'<code>{str(group).upper()}:</code> {counts}    '
                count += 1
            else:
                text_course += f'<code>{str(group).upper()}:</code> {counts}  '
                count += 1
        else:
            text_course += f'<code>{str(group).upper()}:</code> {counts}\n'
            count = 0
        all_std += counts

    state_text += f"\n<code>👨‍🎓 4 КУРС – СТУДЕНТОВ:</code> <b>{all_std}</b>\n{text_course}"
    count = 0
    all_std = 0
    text_course = ''
    for group in fc2:
        counts = db.count_users_group(str(group).upper())
        if count < 2:
            if counts <= 9:
                text_course += f'<code>{str(group).upper()}:</code> {counts}    '
                count += 1
            else:
                text_course += f'<code>{str(group).upper()}:</code> {counts}  '
                count += 1
        else:
            text_course += f'<code>{str(group).upper()}:</code> {counts}\n'
            count = 0
        all_std += counts

    state_text += f"\n🌟 <b>  2 КОРПУС  🌟</b>\n\n<code>👨‍🎓 1 КУРС – СТУДЕНТОВ:</code> <b>{all_std}</b>\n{text_course}"
    count = 0
    all_std = 0
    text_course = ''

    for group in sc2:
        counts = db.count_users_group(str(group).upper())
        if count < 3:
            if counts <= 9:
                text_course += f'<code>{str(group).upper()}:</code> {counts}    '
                count += 1
            else:
                text_course += f'<code>{str(group).upper()}:</code> {counts}  '
                count += 1
        else:
            text_course += f'<code>{str(group).upper()}:</code> {counts}\n'
            count = 0
        all_std += counts

    state_text += f"\n<code>👨‍🎓 2 КУРС – СТУДЕНТОВ:</code> <b>{all_std}</b>\n{text_course}"
    count = 0
    all_std = 0
    text_course = ''

    for group in tc2:
        counts = db.count_users_group(str(group).upper())
        if count < 3:
            if counts <= 9:
                text_course += f'<code>{str(group).upper()}:</code> {counts}    '
                count += 1
            else:
                text_course += f'<code>{str(group).upper()}:</code> {counts}  '
                count += 1
        else:
            text_course += f'<code>{str(group).upper()}:</code> {counts}\n'
            count = 0
        all_std += counts

    state_text += f"\n\n<code>👨‍🎓 3 КУРС – СТУДЕНТОВ:</code> <b>{all_std}</b>\n{text_course}"

    return state_text


async def send_message(text=None, admin=None):
    if admin == 0:
        await bot.send_message(REMOVED_PRIVATE_VALUE, text)
    if admin == 1:
        not_active = 0
        users_len = 0
        active = 0
        find_group = parsing_changes('Changes.pdf')
        active_group = []
        date_chang = []
        return_date = ''
        for t in find_group:
            if 'ВЕРХНЯЯ НЕДЕЛЯ' in t or 'НИЖНЯЯ НЕДЕЛЯ' in t:
                finds_date = re.compile(r'\d{2}\.\d{2}\.\d{4}')
                date = finds_date.search(t).group()
                date_chang.append(date)
            active_group.append(t[0])
        if len(date_chang) > 1:
            if len(date_chang) == 2:
                return_date += f'{date_chang[0]} и {date_chang[1]}'
            else:
                for dat in date_chang:
                    if dat == date_chang[-1]:
                        return_date += f'{dat}'
                    else:
                        return_date += f'{dat}, '
        else:
            return_date = f'{date_chang[0]}'
        for users in db.get_all_users():
            try:
                if str(db.select_current_group(users)).lower() in campus_1 and db.get_notice_changes(users) != 0 and db.get_active_prem(users) == 1:
                    users_len += 1
                    if db.select_current_group(users) in active_group:
                        await bot.send_photo(chat_id=users,
                                             photo=texts.changes_photo,
                                             caption=f'<b>👨‍💻 Добавлены изменения в расписании</b>\n\n'
                                                     f'📆 Дата: <b>{return_date}</b>\n'
                                                     f'👨‍🎓 Группа: <b>{db.select_current_group(users)}</b>\n\n'
                                                     f'❗️ <b>ИЗМЕНЕНИЯ НАЙДЕНЫ</b>',
                                             reply_markup=markups.close_mes)

                    else:
                        if db.get_not_chang(users) == 1:
                            await bot.send_photo(chat_id=users,
                                                 photo=texts.changes_photo,
                                                 caption=f'<b>👨‍💻 Добавлены изменения в расписании</b>\n\n'
                                                         f'📆 Дата: <b>{return_date}</b>\n'
                                                         f'👨‍🎓 Группа: <b>{db.select_current_group(users)}</b>\n\n'
                                                         f'✖️ <b>ИЗМЕНЕНИЯ НЕ НАЙДЕНЫ</b>',
                                                 reply_markup=markups.close_mes)

                active += 1
            except Exception as e:
                print(e)
                not_active += 1
        await bot.send_message(REMOVED_PRIVATE_VALUE,
                               f'<b>👨‍💻 Доставлены уведомления об изменениях 1 корпуса! \n\nОтправлено сообщений: {users_len} \nАктивных пользователей: {active} \nПользователей заблокировавших бота: {not_active}</b>',
                               reply_markup=markups.close_mes)

    if admin == 2:
        not_active = 0
        active = 0
        active_gr = 0
        find_group = parsing_changes('Changes2.pdf')
        active_group = []
        date_chang = []
        return_date = ''
        for t in find_group:
            if 'ВЕРХНЯЯ НЕДЕЛЯ' in t or 'НИЖНЯЯ НЕДЕЛЯ' in t:
                finds_date = re.compile(r'\d{2}\.\d{2}\.\d{4}')
                date = finds_date.search(t).group()
                date_chang.append(date)
            active_group.append(t[0])
        if len(date_chang) > 1:
            if len(date_chang) == 2:
                return_date += f'{date_chang[0]} и {date_chang[1]}'
            else:
                for dat in date_chang:
                    if dat == date_chang[-1]:
                        return_date += f'{dat}'
                    else:
                        return_date += f'{dat}, '
        else:
            return_date = f'{date_chang[0]}'

        for users in db.get_all_users():
            try:
                if str(db.select_current_group(users)).lower() in campus_2 and db.get_notice_changes(users) != 0 and db.get_active_prem(users) == 1:
                    active_gr += 1
                    if db.select_current_group(users) in active_group:
                        await bot.send_photo(chat_id=users,
                                             photo=texts.changes_photo,
                                             caption=f'<b>👨‍💻 Добавлены изменения в расписании</b>\n\n'
                                                     f'📆 Дата: <b>{return_date}</b>\n'
                                                     f'👨‍🎓 Группа: <b>{db.select_current_group(users)}</b>\n\n'
                                                     f'❗️ <b>ИЗМЕНЕНИЯ НАЙДЕНЫ</b>',
                                             reply_markup=markups.close_mes)
                    else:
                        if db.get_not_chang(users) == 1:
                            await bot.send_photo(chat_id=users,
                                                 photo=texts.changes_photo,
                                                 caption=f'<b>👨‍💻 Добавлены изменения в расписании</b>\n\n'
                                                         f'📆 Дата: <b>{return_date}</b>\n'
                                                         f'👨‍🎓 Группа: <b>{db.select_current_group(users)}</b>\n\n'
                                                         f'✖️ <b>ИЗМЕНЕНИЯ НЕ НАЙДЕНЫ</b>',
                                                 reply_markup=markups.close_mes)
                active += 1
            except Exception as e:
                print(e)
                not_active += 1
        await bot.send_message(REMOVED_PRIVATE_VALUE,
                               f'<b>👨‍💻 Доставлены уведомления об изменениях 2 корпуса! \n\nОтправлено сообщений: {active_gr} \nАктивных пользователей: {active} \nПользователей заблокировавших бота: {not_active}</b>',
                               reply_markup=markups.close_mes)


def get_file_info(file_links):
    api_url = 'https://cloud-api.yandex.net/v1/disk/public/resources'
    headers = {'Authorization': YANDEX_TOKEN,
               'Accept': 'application/json'}
    params = {'public_key': file_links,
              'sort': 'modified'}

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        file_info = response.json()
        modified = file_info['modified']
        return modified
    else:
        print('Ошибка получения информации о файле')
        return False


def download():
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = str(db.get_url(1))
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    download_response = requests.get(download_url)
    with open('Changes.pdf', 'wb') as patch:
        patch.write(download_response.content)


def download2():
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = str(db.get_url(2))
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    download_response = requests.get(download_url)
    with open('Changes2.pdf', 'wb') as patch:
        patch.write(download_response.content)


async def array_changes_1():
    logging.info("Изменения 1 корпуса парсятся")
    while True:
        file_link = str(db.get_url(1))
        # ПЕРВЫЙ КОРПУС
        try:
            if get_file_info(file_link) != db.get_date(camp=1):
                download()
                await asyncio.sleep(10)
                update_chan = str(get_file_info(file_link)).split('T')
                cur_date = str(datetime.date.today().strftime('%Y-%m-%d'))
                if db.get_id_chan(cur_date, 1):
                    id_changes = db.get_id_chan(cur_date, 1)
                    for id_chang in id_changes:
                        db.delete_changes(int(id_chang))
                    if db.get_id_teach(cur_date, 1):
                        id_teaches = db.get_id_teach(cur_date, 1)
                        for id_teach in id_teaches:
                            db.delete_teach(int(id_teach))

                db.set_update(update_chan[1], 1)
                db.set_date(get_file_info(file_link), 1)
                changes_list = parsing_changes('Changes.pdf')
                add_db_changes(changes_list, 1, cur_date)
                await send_message(text='<b>👨‍💻 Новые изменения 1 корпуса успешно добавлены в бд</b>', admin=0)
                await send_message(admin=1)
                await asyncio.sleep(600)  # 10 минуту
            else:
                await asyncio.sleep(60)
        except Exception as e:
            await send_message(text=f'<b>👨‍💻 В цикле с изменениями 1 корпуса произошла ошибка:</b> <code>{e}</code>',
                               admin=0)
            await asyncio.sleep(3600)


async def array_changes_2():
    logging.info("Изменения 2 корпуса парсятся")
    while True:
        file_link2 = str(db.get_url(2))
        # ВТОРОЙ КОРПУС
        try:
            if get_file_info(file_link2) != db.get_date(camp=2):
                download2()
                await asyncio.sleep(10)
                update_chan = str(get_file_info(file_link2)).split('T')
                cur_date = str(datetime.date.today().strftime('%Y-%m-%d'))
                if db.get_id_chan(cur_date, 2):
                    id_changes = db.get_id_chan(cur_date, 2)
                    for id_chang in id_changes:
                        db.delete_changes(int(id_chang))
                    if db.get_id_teach(cur_date, 2):
                        id_teaches = db.get_id_teach(cur_date, 2)
                        for id_teach in id_teaches:
                            db.delete_teach(int(id_teach))

                db.set_update(update_chan[1], 2)
                db.set_date(get_file_info(file_link2), 2)
                changes_list = parsing_changes('Changes2.pdf')
                add_db_changes(changes_list, 2, cur_date)
                await send_message(text='<b>👨‍💻 Новые изменения 2 корпуса успешно добавлены в бд</b>', admin=0)
                await send_message(admin=2)
                await asyncio.sleep(600)  # 10 минут
            else:
                await asyncio.sleep(60)  # 1 минута
        except Exception as e:
            await send_message(text=f'<b>👨‍💻 В цикле с изменениями 2 корпуса произошла ошибка:</b> <code>{e}</code>',
                               admin=0)
            await asyncio.sleep(60)


async def send_notice(user_id):
    while True:
        current_weekday = datetime.datetime.today().weekday()
        current_time = str(datetime.datetime.today().strftime('%H:%M'))
        current_group = db.select_current_group(user_id)
        if int(current_weekday) != 6:
            sub = db.get_active_prem(user_id)
            if db.get_notice_time(user_id) == current_time and db.get_notice_morn(
                    user_id) == 1 and current_group != '0' and sub == 1:
                print(user_id)
                current_date = str(datetime.datetime.today().strftime('%d.%m'))
                if is_upper_week(current_date):
                    up_or_down_week = 2
                else:
                    up_or_down_week = 1
                rasp = create_schedule(current_weekday, current_group, current_date, up_or_down_week, sub)
                try:
                    await bot.send_photo(chat_id=user_id,
                                         photo=texts.notice_morning_photo,
                                         caption='😊 <b>Доброе утро, солнышко!</b>\n\n'
                                                 '<b>Скоро на пары, держи расписание</b> 👇\n\n'
                                                 f'{rasp}',
                                         reply_markup=markups.close_mes)
                    await asyncio.sleep(60)
                except Exception as e:
                    logging.error(f"Ошибка в уведомлениях утром: {e}")
                    await asyncio.sleep(60)
            else:
                await asyncio.sleep(20)
        else:
            await asyncio.sleep(3600)
