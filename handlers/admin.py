from config.settings import ADMIN_USER_ID, OWNER_USER_ID
import asyncio
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, InputPollOption
from aiogram.fsm.context import FSMContext
from bot import db, bot
from config import markups, states
import utils
import schedule

router = Router()

@router.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        await message.answer('👑 Добро пожаловать, дорогой админ', reply_markup=markups.admin_panel)
    else:
        await message.answer('<b>❣️ Такая команда доступна только админу</b>')


@router.message(Command('add_admin'))
async def add_admin(message: Message):
    if message.from_user.id == ADMIN_USER_ID:
        data_admin = message.text.split()
        db.add_leader_user(int(data_admin[1]), data_admin[2])
        await message.answer('<b>Новый староста успешно добавлен!</b>')


@router.message(F.text == '🔝 В Админ панель')
async def back_adm(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        await message.answer('👑 Добро пожаловать, дорогой админ', reply_markup=markups.admin_panel)
        await state.clear()


@router.message(F.text == '👥 Пересылка')
async def send_all(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        await message.answer('<b>Выбери кому будем делать пересылку</b>', reply_markup=markups.campus_spam)
        await state.set_state(states.Poll_all.campus_set)
    else:
        await message.answer('<b>❣️ К сожалению такая команда доступна только админу</b>')


@router.message(F.text == '👥 Рассылка')
async def send_all(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        await message.answer('<b>Выбери для кого будем делать рассылку</b>', reply_markup=markups.campus_spam)
        await state.set_state(states.Spam_all.campus_set)
    else:
        await message.answer('<b>❣️ К сожалению такая команда доступна только админу</b>')


@router.message(states.Poll_all.campus_set)
async def campus_set(message: Message, state: FSMContext):
    if message.text == '1 КОРПУСУ':
        await message.answer('Отправьте мне сообщение для пересылки 1 корпусу', reply_markup=markups.back_admin)
        await state.set_state(states.Poll_all.poll1)
    elif message.text == '2 КОРПУСУ':
        await message.answer('Отправьте мне сообщение для пересылки 2 корпусу', reply_markup=markups.back_admin)
        await state.set_state(states.Poll_all.poll2)
    elif message.text == 'ВСЕМ':
        await message.answer('Отправьте мне сообщение для пересылки всем пользователям',
                             reply_markup=markups.back_admin)
        await state.set_state(states.Poll_all.send_poll)


@router.message(states.Spam_all.campus_set)
async def campus_set(message: Message, state: FSMContext):
    if message.text == '1 КОРПУСУ':
        await message.answer('Введите текст текс для рассылки 1 корпусу', reply_markup=markups.back_admin)
        await state.set_state(states.Spam_all.spam1)
    elif message.text == '2 КОРПУСУ':
        await message.answer('Введите текст текс для рассылки 2 корпусу', reply_markup=markups.back_admin)
        await state.set_state(states.Spam_all.spam2)
    elif message.text == 'ВСЕМ':
        await message.answer('Введите текст текс для рассылки всем пользователя', reply_markup=markups.back_admin)
        await state.set_state(states.Spam_all.spam_all)


@router.message(states.Poll_all.send_poll)
async def all_spam(message: Message, state: FSMContext):
    not_active = 0
    active = 0
    for user in db.get_all_users():
        try:
            await bot.forward_message(chat_id=user, from_chat_id=message.chat.id, message_id=message.message_id)
            active += 1
        except Exception as e:
            print(e)
            not_active += 1

    await message.answer(
        f'<b>✅ Пересылка прошла успешно!</b>\nАктивных пользователей: {active}\n<b>Пользователей заблокировавших бота: {not_active}</b>')
    await state.clear()


@router.message(states.Spam_all.spam_all)
async def all_spam(message: Message, state: FSMContext):
    spam_text = message.text
    not_active = 0
    active = 0
    for user in db.get_all_users():
        try:
            await bot.send_message(user, text=spam_text)
            active += 1
        except Exception as e:
            print(e)
            not_active += 1

    await message.answer(
        f'<b>✅ Рассылка прошла успешно!</b>\nАктивных пользователей: {active}\n<b>Пользователей заблокировавших бота: {not_active}</b>')
    await state.clear()


@router.message(states.Poll_all.poll1)
async def spam_1(message: Message, state: FSMContext):
    not_active = 0
    active = 0
    for user in db.get_all_users():
        if str(db.select_current_group(user)).lower() in schedule.campus_1:
            try:
                await bot.forward_message(chat_id=user, from_chat_id=message.chat.id, message_id=message.message_id)
                active += 1
            except Exception as e:
                print(e)
                not_active += 1

    await message.answer(
        f'<b>✅ Пересылка прошла успешно!</b>\nАктивных пользователей 1 корпуса: {active}\n<b>Пользователей заблокировавших бота: {not_active}</b>')
    await state.clear()


@router.message(states.Spam_all.spam1)
async def spam_1(message: Message, state: FSMContext):
    spam_text = message.text
    not_active = 0
    active = 0
    for user in db.get_all_users():
        if str(db.select_current_group(user)).lower() in schedule.campus_1:
            try:
                await bot.send_message(user, text=spam_text)
                active += 1
            except Exception as e:
                print(e)
                not_active += 1

    await message.answer(
        f'<b>✅ Рассылка прошла успешно!</b>\nАктивных пользователей 1 корпуса: {active}\n<b>Пользователей заблокировавших бота: {not_active}</b>')
    await state.clear()


@router.message(states.Poll_all.poll2)
async def spam_2(message: Message, state: FSMContext):
    not_active = 0
    active = 0
    for user in db.get_all_users():
        if str(db.select_current_group(user)).lower() in schedule.campus_2:
            try:
                await bot.forward_message(chat_id=user, from_chat_id=message.chat.id, message_id=message.message_id)
                active += 1
            except Exception as e:
                print(e)
                not_active += 1

    await message.answer(
        f'<b>✅ Пересылка прошла успешно!</b>\nАктивных пользователей 2 корпуса: {active}\n<b>Пользователей заблокировавших бота: {not_active}</b>')
    await state.clear()


@router.message(states.Spam_all.spam2)
async def spam_2(message: Message, state: FSMContext):
    spam_text = message.text
    not_active = 0
    active = 0
    for user in db.get_all_users():
        if str(db.select_current_group(user)).lower() in schedule.campus_2:
            try:
                await bot.send_message(user, text=spam_text)
                active += 1
            except Exception as e:
                print(e)
                not_active += 1

    await message.answer(
        f'<b>✅ Рассылка прошла успешно!</b>\nАктивных пользователей 2 корпуса: {active}\n<b>Пользователей заблокировавших бота: {not_active}</b>')
    await state.clear()


@router.message(F.text == '📊 Статистика')
async def statistics(message: Message):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        count_user = list(db.get_all_users())
        stats = ('📊 <b>АКТУАЛЬНАЯ СТАТИСТИКА</b>\n\n'
                 f'<code>ПОЛЬЗОВАТЕЛЕЙ В БОТЕ:</code> <b>{len(count_user)}</b>\n'
                 f'<code>УВЕДОМЛЕНИЯ УТРОМ:</code> <b>{db.count_users_notice(1)}</b>\n'
                 f'<code>УВЕД. ОБ ИЗМЕНЕНИЯХ:</code> <b>{db.count_users_chang(1)}</b>\n\n')
        stats += utils.state_group()
        await message.answer(text=stats, reply_markup=markups.get_usernames)
    else:
        await message.answer('<b>❣️ К сожалению такая команда доступна только админу</b>')


@router.message(F.text == '👥 Получить usernames')
async def enter_group(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        await message.answer('<b>Введи группу, для получения пользователей:</b>', reply_markup=markups.back_admin)
        await state.set_state(states.Get_Usernames.enter_group)


@router.message(states.Get_Usernames.enter_group)
async def get_usernames(message: Message, state: FSMContext):
    if message.text.lower() in schedule.list_groups:
        result = f"<b>Вот все студенты группы {message.text.upper()}:</b>\n\n"
        lists_username = db.get_username(message.text.upper())
        for i in lists_username:
            if i == 'Без username':
                result += f"{i}\n"
            else:
                result += f"@{i}\n"
        result += f"\n<b>Количество пользователей: {len(lists_username)}</b>"
        await message.answer(text=result, reply_markup=markups.get_usernames)
        await state.clear()
    else:
        await message.answer('<b>В нашем колледже нет такой группы!</b>')


@router.message(F.text == '🔎 Найти пользователя')
async def set_find(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        await message.answer('<b>Выбери как будем искать</b>', reply_markup=markups.set_find_user)
        await state.set_state(states.Find_User.set_find)


@router.message(states.Find_User.set_find)
async def find_user(message: Message, state: FSMContext):
    if message.text == 'ПО USERNAME':
        await message.answer('Введи username того, кого хочешь найти, без @:')
        await state.set_state(states.Find_User.username)
    elif message.text == 'ПО USER ID':
        await message.answer('Введи user_id того, кого хочешь найти:')
        await state.set_state(states.Find_User.user_id)
    else:
        await message.answer('<b>Выбери ниже!</b>')


@router.message(states.Find_User.username)
async def find_user_username(message: Message, state: FSMContext):
    glaz_boba = db.find_users(username=message.text)
    if not glaz_boba == []:
        return_text = ('<b>Информация успешно найдена!</b>\n\n'
                       f'<code>USERNAME:</code> <b>{message.text}</b>\n'
                       f'<code>USER ID:</code> <b>{glaz_boba[0]}</b>\n'
                       f'<code>ГРУППА:</code> <b>{glaz_boba[1]}</b>\n'
                       f'<code>УВЕДОМЛЕНИЯ УТРОМ:</code> <b>{glaz_boba[2]}</b>\n'
                       f'<code>ВРЕМЯ ОТПРАВКИ:</code> <b>{glaz_boba[3]}</b>\n'
                       f'<code>УВЕДОМЛЕНИЯ ОБ ИЗМЕНЕНИЯХ:</code> <b>{glaz_boba[4]}</b>')
        await message.answer(return_text, reply_markup=markups.get_usernames)
        await state.clear()
    else:
        await message.answer('<b>Ничего не найдено!</b>', reply_markup=markups.get_usernames)


@router.message(states.Find_User.user_id)
async def find_user_username(message: Message, state: FSMContext):
    try:
        glaz_boba = db.find_users(user_id=int(message.text))
        if not glaz_boba == []:
            return_text = ('<b>Информация успешно найдена!</b>\n\n'
                           f'<code>USERNAME:</code> <b>{glaz_boba[0]}</b>\n'
                           f'<code>USER ID:</code> <b>{message.text}</b>\n'
                           f'<code>ГРУППА:</code> <b>{glaz_boba[1]}</b>\n'
                           f'<code>УВЕДОМЛЕНИЯ УТРОМ:</code> <b>{glaz_boba[2]}</b>\n'
                           f'<code>ВРЕМЯ ОТПРАВКИ:</code> <b>{glaz_boba[3]}</b>\n'
                           f'<code>УВЕДОМЛЕНИЯ ОБ ИЗМЕНЕНИЯХ:</code> <b>{glaz_boba[4]}</b>')
            await message.answer(return_text, reply_markup=markups.get_usernames)
            await state.clear()
        else:
            await message.answer('<b>Ничего не найдено!</b>', reply_markup=markups.get_usernames)
    except ValueError:
        await message.answer('<b>Введи цифры!</b>')


@router.message(F.text == '🔗 Сменить ссылку')
async def set_url(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID or message.from_user.id == OWNER_USER_ID:
        await message.answer(
            f'<b>Текущие ссылки:\n\n1 корпус –</b> <code>{db.get_url(1)}</code>\n<b>2 корпус –</b> <code>{db.get_url(2)}</code>\n\n<b>Введи в каком корпусе будем менять?</b>',
            reply_markup=markups.back_admin)
        await state.set_state(states.Set_Url.campus)


@router.message(states.Set_Url.campus)
async def update_url(message: Message, state: FSMContext):
    if message.text == '1':
        await message.answer('<b>1 корпус – принято!\nТеперь отправь мне ссылку</b>')
        await state.set_state(states.Set_Url.url1)
    elif message.text == '2':
        await message.answer('<b>2 корпус – принято!\nТеперь отправь мне ссылку</b>')
        await state.set_state(states.Set_Url.url2)
    else:
        await message.answer('<b>У нас нет такого корпуса</b>')


@router.message(states.Set_Url.url1)
async def update_url1(message: Message, state: FSMContext):
    db.set_url(message.text, 1)
    await message.answer(f'<b>Ссылка 1 корпуса обновлена –</b> <code>{message.text}</code>')
    await state.clear()


@router.message(states.Set_Url.url2)
async def update_url2(message: Message, state: FSMContext):
    db.set_url(message.text, 2)
    await message.answer(f'<b>Ссылка 2 корпуса обновлена –</b> <code>{message.text}</code>')
    await state.clear()


@router.message(F.text == '/admin_start_main_array_3752')
async def yes_is_work(message: Message):
    if message.from_user.id == ADMIN_USER_ID:
        await message.answer('<b>Вы выполнили запуск, проверьте логи</b>')
        await start_array()


async def start_array() -> None:
    users = db.get_all_users()  # Все пользователи бота
    tasks = []
    count = 0
    for user_id in users:
        try:
            tasks.append(asyncio.create_task(utils.send_notice(user_id)))  # запуск третьего бесконечного цикла для каждого пользователя
        except Exception as e:
            logging.error(f"Ошибка в главном цикле:{e}\nДля пользователя: {user_id}")
        else:
            count += 1
    logging.info(f'Главный цикл запущен для {count} человек!')
    await asyncio.gather(*tasks, utils.array_changes_1(), utils.array_changes_2())


@router.message(F.text == '/send_pool')
async def send_pool(message: Message):
    if message.from_user.id == ADMIN_USER_ID:
        msg = await message.bot.send_poll(
            chat_id=message.chat.id,
            question="👨‍💻 Хочешь пользоваться ботом?\n\n"
                     "Делись опросом с друзьями и если наберется хотя бы 500 желающих, "
                     "то бот снова станет полностью бесплатным и будет всегда вовремя уведомлять тебя об изменениях!",
            options=[InputPollOption(text='Да'),
                     InputPollOption(text='Нет')],
            is_anonymous=True
        )
        count = 0
        all_users = db.get_all_users()
        for user_id in all_users:
            try:
                await bot.forward_message(
                    chat_id=user_id,
                    from_chat_id=message.chat.id,
                    message_id=msg.message_id
                )
                count += 1
            except Exception as e:
                print(e)
        await message.answer(f'Активных пользователей: {count}')


@router.message()
async def send_admin(message: Message):
    if db.user_exists(message.from_user.id):
        await message.reply(f'<b>Вы хотите отправить это сообщение админу?</b>',
                            reply_markup=markups.create_send_admin_keyboard(message.message_id))