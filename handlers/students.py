from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import schedule
from bot import db, bot
from config import texts, markups, states
import datetime
from schedule import create_schedule, create_schedule_teach

router = Router()


@router.callback_query(F.data == 'rasp_students')
async def schedule_students(callback: CallbackQuery):
    await callback.answer('Еще не набралось 500 голосов в опросе!', show_alert=True)
    return
    # current_group = db.select_current_group(callback.from_user.id)
    # if current_group != '0':
    #     today_date = datetime.datetime.today()
    #     current_weekday = today_date.weekday()
    #     if current_weekday != 0:
    #         tod_date = today_date - datetime.timedelta(days=current_weekday)
    #     else:
    #         tod_date = today_date
    #     db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
    #     await bot.edit_message_media(chat_id=callback.message.chat.id,
    #                                  message_id=callback.message.message_id,
    #                                  media=InputMediaPhoto(
    #                                      media=texts.rasp_photo,
    #                                      caption=f"<b>👨‍🎓 Текущая группа: {current_group}</b>\n"
    #                                              "<b>📅 Выбери желаемую дату расписания</b>"),
    #                                  reply_markup=markups.update_keyboard_dates(date=tod_date.strftime('%d.%m.%Y'),
    #                                                                             set_group=current_group))
    #
    # else:
    #     await bot.edit_message_media(chat_id=callback.message.chat.id,
    #                                  message_id=callback.message.message_id,
    #                                  media=InputMediaPhoto(
    #                                      media=texts.rasp_photo,
    #                                      caption='<b>Для продолжения тебе надо выбрать группу</b>'),
    #                                  reply_markup=markups.set_group_menu)


@router.callback_query(lambda call: call.data.startswith('previous-week-clicked-hw-use'))
async def previous_week_clicked_hw_use(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    previous_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') - datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    previous_week_date = previous_week_date.replace(year=current_year)
    db.update_date(previous_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates_hw_use(
                                            date=previous_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('previous-week-clicked-hw'))
async def previous_week_clicked_hw(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    previous_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') - datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    previous_week_date = previous_week_date.replace(year=current_year)
    db.update_date(previous_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates_hw(
                                            date=previous_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('previous-week-clicked-teach'))
async def previous_week_clicked_teach(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    previous_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') - datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    previous_week_date = previous_week_date.replace(year=current_year)
    db.update_date(previous_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates_teach(
                                            date=previous_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('previous-week-clicked'))
async def previous_week_clicked(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    previous_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') - datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    previous_week_date = previous_week_date.replace(year=current_year)
    db.update_date(previous_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates(
                                            date=previous_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('next-week-clicked-hw-use'))
async def next_week_clicked_hw_use(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    next_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') + datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    next_week_date = next_week_date.replace(year=current_year)
    db.update_date(next_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates_hw_use(
                                            date=next_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('next-week-clicked-hw'))
async def next_week_clicked_hw(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    next_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') + datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    next_week_date = next_week_date.replace(year=current_year)
    db.update_date(next_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates_hw(
                                            date=next_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('next-week-clicked-teach'))
async def next_week_clicked_teach(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    next_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') + datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    next_week_date = next_week_date.replace(year=current_year)
    db.update_date(next_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates_teach(
                                            date=next_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('next-week-clicked'))
async def next_week_clicked(callback: CallbackQuery):
    button_text = callback.data.split('_')
    await callback.answer()
    next_week_date = datetime.datetime.strptime(
        callback.message.reply_markup.inline_keyboard[1][0].text.split()[2],
        '%d.%m') + datetime.timedelta(days=7)
    current_year = datetime.datetime.now().year
    next_week_date = next_week_date.replace(year=current_year)
    db.update_date(next_week_date.strftime('%d.%m.%Y'), callback.from_user.id)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=markups.update_keyboard_dates(
                                            date=next_week_date.strftime('%d.%m.%Y'),
                                            set_group=button_text[1]))


@router.callback_query(lambda call: call.data.startswith('now-day-teach'))
async def now_day_tech(callback: CallbackQuery):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    try:
        today_date = datetime.datetime.today()
        current_weekday = today_date.weekday()
        if current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        if current_weekday == 6:
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption='🦦 <b>Расслабься, сегодня выходной</b>'),
                                         reply_markup=markups.update_keyboard_dates_teach(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1]))
            await callback.answer()
        else:
            if schedule.is_upper_week(button_text[2]):
                up_or_down_week = 2
            else:
                up_or_down_week = 1
            current_year = datetime.datetime.now().year
            tod_date = tod_date.replace(year=current_year)
            sub = db.get_active_prem(callback.from_user.id)
            rasp = create_schedule_teach(current_weekday, button_text[1], button_text[2], up_or_down_week, sub)
            db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption=rasp),
                                         reply_markup=markups.update_keyboard_dates_teach(
                                             date=tod_date.strftime('%d.%m.%Y'),
                                             set_group=button_text[1],
                                             update_markup=today_date.strftime('%d.%m')))
            await callback.answer()
    except TelegramBadRequest:
        await callback.answer('Этот день уже выбран!')


@router.callback_query(lambda call: call.data.startswith('now-day'))
async def now_day(callback: CallbackQuery):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    try:
        today_date = datetime.datetime.today()
        current_weekday = today_date.weekday()
        if current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        if current_weekday == 6:
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption='🦦 <b>Расслабься, сегодня выходной</b>'),
                                         reply_markup=markups.update_keyboard_dates(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1]))
            await callback.answer()
        else:
            if schedule.is_upper_week(button_text[2]):
                up_or_down_week = 2
            else:
                up_or_down_week = 1
            current_year = datetime.datetime.now().year
            tod_date = tod_date.replace(year=current_year)
            sub = db.get_active_prem(callback.from_user.id)
            rasp = create_schedule(current_weekday, button_text[1], button_text[2], up_or_down_week, sub)
            db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption=rasp),
                                         reply_markup=markups.update_keyboard_dates(date=tod_date.strftime('%d.%m.%Y'),
                                                                                    set_group=button_text[1],
                                                                                    update_markup=today_date.strftime(
                                                                                        '%d.%m')))
            await callback.answer()
    except TelegramBadRequest:
        await callback.answer('Этот день уже выбран!')


@router.callback_query(lambda call: call.data.startswith('tomorrow-day-hw-use'))
async def tomorrow_day_hw_use(callback: CallbackQuery):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    try:
        today_date = datetime.datetime.today()
        current_weekday = today_date.weekday()
        tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1))
        if current_weekday == 6:
            tod_date = tomorrow
        elif current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        if tomorrow.weekday() == 6:
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.homework_photo,
                                             caption='🦦 <b>Расслабься, завтра выходной</b>'),
                                         reply_markup=markups.update_keyboard_dates_hw_use(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1]))
            await callback.answer()
        else:
            db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
            homework = db.get_hw_use(button_text[1], button_text[-1])
            if homework:
                try:
                    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                                 message_id=callback.message.message_id,
                                                 media=InputMediaPhoto(
                                                     media=texts.homework_photo,
                                                     caption=homework),
                                                 reply_markup=markups.update_keyboard_dates_hw_use(
                                                     date=tod_date.strftime('%d.%m.%Y'),
                                                     set_group=button_text[1],
                                                     update_markup=tomorrow.strftime('%d.%m')))
                    await callback.answer()
                except TelegramBadRequest:
                    await callback.answer('Этот день уже выбран!')
            else:
                try:
                    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                                 message_id=callback.message.message_id,
                                                 media=InputMediaPhoto(
                                                     media=texts.homework_photo,
                                                     caption='🫧 <b>На этот день дз не выложено</b>'),
                                                 reply_markup=markups.update_keyboard_dates_hw_use(
                                                     date=tod_date.strftime('%d.%m.%Y'),
                                                     set_group=button_text[1],
                                                     update_markup=tomorrow.strftime('%d.%m')))
                    await callback.answer()
                except TelegramBadRequest:
                    await callback.answer('Этот день уже выбран!')
    except TelegramBadRequest:
        await callback.answer('Этот день уже выбран!')


@router.callback_query(lambda call: call.data.startswith('tomorrow-day-hw'))
async def tomorrow_day_hw(callback: CallbackQuery, state: FSMContext):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    try:
        today_date = datetime.datetime.today()
        current_weekday = today_date.weekday()
        tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1))
        if current_weekday == 6:
            tod_date = tomorrow
        elif current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        if tomorrow.weekday() == 6:
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.homework_photo,
                                             caption='🦦 <b>Расслабься, завтра выходной, можно без домашки</b>'),
                                         reply_markup=markups.update_keyboard_dates_hw(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1]))
            await callback.answer()

        else:
            db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
            group_leader = db.get_group_leader(callback.from_user.id)
            if db.set_active_hw(group_leader, str(tomorrow.strftime('%d.%m'))):
                homework = db.get_hw(group_leader, str(tomorrow.strftime('%d.%m')))
                await callback.answer()
                await bot.edit_message_media(chat_id=callback.message.chat.id,
                                             message_id=callback.message.message_id,
                                             media=InputMediaPhoto(
                                                 media=texts.homework_photo,
                                                 caption=homework),
                                             reply_markup=markups.create_key_sett_hw(str(tomorrow.strftime('%d.%m'))))
            else:
                await bot.edit_message_media(chat_id=callback.message.chat.id,
                                             message_id=callback.message.message_id,
                                             media=InputMediaPhoto(
                                                 media=texts.homework_photo,
                                                 caption='<b>✍️ Напиши мне название дисциплины..</b>'),
                                             reply_markup=markups.remove_date)
                await callback.answer()
                await state.set_state(states.Add_Home_Work.enter_para)
                await state.update_data(day=str(tomorrow.strftime('%d.%m')))
                await state.update_data(id_mess=callback.message.message_id)
    except TelegramBadRequest:
        await callback.answer("Этот день уже выбран!")


@router.callback_query(lambda call: call.data.startswith('tomorrow-day-teach'))
async def tomorrow_day_teach(callback: CallbackQuery):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    try:
        today_date = datetime.datetime.today()
        current_weekday = today_date.weekday()
        tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1))
        if current_weekday == 6:
            tod_date = tomorrow
        elif current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        if tomorrow.weekday() == 6:
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption='🦦 <b>Расслабься, завтра выходной</b>'),
                                         reply_markup=markups.update_keyboard_dates_teach(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1]))
            await callback.answer()
        else:
            if schedule.is_upper_week(button_text[2]):
                up_or_down_week = 2
            else:
                up_or_down_week = 1
            current_year = datetime.datetime.now().year
            tod_date = tod_date.replace(year=current_year)
            sub = db.get_active_prem(callback.from_user.id)
            rasp = create_schedule_teach(tomorrow.weekday(), button_text[1], button_text[2], up_or_down_week, sub)
            db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption=rasp),
                                         reply_markup=markups.update_keyboard_dates_teach(
                                             date=tod_date.strftime('%d.%m.%Y'),
                                             set_group=button_text[1],
                                             update_markup=tomorrow.strftime('%d.%m')))
            await callback.answer()
    except TelegramBadRequest:
        await callback.answer('Этот день уже выбран!')


@router.callback_query(lambda call: call.data.startswith('tomorrow-day'))
async def tomorrow_day(callback: CallbackQuery):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    try:
        today_date = datetime.datetime.today()
        current_weekday = today_date.weekday()
        tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1))
        if current_weekday == 6:
            tod_date = tomorrow
        elif current_weekday != 0:
            tod_date = today_date - datetime.timedelta(days=current_weekday)
        else:
            tod_date = today_date
        if tomorrow.weekday() == 6:
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption='🦦 <b>Расслабься, завтра выходной</b>'),
                                         reply_markup=markups.update_keyboard_dates(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1]))
            await callback.answer()
        else:
            if schedule.is_upper_week(button_text[2]):
                up_or_down_week = 2
            else:
                up_or_down_week = 1
            current_year = datetime.datetime.now().year
            tod_date = tod_date.replace(year=current_year)
            sub = db.get_active_prem(callback.from_user.id)
            rasp = create_schedule(tomorrow.weekday(), button_text[1], button_text[2], up_or_down_week, sub)
            db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.rasp_photo,
                                             caption=rasp),
                                         reply_markup=markups.update_keyboard_dates(date=tod_date.strftime('%d.%m.%Y'),
                                                                                    set_group=button_text[1],
                                                                                    update_markup=tomorrow.strftime(
                                                                                        '%d.%m')))
            await callback.answer()
    except TelegramBadRequest:
        await callback.answer('Этот день уже выбран!')


@router.callback_query(lambda call: call.data.startswith('group-teach'))
async def group_teach(callback: CallbackQuery):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    current_year = datetime.datetime.now().year

    day = button_text[2]
    day1 = datetime.datetime.strptime(day, '%d.%m').replace(year=current_year)
    week = day1.weekday()
    current_group = button_text[1]
    if schedule.is_upper_week(button_text[2]):
        up_or_down_week = 2
    else:
        up_or_down_week = 1
    sub = db.get_active_prem(callback.from_user.id)
    rasp = create_schedule_teach(week, current_group, button_text[2], up_or_down_week, sub)
    try:
        await bot.edit_message_media(chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaPhoto(
                                         media=texts.rasp_photo,
                                         caption=rasp),
                                     reply_markup=markups.update_keyboard_dates_teach(
                                         date=current_date1.strftime('%d.%m.%Y'),
                                         set_group=button_text[1],
                                         update_markup=button_text[2]))
        await callback.answer()
    except TelegramBadRequest:
        await callback.answer('Этот день уже выбран!')


@router.callback_query(lambda call: call.data.startswith('group'))
async def group_set(callback: CallbackQuery):
    button_text = callback.data.split('_')
    current_date = db.select_cur_date(callback.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    current_year = datetime.datetime.now().year

    day = button_text[2]
    day1 = datetime.datetime.strptime(day, '%d.%m').replace(year=current_year)
    week = day1.weekday()
    current_group = button_text[1]
    if schedule.is_upper_week(button_text[2]):
        up_or_down_week = 2
    else:
        up_or_down_week = 1
    sub = db.get_active_prem(callback.from_user.id)
    rasp = create_schedule(week, current_group, button_text[2], up_or_down_week, sub)
    try:
        await bot.edit_message_media(chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaPhoto(
                                         media=texts.rasp_photo,
                                         caption=rasp),
                                     reply_markup=markups.update_keyboard_dates(
                                         date=current_date1.strftime('%d.%m.%Y'),
                                         set_group=button_text[1],
                                         update_markup=button_text[2]))
        await callback.answer()
    except TelegramBadRequest:
        await callback.answer('Этот день уже выбран!')


@router.callback_query(F.data == 'rasp_teachers')
async def teacher_sch(callback: CallbackQuery):
    await callback.answer('Еще не набралось 500 голосов в опросе!', show_alert=True)
    # if db.get_active_prem(callback.from_user.id) != 1:
    #     await callback.answer(text="⚜️ У вас нет премиум подписки!\n\n"
    #                                "✅ Расписание\n"
    #                                "✅ Расписание с изменениями\n"
    #                                "✅ Домашка\n"
    #                                "🔒 Уведомления об изменениях\n"
    #                                "🔒 Напоминания утром\n"
    #                                "🔒 Улучшенная поддержка\n\n"
    #                                "👤 Приобрести подписку можно в профиле",
    #                           show_alert=True)
    # cur_teach = db.get_cur_teach(callback.from_user.id)
    # if cur_teach != '0':
    #     today_date = datetime.datetime.today()
    #     current_weekday = today_date.weekday()
    #     if current_weekday != 0:
    #         tod_date = today_date - datetime.timedelta(days=current_weekday)
    #     else:
    #         tod_date = today_date
    #     db.update_date(tod_date.strftime('%d.%m.%Y'), callback.from_user.id)
    #     await bot.edit_message_media(chat_id=callback.message.chat.id,
    #                                  message_id=callback.message.message_id,
    #                                  media=InputMediaPhoto(
    #                                      media=texts.rasp_photo,
    #                                      caption=f'🧑‍🏫 <b>Текущий учитель: {cur_teach}</b>\n'
    #                                              f'<b>📅 Выбери желаемую дату расписания</b>'),
    #                                  reply_markup=markups.update_keyboard_dates_teach(
    #                                      date=tod_date.strftime('%d.%m.%Y'),
    #                                      set_group=cur_teach))
    #
    # else:
    #     await bot.edit_message_media(chat_id=callback.message.chat.id,
    #                                  message_id=callback.message.message_id,
    #                                  media=InputMediaPhoto(
    #                                      media=texts.rasp_photo,
    #                                      caption='<b>Для продолжения тебе надо выбрать учителя</b>'),
    #                                  reply_markup=markups.set_teach_menu)


@router.callback_query(lambda call: call.data.startswith('use-date-use'))
async def use_date_use(callback_query: CallbackQuery):
    button_text = callback_query.data.split('_')
    current_date = db.select_cur_date(callback_query.from_user.id)
    current_date1 = datetime.datetime.strptime(current_date, '%d.%m.%Y')
    homework = db.get_hw_use(button_text[1], button_text[-1])
    if homework:
        try:
            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.homework_photo,
                                             caption=homework),
                                         reply_markup=markups.update_keyboard_dates_hw_use(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1],
                                             update_markup=button_text[2]))
            await callback_query.answer()
        except TelegramBadRequest:
            await callback_query.answer('Этот день уже выбран!')
    else:
        try:
            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.homework_photo,
                                             caption='🫧 <b>На этот день дз не выложено</b>'),
                                         reply_markup=markups.update_keyboard_dates_hw_use(
                                             date=current_date1.strftime('%d.%m.%Y'),
                                             set_group=button_text[1],
                                             update_markup=button_text[2]))
            await callback_query.answer()
        except TelegramBadRequest:
            await callback_query.answer('Этот день уже выбран!')


@router.callback_query(lambda call: call.data.startswith('use-date'))
async def use_date(callback_query: CallbackQuery, state: FSMContext):
    button_text = callback_query.data.split('_')
    groups = db.get_group_leader(callback_query.from_user.id)
    if db.set_active_hw(groups, button_text[2]):
        homeworks = db.get_hw(groups, button_text[2])
        await callback_query.answer()
        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id,
                                     media=InputMediaPhoto(
                                         media=texts.homework_photo,
                                         caption=homeworks),
                                     reply_markup=markups.create_key_sett_hw(button_text[2]))
    else:
        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id,
                                     media=InputMediaPhoto(
                                         media=texts.homework_photo,
                                         caption='<b>✍️ Напиши мне название дисциплины..</b>'),
                                     reply_markup=markups.remove_date)
        await state.set_state(states.Add_Home_Work.enter_para)
        await state.update_data(day=button_text[2])
        await state.update_data(id_mess=callback_query.message.message_id)


@router.callback_query(lambda call: call.data.startswith('plus-hw'))
async def plus_hw(callback_query: CallbackQuery, state: FSMContext):
    button_text = callback_query.data.split('_')
    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.homework_photo,
                                     caption='<b>✍️ Напиши мне название дисциплины..</b>'),
                                 reply_markup=markups.create_key_edit_hw(button_text[-1]))
    await callback_query.answer()
    await state.set_state(states.Add_Home_Work.enter_para)
    await state.update_data(day=button_text[-1])
    await state.update_data(id_mess=callback_query.message.message_id)


@router.callback_query(lambda call: call.data.startswith('back-hw-edit'))
async def back_hw_edit(callback_query: CallbackQuery, state: FSMContext):
    button_text = callback_query.data.split('_')
    groups = db.get_group_leader(callback_query.from_user.id)
    homeworks = db.get_hw(groups, button_text[1])
    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.homework_photo,
                                     caption=homeworks),
                                 reply_markup=markups.create_key_sett_hw(button_text[1]))
    await state.clear()


@router.callback_query(F.data == 'remove_date')
async def remove_date(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    today_date = datetime.datetime.today()
    current_weekday = today_date.weekday()
    if current_weekday != 0:
        tod_date = today_date - datetime.timedelta(days=current_weekday)
    else:
        tod_date = today_date
    db.update_date(tod_date.strftime('%d.%m.%Y'), callback_query.message.from_user.id)
    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.homework_photo,
                                     caption='📚 <b>Выбери день для добавления дз</b>'),
                                 reply_markup=markups.update_keyboard_dates_hw(tod_date.strftime('%d.%m.%Y'),
                                                                               db.get_group_leader(
                                                                                   callback_query.from_user.id)))


@router.callback_query(lambda call: call.data.startswith('save-hw'))
async def save_hw(callback_query: CallbackQuery, state: FSMContext):
    button_text = callback_query.data.split('_')
    await state.clear()
    group = db.get_group_leader(callback_query.from_user.id)
    db.active_hw(1, group, button_text[-1])
    await callback_query.answer('✅ Домашка сохранена и доступна для просмотра.', show_alert=True)
    today_date = datetime.datetime.today()
    current_weekday = today_date.weekday()
    if current_weekday != 0:
        tod_date = today_date - datetime.timedelta(days=current_weekday)
    else:
        tod_date = today_date
    db.update_date(tod_date.strftime('%d.%m.%Y'), callback_query.message.from_user.id)
    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.homework_photo,
                                     caption='📚 <b>Выбери день для добавления дз</b>'),
                                 reply_markup=markups.update_keyboard_dates_hw(tod_date.strftime('%d.%m.%Y'), group))


@router.callback_query(lambda call: call.data.startswith('delete-hw'))
async def delete_hw(callback_query: CallbackQuery, state: FSMContext):
    button_text = callback_query.data.split('_')
    await state.clear()
    group = db.get_group_leader(callback_query.from_user.id)
    db.delete_hw(group, button_text[-1])
    await callback_query.answer('❗️ Вы удалили всю домашнюю работу на этот день.', show_alert=True)
    today_date = datetime.datetime.today()
    current_weekday = today_date.weekday()
    if current_weekday != 0:
        tod_date = today_date - datetime.timedelta(days=current_weekday)
    else:
        tod_date = today_date
    db.update_date(tod_date.strftime('%d.%m.%Y'), callback_query.message.from_user.id)
    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.homework_photo,
                                     caption='📚 <b>Выбери день для добавления дз</b>'),
                                 reply_markup=markups.update_keyboard_dates_hw(tod_date.strftime('%d.%m.%Y'),
                                                                               group))


@router.callback_query(lambda call: call.data.startswith('edit-hw'))
async def edit_hw(callback_query: CallbackQuery):
    button_text = callback_query.data.split('_')
    mes_id = callback_query.message.message_id
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=mes_id)
    group = db.get_group_leader(callback_query.from_user.id)
    homework = db.get_hw(group, button_text[-1])
    count_str = len(homework.split('\n\n'))
    await callback_query.answer('Выбери номер строчки, которую ты бы хотел изменить')
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups.number_str(count_str - 2, mes_id, button_text[-1]))


@router.callback_query(lambda call: call.data.startswith('edit-str-num'))
async def edit_str_num(callback_query: CallbackQuery, state: FSMContext):
    button_text = callback_query.data.split('_')
    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.homework_photo,
                                     caption='<b>✍️ Напиши мне название дисциплины..</b>'))
    await state.set_state(states.Edit_Home_Work.enter_para)
    await state.update_data(day=button_text[2])
    await state.update_data(number=button_text[1])
    await state.update_data(id_mess=callback_query.message.message_id)
