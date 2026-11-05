from config.settings import ADMIN_USER_ID, YOOMONEY_RECEIVER
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from dateutil.relativedelta import relativedelta
from yoomoney import Client
from yoomoney import Quickpay

from bot import db, bot
from config import texts, markups, states
import datetime

client = Client(texts.TOKEN_YOO_MONEY)
router = Router()


@router.callback_query(F.data == 'back_profile')
async def back_profile(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await profile(callback)


@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    await callback.answer('Профиль временно не доступен!', show_alert=True)
    # if db.get_active_prem(callback.from_user.id) == 1:
    #     end_date = db.get_end_date(callback.from_user.id)
    #     if datetime.datetime.now() > datetime.datetime.strptime(end_date, '%d.%m.%Y %H:%M'):
    #         db.set_active_prem(callback.from_user.id, 0)
    #         await callback.answer(text='⚜️ Ваша подписка закончилась!\n\n'
    #                                    'Для дальнейшего использования всех функций подписки, продлите ее в профиле.',
    #                               show_alert=True)
    #
    # await bot.edit_message_media(chat_id=callback.message.chat.id,
    #                              message_id=callback.message.message_id,
    #                              media=InputMediaPhoto(
    #                                  media=texts.profile_photo,
    #                                  caption=texts.profile_text(callback.from_user.id)),
    #                              reply_markup=markups.profile_menu())


@router.callback_query(F.data == 'referrer')
async def referrers(callback: CallbackQuery):
    if db.user_exists_premium(callback.from_user.id):
        await callback.answer()
        await callback.message.answer(text=texts.referrer_text(callback.from_user.id),
                                      reply_markup=markups.close_mes)
    else:
        await callback.answer("👥 Для использования реферальной системы вам необходимо пополнить баланс на любую сумму (от 10 RUB).",
                              show_alert=True)


@router.callback_query(F.data == 'premium')
async def premium_sub(callback: CallbackQuery):
    await callback.answer(text='💝 АКЦИЯ 💝\n\n'
                               '⚜️ За каждого приглашенного друга, премиум подписка на месяц в ПОДАРОК\n\n'
                               '📎 Получить реферальную ссылку можно в разделе 👥 Рефералы',
                          show_alert=True)
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.profile_photo,
                                     caption=texts.premium_sub_text(callback.from_user.id)),
                                 reply_markup=markups.premium_sub_menu())


@router.callback_query(F.data == "1-month")
async def prem_1_month(callback: CallbackQuery):
    if db.user_exists_premium(callback.from_user.id):
        balance = db.get_balance(callback.from_user.id)
        if balance >= 100:
            current_date = datetime.datetime.now()
            if db.get_active_prem(callback.from_user.id) == 1:
                date_end_old = datetime.datetime.strptime(db.get_end_date(callback.from_user.id), '%d.%m.%Y %H:%M')
                next_month_date = date_end_old + relativedelta(months=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            else:
                next_month_date = current_date + relativedelta(months=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.profile_photo,
                                             caption=texts.premium_pay_ds(price=100, date_end=date_end)),
                                         reply_markup=markups.premium_pay_ds_kb(price=100, date_end=date_end))
        else:
            await callback.answer(text="⚜️ У вас недостаточно средств.\n"
                                       f"💸 Пополните счет на {100 - balance} RUB",
                                  show_alert=True)
    else:
        await callback.answer(text="⚜️ Для покупки подписки пополните счет на 100 RUB 💸",
                              show_alert=True)


@router.callback_query(F.data == "5-month")
async def prem_5_months(callback: CallbackQuery):
    if db.user_exists_premium(callback.from_user.id):
        balance = db.get_balance(callback.from_user.id)
        if balance >= 450:
            current_date = datetime.datetime.now()
            if db.get_active_prem(callback.from_user.id) == 1:
                date_end_old = datetime.datetime.strptime(db.get_end_date(callback.from_user.id), '%d.%m.%Y %H:%M')
                next_month_date = date_end_old + relativedelta(months=5)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            else:
                next_month_date = current_date + relativedelta(months=5)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.profile_photo,
                                             caption=texts.premium_pay_ds(price=450, date_end=date_end)),
                                         reply_markup=markups.premium_pay_ds_kb(price=450, date_end=date_end))
        else:
            await callback.answer(text="⚜️ У вас недостаточно средств.\n"
                                       f"💸 Пополните счет на {450 - balance} RUB",
                                  show_alert=True)
    else:
        await callback.answer(text="⚜️ Для покупки подписки пополните счет на 450 RUB 💸",
                              show_alert=True)


@router.callback_query(F.data == "1-year")
async def prem_1_year(callback: CallbackQuery):
    if db.user_exists_premium(callback.from_user.id):
        balance = db.get_balance(callback.from_user.id)
        if balance >= 900:
            current_date = datetime.datetime.now()
            if db.get_active_prem(callback.from_user.id) == 1:
                date_end_old = datetime.datetime.strptime(db.get_end_date(callback.from_user.id), '%d.%m.%Y %H:%M')
                next_month_date = date_end_old + relativedelta(years=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            else:
                next_month_date = current_date + relativedelta(years=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.profile_photo,
                                             caption=texts.premium_pay_ds(price=900, date_end=date_end)),
                                         reply_markup=markups.premium_pay_ds_kb(price=900, date_end=date_end))
        else:
            await callback.answer(text="⚜️ У вас недостаточно средств.\n"
                                       f"💸 Пополните счет на {900 - balance} RUB",
                                  show_alert=True)
    else:
        await callback.answer(text="⚜️ Для покупки подписки пополните счет на 900 RUB 💸",
                              show_alert=True)


@router.callback_query(F.data == "1-week")
async def prem_1_week(callback: CallbackQuery):
    if db.user_exists_premium(callback.from_user.id):
        balance = db.get_balance(callback.from_user.id)
        if balance >= 75:
            current_date = datetime.datetime.now()
            if db.get_active_prem(callback.from_user.id) == 1:
                date_end_old = datetime.datetime.strptime(db.get_end_date(callback.from_user.id), '%d.%m.%Y %H:%M')
                next_month_date = date_end_old + relativedelta(weeks=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            else:
                next_month_date = current_date + relativedelta(weeks=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.profile_photo,
                                             caption=texts.premium_pay_ds(price=75, date_end=date_end)),
                                         reply_markup=markups.premium_pay_ds_kb(price=75, date_end=date_end))
        else:
            await callback.answer(text="⚜️ У вас недостаточно средств.\n"
                                       f"💸 Пополните счет на {75 - balance} RUB",
                                  show_alert=True)
    else:
        await callback.answer(text="⚜️ Для покупки подписки пополните счет на 75 RUB 💸",
                              show_alert=True)


@router.callback_query(F.data == "1-day")
async def prem_1_day(callback: CallbackQuery):
    if db.user_exists_premium(callback.from_user.id):
        balance = db.get_balance(callback.from_user.id)
        if balance >= 50:
            current_date = datetime.datetime.now()
            if db.get_active_prem(callback.from_user.id) == 1:
                date_end_old = datetime.datetime.strptime(db.get_end_date(callback.from_user.id), '%d.%m.%Y %H:%M')
                next_month_date = date_end_old + relativedelta(days=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            else:
                next_month_date = current_date + relativedelta(days=1)
                date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
            await bot.edit_message_media(chat_id=callback.message.chat.id,
                                         message_id=callback.message.message_id,
                                         media=InputMediaPhoto(
                                             media=texts.profile_photo,
                                             caption=texts.premium_pay_ds(price=50, date_end=date_end)),
                                         reply_markup=markups.premium_pay_ds_kb(price=50, date_end=date_end))
        else:
            await callback.answer(text="⚜️ У вас недостаточно средств.\n"
                                       f"💸 Пополните счет на {50 - balance} RUB",
                                  show_alert=True)
    else:
        await callback.answer(text="⚜️ Для покупки подписки пополните счет на 50 RUB 💸",
                              show_alert=True)


@router.callback_query(lambda call: call.data.startswith('pay-prem_'))
async def premium_sub_payed(callback: CallbackQuery):
    button_text = callback.data.split('_')
    db.new_sub_premium(user_id=callback.from_user.id,
                       price=int(button_text[1]),
                       date_start=datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
                       date_end=button_text[2])
    await callback.answer("🥳 Поздравляем с покупкой подписки!\n"
                          "🫶🏻 Приятного пользования в боте!", show_alert=True)
    await profile(callback)


@router.callback_query(F.data == "top-up-balance")
async def top_up_balance(callback: CallbackQuery):
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.profile_photo,
                                     caption='💵 <b>Выберите сумму для пополнения или введите ее вручную</b>'),
                                 reply_markup=markups.top_up_kb())


@router.callback_query(F.data == "enter-summa")
async def top_up_balance_set(callback: CallbackQuery, state: FSMContext):
    mes = await bot.edit_message_media(chat_id=callback.message.chat.id,
                                       message_id=callback.message.message_id,
                                       media=InputMediaPhoto(
                                           media=texts.profile_photo,
                                           caption='✍️ <b>Введите сумму для пополнения</b>\n\n'
                                                   '- Сумма должна быть <b>целым числом</b>\n'
                                                   '- Минимальная сумма для пополнения <b>10 RUB</b>'),
                                       reply_markup=markups.back_profile)
    await state.update_data(mes_id=mes.message_id)
    await state.set_state(states.Check_Summ.summ)


@router.callback_query(lambda call: call.data.startswith('top-up_'))
async def top_up_summ(callback: CallbackQuery):
    summa = int(callback.data.split('_')[1])
    label = f"{summa}/{callback.from_user.id}/{datetime.datetime.now()}"
    pay_form = Quickpay(
        receiver=YOOMONEY_RECEIVER,
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=summa,
        label=label
    )
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(
                                     media=texts.profile_photo,
                                     caption=f'💸 Сумма к оплате: <b>{summa} RUB</b>\n'
                                             '🔍 <b>После оплаты не забудьте нажать Проверить оплату, для подтверждения транзакции</b>'),
                                 reply_markup=markups.pay_top_up(url=pay_form.redirected_url,
                                                                 label=label))


@router.callback_query(lambda call: call.data.startswith('check-top-up_'))
async def check_top_up(callback: CallbackQuery):
    label = callback.data.split('_')[1]
    print(label)
    label_list = label.split('/')
    summa, user_id, date = label_list
    history = client.operation_history(label=label)
    for operations in history.operations:
        if operations.status == 'success':
            if not db.user_exists_premium(callback.from_user.id):
                db.new_premium_user(user_id=callback.from_user.id, balance=int(summa))
                await callback.answer(text=f"✅ Ваш баланс успешно пополнен!\n\n"
                                           f"💸 Сумма: {summa} RUB\n"
                                           f"💰 Баланс: {summa} RUB",
                                      show_alert=True)
            else:
                balance = db.get_balance(callback.from_user.id) + int(summa)
                db.update_balance(user_id=callback.from_user.id, balance=balance)
                await callback.answer(text=f"✅ Ваш баланс успешно пополнен!\n\n"
                                           f"💸 Сумма: {summa} RUB\n"
                                           f"💰 Баланс: {balance} RUB",
                                      show_alert=True)
            await profile(callback)
            await bot.send_message(chat_id=ADMIN_USER_ID,
                                   text=f'💸 Пользователь @{callback.from_user.username} пополнил счет на {summa} RUB',
                                   reply_markup=markups.close_mes)
            break
        else:
            await callback.answer(text='⌛️ Ваш платеж ожидает оплаты\n'
                                       '💳 Для оплаты нажмите кнопку "Оплатить"',
                                  show_alert=True)
            break
    else:
        await callback.answer(text='⌛️ Ваш платеж ожидает оплаты\n'
                                   '💳 Для оплаты нажмите кнопку "Оплатить"',
                              show_alert=True)


@router.callback_query(F.data == "bonus")
async def bonus(callback: CallbackQuery):
    count_free = db.get_free_bonus(callback.from_user.id)
    if count_free > 0:
        current_date = datetime.datetime.now()
        if db.get_active_prem(callback.from_user.id) == 1:
            date_end_old = datetime.datetime.strptime(db.get_end_date(callback.from_user.id), '%d.%m.%Y %H:%M')
            next_month_date = date_end_old + relativedelta(months=1)
            date_end = next_month_date.strftime('%d.%m.%Y %H:%M')
        else:
            next_month_date = current_date + relativedelta(months=1)
            date_end = next_month_date.strftime('%d.%m.%Y %H:%M')

        await bot.edit_message_media(chat_id=callback.message.chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaPhoto(
                                         media=texts.profile_photo,
                                         caption=texts.premium_bonus(date_end=date_end, count_free=count_free)),
                                     reply_markup=markups.premium_pay_bonus_kb(date_end=date_end))
    else:
        await callback.answer(text='💝 У вас нет активных бонусов для активации!',
                              show_alert=True)


@router.callback_query(lambda call: call.data.startswith('pay-prem-bonus_'))
async def pay_bonus_prem_bonus(callback: CallbackQuery):
    date_end = callback.data.split('_')[1]
    db.update_bonus_minus(callback.from_user.id)
    db.new_sub_premium(user_id=callback.from_user.id,
                       price=0,
                       date_start=datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
                       date_end=date_end)
    await callback.answer("🥳 Поздравляем с покупкой подписки!\n"
                          "🫶🏻 Приятного пользования в боте!", show_alert=True)
    await profile(callback)