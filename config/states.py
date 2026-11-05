from config.settings import YOOMONEY_RECEIVER
import asyncio
import datetime
import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from yoomoney import Quickpay

import utils
import schedule
from bot import db, bot
from config import texts, markups

router = Router()


class Set_time(StatesGroup):
    input_time = State()


class Spam_all(StatesGroup):
    campus_set = State()
    spam_all = State()
    spam1 = State()
    spam2 = State()


class Poll_all(StatesGroup):
    campus_set = State()
    poll1 = State()
    poll2 = State()
    send_poll = State()


class Get_Usernames(StatesGroup):
    enter_group = State()


class Find_User(StatesGroup):
    set_find = State()
    username = State()
    user_id = State()


class Check_Summ(StatesGroup):
    summ = State()


class Set_Url(StatesGroup):
    campus = State()
    url1 = State()
    url2 = State()


class Add_Home_Work(StatesGroup):
    enter_para = State()
    enter_hw = State()


class Edit_Home_Work(StatesGroup):
    enter_para = State()
    enter_hw = State()


@router.message(Set_time.input_time)
async def check_input_time(message: Message, state: FSMContext):
    if ':' in message.text and ' ' not in message.text:
        check_int = message.text.split(':')
        if len(check_int) == 2:
            try:
                hour = int(check_int[0])
                minute = int(check_int[1])
                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    if len(check_int[0]) == 2 and len(check_int[1]) == 2:
                        try:
                            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
                            await message.delete()
                        except Exception as e:
                            logging.error(f"Произошла ошибка при удалении сообщения: {e}")

                        db.set_notice_time(message.text, message.from_user.id)
                        await message.answer(
                            f'<b>✅ Изменения применены!</b>\nТеперь ты будешь получать свое расписание в <b>{message.text}</b>')
                        await bot.send_photo(chat_id=message.chat.id,
                                             photo=texts.main_photo,
                                             caption=texts.main_menu(message.from_user.first_name),
                                             reply_markup=markups.main_menu(),
                                             protect_content=True)
                        await state.clear()
                    else:
                        await message.answer(
                            '❌<b>Некорректный формат времени!</b>\nВведите время из двух цифр, <b>например 07:23</b>')
                else:
                    await message.answer(
                        '❌<b>Некорректный формат времени!</b>\nВведите реальное время, <b>например 07:38</b>')
            except ValueError:
                await message.answer('❌<b>Некорректный формат времени!</b>\nВведите числа, <b>например 07:26</b>')
        else:
            await message.answer(
                '❌<b>Некорректный формат времени!</b>\nВведите только два числа, <b>например 07:55</b>')
    else:
        await message.answer(
            '❌<b>Некорректный формат времени!</b>\nВведите время через двоеточие, <b>например 07:59</b>')


@router.message(Add_Home_Work.enter_para)
async def enter_para(message: Message, state: FSMContext):
    data_id = await state.get_data()
    mes_id = data_id['id_mess']
    try:
        await bot.delete_message(message.chat.id, int(mes_id))
    except Exception as e:
        logging.error(f'Ошибочка: {e}')
    await message.reply('✍️ <b>Теперь напиши дз на эту пару..</b>', allow_sending_without_reply=True)
    await state.update_data(para=message.text)
    await state.set_state(Add_Home_Work.enter_hw)


@router.message(Edit_Home_Work.enter_para)
async def edit_para(message: Message, state: FSMContext):
    data_id = await state.get_data()
    mes_id = data_id['id_mess']
    try:
        await bot.delete_message(message.chat.id, int(mes_id))
    except Exception as e:
        logging.error(f'Ошибочка: {e}')
    await message.reply('✍️ <b>Теперь напиши дз на эту пару..</b>', allow_sending_without_reply=True)
    await state.update_data(para=message.text)
    await state.set_state(Edit_Home_Work.enter_hw)


@router.message(Add_Home_Work.enter_hw)
async def enter_hw(message: Message, state: FSMContext):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception as e:
        print(f'Ошибочка: {e}')

    datas = await state.get_data()
    para = datas['para']
    day = datas['day']
    group = db.get_group_leader(message.from_user.id)
    if not db.get_hw(group, day):
        homework = (f'📚 <b>Домашка на {day} | Группа: {group}</b>\n\n'
                    f'<b>1. {para}</b> – {message.text}\n\n')
        db.add_hw(message.from_user.id, group, day, homework)
    else:
        homework = db.get_hw(group, day)
        count = len(homework.split("\n\n"))
        homework += f'<b>{count - 1}. {para}</b> – {message.text}\n\n'
        db.update_hw(homework, group, day)
    await message.answer_photo(
        photo=texts.rasp_photo,
        caption=homework,
        reply_markup=markups.create_key_sett_hw(day),
        protect_content=True)
    await state.clear()


@router.message(Edit_Home_Work.enter_hw)
async def enter_hww(message: Message, state: FSMContext):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception as e:
        print(f'Ошибочка: {e}')
    datas = await state.get_data()
    para = datas['para']
    day = datas['day']
    number = datas['number']
    group = db.get_group_leader(message.from_user.id)
    homework = db.get_hw(group, day)
    list_hw = homework.split("\n\n")
    list_hw[int(number)] = f'<b>{number}. {para}</b> – {message.text}'
    for i in range(len(list_hw)):
        if i != len(list_hw) - 1:
            list_hw[i] = f'{list_hw[i]}\n\n'
    homework = ''.join(list_hw)
    db.update_hw(homework, group, day)
    await message.answer_photo(
        photo=texts.rasp_photo,
        caption=homework,
        reply_markup=markups.create_key_sett_hw(day),
        protect_content=True)
    await state.clear()


@router.message(Check_Summ.summ)
async def check_summ_top_up(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data['mes_id']
    try:
        summ_pay = int(message.text)
        if summ_pay < 10:
            raise TypeError
    except ValueError:
        await message.answer(text='❌ Некорректный формат суммы, введите число')
    except TypeError:
        await message.answer(text='💰 Минимальная сумма пополнения 10 RUB')
    else:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.delete()
        except Exception as e:
            logging.error(f"Произошла ошибка при удалении сообщения: {e}")
        try:
            label = f"{summ_pay}/{message.from_user.id}/{datetime.datetime.now()}"
            pay_form = Quickpay(
                receiver=YOOMONEY_RECEIVER,
                quickpay_form="shop",
                targets="Sponsor this project",
                paymentType="SB",
                sum=summ_pay,
                label=label
            )
            await message.answer_photo(photo=texts.profile_photo,
                                       caption=f'💸 Сумма к оплате: <b>{summ_pay} RUB</b>\n'
                                               '🔍 <b>После оплаты не забудьте нажать Проверить оплату, для подтверждения транзакции</b>',
                                       reply_markup=markups.pay_top_up(url=pay_form.redirected_url,
                                                                       label=label),
                                       protect_content=True)
            await state.clear()
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
            await message.answer(text='❌ Некорректный формат суммы')