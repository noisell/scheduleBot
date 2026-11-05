from config.settings import ADMIN_USER_ID
import datetime
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from bot import db, bot
from utils import send_notice
from config import texts, markups, states

router = Router()


@router.message(Command('start'))
async def start_bot(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            if message.from_user.username is not None:
                username = message.from_user.username
            else:
                username = False
            if message.text != '/start':
                ref = message.text.split()[1]
                if ref and ref.isdigit():
                    referrer_id = int(ref)
                    user_id = message.from_user.id
                    if db.user_exists(referrer_id) and referrer_id != user_id and db.user_exists_premium(referrer_id):
                        if username:
                            try:
                                await bot.send_message(chat_id=referrer_id,
                                                       text=f'🤩 <b>У вас новый реферал <a href="https://t.me/{username}">{message.from_user.first_name}</a>!</b>\n'
                                                            f'🥳 Поздравляем, вам зачислен бонус, в размере <b>1 месяца</b> бесплатной подписки!',
                                                       reply_markup=markups.close_mes)
                            except TelegramBadRequest:
                                pass
                            finally:
                                db.update_bonus(user_id=referrer_id)
                                db.update_get_bonus(user_id=referrer_id)
                        else:
                            try:
                                await bot.send_message(chat_id=referrer_id,
                                                       text=f'🤩 <b>У вас новый реферал <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>!</b>\n'
                                                            f'🥳 Поздравляем, вам зачислен бонус, в размере <b>1 месяца</b> бесплатной подписки!',
                                                       reply_markup=markups.close_mes)
                            except TelegramBadRequest:
                                pass
                            finally:
                                db.update_bonus(user_id=referrer_id)
                                db.update_get_bonus(user_id=referrer_id)
                        if username:
                            db.add_user(user_id=user_id, username=message.from_user.username, referrer_id=referrer_id)
                        else:
                            db.add_user(user_id=user_id, referrer_id=referrer_id)

                        await bot.send_photo(chat_id=message.chat.id,
                                             photo=texts.main_photo,
                                             caption=texts.main_menu(message.from_user.first_name),
                                             reply_markup=markups.main_menu(),
                                             protect_content=True)
                    else:
                        await message.answer(text="❗️ Неправильная ссылка. Проверьте ее корректность и повторите попытку.",
                                             reply_markup=markups.close_mes)
                else:
                    if username:
                        db.add_user(user_id=message.from_user.id, username=message.from_user.username)
                    else:
                        db.add_user(user_id=message.from_user.id)

                    await bot.send_photo(chat_id=message.chat.id,
                                         photo=texts.main_photo,
                                         caption=texts.main_menu(message.from_user.first_name),
                                         reply_markup=markups.main_menu(),
                                         protect_content=True)
            else:
                if username:
                    db.add_user(user_id=message.from_user.id, username=message.from_user.username)
                else:
                    db.add_user(user_id=message.from_user.id)

                await bot.send_photo(chat_id=message.chat.id,
                                     photo=texts.main_photo,
                                     caption=texts.main_menu(message.from_user.first_name),
                                     reply_markup=markups.main_menu(),
                                     protect_content=True)

            await send_notice(message.from_user.id)
        else:
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=texts.main_photo,
                                 caption=texts.main_menu(message.from_user.first_name),
                                 reply_markup=markups.main_menu(),
                                 protect_content=True)
            await state.clear()
    else:
        await message.answer('<b>❣️ Не люблю быть в группах, запусти меня в личной переписке</b>')


@router.message(F.text == '🔝 Главное меню')
async def back_main_menu(message: Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id,
                         photo=texts.main_photo,
                         caption=texts.main_menu(message.from_user.first_name),
                         reply_markup=markups.main_menu())
    await state.clear()


@router.callback_query(F.data == 'support')
async def support(callback: CallbackQuery):
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.about,
                                     caption=texts.support_menu
                                 ),
                                 reply_markup=markups.back_main_menu)


@router.message(F.text == '🔝 Назад')
async def back_schedule(message: Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id,
                         photo=texts.main_photo,
                         caption=texts.main_menu(message.from_user.first_name),
                         reply_markup=markups.main_menu)
    await state.clear()


@router.callback_query(F.data == 'settings')
async def settings(callback: CallbackQuery):
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.settings,
                                     caption=texts.create_settings_text(callback.from_user.id)
                                 ),
                                 reply_markup=markups.create_settings_keyboard(callback.from_user.id))


@router.callback_query(F.data == 'off_morning')
async def off_morning(callback: CallbackQuery):
    db.set_notice_morn(0, callback.from_user.id)
    await settings(callback)


@router.callback_query(F.data == 'on_morning')
async def on_morning(callback: CallbackQuery):
    db.set_notice_morn(1, callback.from_user.id)
    await settings(callback)


@router.callback_query(F.data == 'off_chang')
async def off_chang(callback: CallbackQuery):
    db.set_notice_changes(0, callback.from_user.id)
    await settings(callback)


@router.callback_query(F.data == 'on_chang')
async def on_chang(callback: CallbackQuery):
    db.set_notice_changes(1, callback.from_user.id)
    await settings(callback)


@router.callback_query(F.data == 'off_not_ch')
async def off_not_ch(callback: CallbackQuery):
    db.set_not_chang(0, callback.from_user.id)
    await settings(callback)


@router.callback_query(F.data == 'on_not_ch')
async def on_not_ch(callback: CallbackQuery):
    db.set_not_chang(1, callback.from_user.id)
    await settings(callback)


@router.callback_query(F.data == 'settings_time')
async def on_not_ch(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.settings,
                                     caption="<b>⏰ Введи время в которое ты бы хотел получать свое расписание на день!\nВ формате часы:минуты, например: 07:35</b>"
                                 ),
                                 reply_markup=markups.back_settings)
    await state.set_state(states.Set_time.input_time)


@router.callback_query(F.data == 'back_main_menu')
async def main_menu(callback: CallbackQuery):
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.main_photo,
                                     caption=texts.main_menu(callback.from_user.first_name)),
                                 reply_markup=markups.main_menu())


@router.callback_query(F.data == 'back_settings')
async def back_settings(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await settings(callback)


@router.callback_query(F.data == 'homework')
async def homework(callback: CallbackQuery):
    today_date = datetime.datetime.today()
    current_weekday = today_date.weekday()
    if not db.user_exists_leader(callback.from_user.id):
        if current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
        group = db.select_current_group(callback.from_user.id)
        if db.group_exists_leader(group):
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.homework_photo,
                                             caption='📚 <b>Выбери день, на который хочешь узнать д/з</b>'),
                                         reply_markup=markups.update_keyboard_dates_hw_use(
                                             tod_date.strftime('%d.%m.%Y'),
                                             group))
        else:
            await callback.answer(text='☹️ Твоя группа еще не подключена к данной функции!', show_alert=True)

    else:
        if current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
        await bot.edit_message_media(chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaPhoto(
                                         media=texts.homework_photo,
                                         caption='📚 <b>Выбери день для добавления д/з</b>'),
                                     reply_markup=markups.update_keyboard_dates_hw(tod_date.strftime('%d.%m.%Y'),
                                                                                   db.get_group_leader(
                                                                                       callback.from_user.id)))


@router.callback_query(lambda call: call.data.startswith('send-admin_'))
async def send_message_admin(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await bot.send_message(chat_id=ADMIN_USER_ID,
                           text=f'Сообщение от <a href="tg://user?id={callback.from_user.id}">{callback.from_user.first_name}</a>:')
    await bot.copy_message(chat_id=ADMIN_USER_ID,
                           from_chat_id=callback.message.chat.id,
                           message_id=int(button_text[1]))
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text="Ваше сообщение успешно отправлено!")


@router.callback_query(F.data == 'delete-mess')
async def delete_message(callback: CallbackQuery):
    await callback.answer("Сообщение удалено!")
    await callback.message.delete()
