import logging
import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto, InputMediaVideo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder
from config import texts, markups, database

logging.basicConfig(level=logging.INFO)
bot = Bot(texts.BOT_TOKEN_LOVE, parse_mode='HTML')
db = database.Database('config/db_love.db')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

not_symbols = ['[', ']', '{', '}', '<', '>',  '`', '~', '\\']

@dp.message(Command('start'))
async def lowe_ngk(message: Message, state: FSMContext):
    await state.clear()
    if not db.user_exists_love(message.from_user.id) or not db.get_accept(message.from_user.id):
        await message.answer(text=texts.accept_love, reply_markup=markups.accept_love)
    elif not db.get_prof(message.from_user.id):
        await message.answer(f'<b>👋 Приветствую тебя, {message.from_user.first_name}</b>\n\n'
                             f'💖 <b>Я готов помочь найти тебе новые знакомства в нашем колледже!</b>\n\n'
                             f'💌 <b>Давай создадим тебе анкету, для этого нажми на кнопку ниже</b>',
                             reply_markup=markups.create_prof)
    else:
        await message.answer(texts.main_menu_love, reply_markup=markups.main_love)


class Create_Prof(StatesGroup):
    name = State()
    gender = State()
    groups = State()
    year = State()

class About(StatesGroup):
    interes = State()
    about = State()

class Media(StatesGroup):
    media1 = State()
    media2 = State()
    media3 = State()
    end = State()

class Edit(StatesGroup):
    edite_about = State()
    edit_find = State()
    edite_name = State()
    edite_group = State()


@dp.message(Create_Prof.name)
async def name_prof(message: Message, state: FSMContext):
    true = 1
    for i in message.text:
        if i in not_symbols:
            await message.answer('<b>❗️ Введи имя без специальных символов</b>')
            true = 0
            break
    if true:
        db.set_name(message.text.title(), message.from_user.id)
        await message.answer('<b>❤️‍🔥 Какого ты пола?</b>', reply_markup=markups.gender)
        await state.set_state(Create_Prof.gender)


@dp.message(Edit.edite_name)
async def ed_prof(message: Message, state: FSMContext):
    true = 1
    for i in message.text:
        if i in not_symbols:
            await message.answer('<b>❗️ Введи имя без специальных символов</b>')
            true = 0
            break
    if true:
        db.set_name(message.text.title(), message.from_user.id)
        await end(message, state)


@dp.message(Create_Prof.gender)
async def set_gender(message: Message, state: FSMContext):
    course = [
        [KeyboardButton(text='1 корпус'),
         KeyboardButton(text='2 корпус'),
         KeyboardButton(text='3 корпус')]
    ]
    course = ReplyKeyboardMarkup(keyboard=course, resize_keyboard=True)
    if message.text.lower() == 'мужского':
        db.set_gender(1, message.from_user.id)
        await message.answer('<b>👨‍🎓 В каком корпусе учишься?</b>', reply_markup=course)
        await state.set_state(Create_Prof.groups)
    elif message.text.lower() == 'женского':
        db.set_gender(2, message.from_user.id)
        await message.answer('<b>👩‍🎓 В каком корпусе учишься?</b>', reply_markup=course)
        await state.set_state(Create_Prof.groups)
    else:
        await message.answer('<b>❗️ Выбери вариант ответа на клавиатуре</b>')


all_groups = ['11б', '12б', '11л', '12л', '13л', '11п', '12п', '13п', '14п', '11ю', '12ю', '13ю', '21б', '22б', '21л',
              '22л', '21ю', '22ю', '23ю', '32ю', '33ю', '21п', '22в', '23п', '24в', '31с', '31б', '31л', '31ю', '31п',
              '32б', '32л', '32в', '33п', '41б', '41п', '42б', '42в', '43п', '44в',
              '11к', '12к', '13к', '14к', '21к', '22к', '23к', '31к', '32к', '31т',
              '21бд', '22бд', '31бд', '32бд', '11доу', '12доу', '21доу', '33доу', '31доу', '22доу'
              '144', '144а', '144к', '244',
              '244а', '244к', '344', '344а', '344в', '444', '444а', '444к',
              '130', '230', '330', '430',
              '146', '146а', '146б', '146к', '246', '246а', '246б', '246к', '346', '346а', '346б', '346в', '446',
              '446а', '446к1', '446к2',
              '144б', '244б', '344б', '444б']


@dp.message(Create_Prof.groups)
async def set_course(message: Message, state: FSMContext):
    if message.text.lower() == '1 корпус':
        db.set_course(message.text, message.from_user.id)
        await message.answer('<b>🤩 Сколько тебе лет?</b>', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Create_Prof.year)
    elif message.text.lower() == '2 корпус':
        db.set_course(message.text, message.from_user.id)
        await message.answer('<b>🤩 Сколько тебе лет?</b>', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Create_Prof.year)
    elif message.text.lower() == '3 корпус':
        db.set_course(message.text, message.from_user.id)
        await message.answer('<b>🤩 Сколько тебе лет?</b>', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Create_Prof.year)
    else:
        await message.answer('<b>❗️ В нашем колледже нет такого корпуса</b>')


@dp.message(Edit.edite_group)
async def ed_course(message: Message, state: FSMContext):
    if message.text.lower() == '1 корпус':
        db.set_course(message.text, message.from_user.id)
        await end(message, state)
    elif message.text.lower() == '2 корпус':
        db.set_course(message.text, message.from_user.id)
        await end(message, state)
    elif message.text.lower() == '3 корпус':
        db.set_course(message.text, message.from_user.id)
        await end(message, state)
    else:
        await message.answer('<b>❗️ В нашем колледже нет такого корпуса</b>')


@dp.message(Create_Prof.year)
async def set_year(message: Message, state: FSMContext):
    try:
        year = int(message.text)
        if 13 < year < 30:
            db.set_year(year, message.from_user.id)
            await message.answer('<b>🫰 Чьи анкеты хочешь смотреть?</b>', reply_markup=markups.interes)
            await state.set_state(About.interes)
        elif year <= 13:
            await message.answer('<b>🙃 Мне кажется тебе еще рано знакомится</b>')
        elif year >= 30:
            await message.answer('<b>🤨 Мне кажется ты не студент</b>')
    except ValueError:
        await message.answer('<b>🙂 Не прикалывайся, введи число</b>')


@dp.message(About.interes)
async def set_interes(message: Message, state: FSMContext):
    if message.text == 'Парней':
        db.set_interes(1, message.from_user.id)
        await message.answer('<b>💌 Расскажи о себе, о своих интересах, на каком курсе, кого ищешь.</b>\n'
                             '<b>Это поможет быстрее найти новые знакомства!</b>', reply_markup=markups.about)
        await state.set_state(About.about)
    elif message.text == 'Девушек':
        db.set_interes(2, message.from_user.id)
        await message.answer('<b>💌 Расскажи о себе, о своих интересах, на каком курсе, кого ищешь.</b>\n'
                             '<b>Это поможет быстрее найти новые знакомства!</b>', reply_markup=markups.about)
        await state.set_state(About.about)
    elif message.text == 'Все равно':
        db.set_interes(3, message.from_user.id)
        await message.answer('<b>💌 Расскажи о себе, о своих интересах, на каком курсе, кого ищешь.</b>\n'
                             '<b>Это поможет быстрее найти новые знакомства!</b>', reply_markup=markups.about)
        await state.set_state(About.about)
    else:
        await message.answer('<b>❗️ Выбери вариант ответа на клавиатуре</b>')


@dp.message(Edit.edit_find)
async def ed_interes(message: Message, state: FSMContext):
    if message.text == 'Парней':
        db.set_interes(1, message.from_user.id)
        await end(message, state)
    elif message.text == 'Девушек':
        db.set_interes(2, message.from_user.id)
        await end(message, state)
    elif message.text == 'Все равно':
        db.set_interes(3, message.from_user.id)
        await end(message, state)
    else:
        await message.answer('<b>❗️ Выбери вариант ответа на клавиатуре</b>')


@dp.message(About.about)
async def set_about(message: Message, state: FSMContext):
    true = 1
    if message.text != 'Пропустить этот шаг':
        for i in message.text:
            if i in not_symbols:
                await message.answer('<b>❗️ Не используй специальные символы</b>')
                true = 0
                break
        if true:
            db.set_about(message.text, message.from_user.id)
            await message.answer('<b>🖼 Теперь отправь мне свою фотографию или видео</b>', reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(Media.media1)
    else:
        db.set_about('0', message.from_user.id)
        await message.answer('<b>🖼 Теперь отправь мне свою фотографию или видео</b>', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Media.media1)


@dp.message(Edit.edite_about)
async def ed_about(message: Message, state: FSMContext):
    true = 1
    if message.text != 'Оставить без описания':
        for i in message.text:
            if i in not_symbols:
                await message.answer('<b>❗️ Не используй специальные символы</b>')
                true = 0
                break
        if true:
            db.set_about(message.text, message.from_user.id)
            await end(message, state)
    else:
        db.set_about('0', message.from_user.id)
        await end(message, state)


@dp.message(F.photo, Media.media1)
async def photo1(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    db.set_media1(photo_id, message.from_user.id)
    db.set_type1(1, message.from_user.id)
    await message.answer('<b>Фото добавлено.</b> Можешь отправить еще 2 или закончить', reply_markup=markups.save)
    await state.set_state(Media.media2)


@dp.message(F.video, Media.media1)
async def video1(message: Message, state: FSMContext):
    video_id = message.video.file_id
    db.set_media1(video_id, message.from_user.id)
    db.set_type1(2, message.from_user.id)
    await message.answer('<b>Видео добавлено.</b> Можешь отправить еще 2 или закончить', reply_markup=markups.save)
    await state.set_state(Media.media2)


@dp.message(Media.media1)
async def error1(message: Message, state: FSMContext):
    if message.text == 'Оставить текущее' and db.get_type1(message.from_user.id) != 0:
        await end(message, state)
    else:
        await message.answer('<b>❗️ Отправь мне фото или видео! Это обязательно</b>')


@dp.message(F.photo, Media.media2)
async def photo2(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    db.set_media2(photo_id, message.from_user.id)
    db.set_type2(1, message.from_user.id)
    await message.answer('<b>Фото добавлено.</b> Можешь отправить еще 1 или закончить', reply_markup=markups.save)
    await state.set_state(Media.media3)


@dp.message(F.video, Media.media2)
async def video2(message: Message, state: FSMContext):
    video_id = message.video.file_id
    db.set_media2(video_id, message.from_user.id)
    db.set_type2(2, message.from_user.id)
    await message.answer('<b>Видео добавлено.</b> Можешь отправить еще 1 или закончить', reply_markup=markups.save)
    await state.set_state(Media.media3)


@dp.message(Media.media2)
async def error2(message: Message, state: FSMContext):
    if message.text == 'Закончить добавление':
        db.set_media2('0', message.from_user.id)
        db.set_type2(0, message.from_user.id)
        db.set_media3('0', message.from_user.id)
        db.set_type3(0, message.from_user.id)
        await end(message, state)
    else:
        await message.answer('<b>❗️ Отправь мне фото или видео! Или заверши добавление</b>')


@dp.message(F.photo, Media.media3)
async def photo3(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    db.set_media3(photo_id, message.from_user.id)
    db.set_type3(1, message.from_user.id)
    await end(message, state)


@dp.message(F.video, Media.media3)
async def video3(message: Message, state: FSMContext):
    video_id = message.video.file_id
    db.set_media3(video_id, message.from_user.id)
    db.set_type3(2, message.from_user.id)
    await end(message, state)


@dp.message(Media.media3)
async def error3(message: Message, state: FSMContext):
    if message.text == 'Закончить добавление':
        db.set_media3('0', message.from_user.id)
        db.set_type3(0, message.from_user.id)
        await end(message, state)
    else:
        await message.answer('<b>❗️ Отправь мне фото или видео! Или заверши добавление</b>')


def year_text(year):
    if year <= 20:
        text = 'лет'
    elif year == 21:
        text = 'год'
    elif 21 < year < 25:
        text = 'года'
    elif year >= 25:
        text = 'лет'
    else:
        text = ''
    return text


def create_form_keyboard(from_user_id: int, count: int | None = None,  form: bool | None = None, not_skip: bool | None = None, id_form: int | None = None, answer_form: bool | None = None):
    inline_keyboard = InlineKeyboardBuilder()
    if answer_form is None and not_skip:
        inline_keyboard.button(text='🎤', callback_data=f'voice-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='💌', callback_data=f'love-mess-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='📹', callback_data=f'video-note-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='❤️', callback_data=f'like-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_form')
        inline_keyboard.adjust(3, 2)
    elif answer_form and not_skip:
        inline_keyboard.button(text='🎤', callback_data=f'answer-voice-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='💌', callback_data=f'answer-love-mess-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='📹', callback_data=f'answer-video-note-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='❤️', callback_data=f'answer-like-form_{from_user_id}_{id_form}')
        inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_answer')
        inline_keyboard.adjust(3, 2)
    elif answer_form:
        if count == 1:
            inline_keyboard.button(text='➡️', callback_data=f'next-med_2_{from_user_id}_1_1_{id_form}')
            inline_keyboard.button(text='🎤', callback_data=f'answer-voice-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='💌', callback_data=f'answer-love-mess-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='📹', callback_data=f'answer-video-note-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='❤️', callback_data=f'answer-like-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_answer')
            inline_keyboard.adjust(1, 3, 2)
        elif count == 2:
            inline_keyboard.button(text='⬅️', callback_data=f'back-med_1_{from_user_id}_1_1_{id_form}')
            inline_keyboard.button(text='➡️', callback_data=f'next-med_3_{from_user_id}_1_1_{id_form}')
            inline_keyboard.button(text='🎤', callback_data=f'answer-voice-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='💌', callback_data=f'answer-love-mess-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='📹', callback_data=f'answer-video-note-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='❤️', callback_data=f'answer-like-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_answer')
            inline_keyboard.adjust(2, 3, 2)
        elif count == 3:
            inline_keyboard.button(text='⬅️', callback_data=f'back-med_1_{from_user_id}_1_1_{id_form}')
            inline_keyboard.button(text='🎤', callback_data=f'answer-voice-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='💌', callback_data=f'answer-love-mess-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='📹', callback_data=f'answer-video-note-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='❤️', callback_data=f'answer-like-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_answer')
            inline_keyboard.adjust(1, 3, 2)
        elif count == 4:
            inline_keyboard.button(text='⬅️', callback_data=f'back-med_2_{from_user_id}_1_1_{id_form}')
            inline_keyboard.button(text='🎤', callback_data=f'answer-voice-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='💌', callback_data=f'answer-love-mess-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='📹', callback_data=f'answer-video-note-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='❤️', callback_data=f'answer-like-form_{from_user_id}_{id_form}')
            inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_answer')
            inline_keyboard.adjust(1, 3, 2)
    else:
        if form is None:
            if count == 1:
                inline_keyboard.button(text='➡️', callback_data=f'next-med_2_{from_user_id}_0')
            elif count == 2:
                inline_keyboard.button(text='⬅️', callback_data=f'back-med_1_{from_user_id}_0')
                inline_keyboard.button(text='➡️', callback_data=f'next-med_3_{from_user_id}_0')
                inline_keyboard.adjust(2)
            elif count == 3:
                inline_keyboard.button(text='⬅️', callback_data=f'back-med_1_{from_user_id}_0')
            elif count == 4:
                inline_keyboard.button(text='⬅️', callback_data=f'back-med_2_{from_user_id}_0')
        else:
            if count == 1:
                inline_keyboard.button(text='➡️', callback_data=f'next-med_2_{from_user_id}_1_0_{id_form}')
                inline_keyboard.button(text='🎤', callback_data=f'voice-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='💌', callback_data=f'love-mess-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='📹', callback_data=f'video-note-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='❤️', callback_data=f'like-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_form')
                inline_keyboard.adjust(1, 3, 2)
            elif count == 2:
                inline_keyboard.button(text='⬅️', callback_data=f'back-med_1_{from_user_id}_1_0_{id_form}')
                inline_keyboard.button(text='➡️', callback_data=f'next-med_3_{from_user_id}_1_0_{id_form}')
                inline_keyboard.button(text='🎤', callback_data=f'voice-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='💌', callback_data=f'love-mess-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='📹', callback_data=f'video-note-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='❤️', callback_data=f'like-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_form')
                inline_keyboard.adjust(2, 3, 2)
            elif count == 3:
                inline_keyboard.button(text='⬅️', callback_data=f'back-med_1_{from_user_id}_1_0_{id_form}')
                inline_keyboard.button(text='🎤', callback_data=f'voice-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='💌', callback_data=f'love-mess-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='📹', callback_data=f'video-note-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='❤️', callback_data=f'like-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_form')
                inline_keyboard.adjust(1, 3, 2)
            elif count == 4:
                inline_keyboard.button(text='⬅️', callback_data=f'back-med_2_{from_user_id}_1_0_{id_form}')
                inline_keyboard.button(text='🎤', callback_data=f'voice-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='💌', callback_data=f'love-mess-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='📹', callback_data=f'video-note-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='❤️', callback_data=f'like-form_{from_user_id}_{id_form}')
                inline_keyboard.button(text='👎', callback_data=f'dis-form_{from_user_id}_{id_form}_form')
                inline_keyboard.adjust(1, 3, 2)

    return inline_keyboard

def delete_message(user_id: int, message_id: int, answer: bool | None = None):
    if answer is None:
        back_inline = [
            [InlineKeyboardButton(text='Вернуться назад', callback_data=f'delete-form-mess_{user_id}_{message_id}_form')]
        ]
    else:
        back_inline = [
            [InlineKeyboardButton(text='Вернуться назад', callback_data=f'delete-form-mess_{user_id}_{message_id}_answer')]
        ]
    back_inline = InlineKeyboardMarkup(inline_keyboard=back_inline)
    return back_inline

async def end(message: Message, state: FSMContext):
    name = db.get_name(message.from_user.id)
    group = db.get_course(message.from_user.id)
    year = db.get_year(message.from_user.id)
    about = db.get_about(message.from_user.id)
    gender = db.get_gender(message.from_user.id)
    media1 = db.get_media1(message.from_user.id)
    type1 = db.get_type1(message.from_user.id)
    type2 = db.get_type2(message.from_user.id)
    type3 = db.get_type3(message.from_user.id)
    if gender == 1 or gender == 3:
        if about != '0':
            text_form = f"<b>👨‍🎓 {name}, {year} {year_text(year)}, {group}</b>\n💭 {about}"
        else:
            text_form = f"<b>👨‍🎓 {name}, {year} {year_text(year)}, {group}</b>"
    else:
        if about != '0':
            text_form = f"<b>👩‍🎓 {name}, {year} {year_text(year)}, {group}</b>\n💭 {about}"
        else:
            text_form = f"<b>👩‍🎓 {name}, {year} {year_text(year)}, {group}</b>"

    db.set_text(text_form, message.from_user.id)

    if type1 != 0:
        if type2 != 0:
            await message.answer('<b>Заполнение анкеты закончено!</b>\n'
                                 'Проверь все ли правильно и выбери действие', reply_markup=markups.save_prof)
            if type1 == 1:
                await bot.send_photo(message.chat.id,
                                     photo=media1,
                                     caption=text_form,
                                     reply_markup=create_form_keyboard(message.from_user.id, 1).as_markup())
            elif type1 == 2:
                await bot.send_video(message.chat.id,
                                     video=media1,
                                     caption=text_form,
                                     reply_markup=create_form_keyboard(message.from_user.id, 1).as_markup())
        else:
            await message.answer('<b>Заполнение анкеты закончено!</b>\n'
                                 'Проверь все ли правильно и выбери действие', reply_markup=markups.save_prof)
            if type1 == 1:
                await bot.send_photo(message.chat.id,
                                     photo=media1,
                                     caption=text_form)
            elif type1 == 2:
                await bot.send_video(message.chat.id,
                                     video=media1,
                                     caption=text_form)
        if type3 != 0:
            len_media = 3
        elif type2 != 0:
            len_media = 2
        else:
            len_media = 1

        if not db.form_exists(message.from_user.id):
            db.add_forms(message.from_user.id, text_form, len_media, gender)
        else:
            db.update_forms(text_form=text_form, len_media=len_media, gender=gender, user_id=message.from_user.id)

        await state.set_state(Media.end)
    else:
        await state.set_state(Media.media1)
        await message.answer('<b>❗️ Отправь мне фото или видео! Это обязательно</b>')


@dp.message(Media.end)
async def finish(message: Message, state: FSMContext):
    if message.text == 'Сохранить':
        await message.answer(texts.main_menu_love, reply_markup=markups.main_love)
        db.set_prof(1, message.from_user.id)
        db.set_active_form(1, message.from_user.id)
        await state.clear()
    elif message.text == 'Изменить анкету':
        await message.answer('<b>Выбери, что бы ты хотел изменить?</b>', reply_markup=markups.edite_prof)
    else:
        await message.answer('❗️ <b>Выбери действие на клавиатуре</b>')


@dp.message(F.text == '👨‍🎓 Профиль')
async def settings(message: Message):
    if message.from_user.username is not None:
        username = f'@{message.from_user.username}'
    else:
        username = '<b>Не задан</b>'
    if db.get_active_form(message.from_user.id) == 1:
        active = 'Да'
        profile = [
            [InlineKeyboardButton(text='Изменить анкету', callback_data='edite_form_prof'),
             InlineKeyboardButton(text='Отключить анкету', callback_data='off_form_prof')],
            [InlineKeyboardButton(text='Показать мою анкету', callback_data=f'answer-mess_{message.from_user.id}_{db.get_id_form(message.from_user.id)}_1')]
        ]
    else:
        active = 'Нет'
        profile = [
            [InlineKeyboardButton(text='Изменить анкету', callback_data='edite_form_prof'),
             InlineKeyboardButton(text='Включить анкету', callback_data='on_form_prof')],
            [InlineKeyboardButton(text='Показать мою анкету', callback_data=f'answer-mess_{message.from_user.id}_{db.get_id_form(message.from_user.id)}_1')]
        ]
    profile = InlineKeyboardMarkup(inline_keyboard=profile)
    mess_text = ('🪪 <b>ТВОЙ ПРОФИЛЬ</b>\n\n'
                 f'<code>ID:</code> <b>{message.from_user.id}</b>\n'
                 f'<code>USERNAME:</code> {username}\n\n'
                 '💌 <b>Статистика твоей анкеты</b>\n'
                 f'<code>АНКЕТА АКТИВНА:</code> <b>{active}</b>\n'
                 f'<code>КОЛ-ВО ПРОСМОТРОВ:</code> <b>{db.get_count_view_form(message.from_user.id)}</b>\n'
                 f'<code>КОЛ-ВО СИМПАТИЙ:</code> <b>{db.get_count_likes(message.from_user.id)}</b>\n\n'
                 '📊 <b>Твоя статистика</b>\n'
                 f'<code>ПРОСМОТРЕННО АНКЕТ:</code> <b>{db.get_count_look_form(message.from_user.id)}</b>\n'
                 f'<code>ПОСТАВЛЕННО СИМПАТИЙ:</code> <b>{db.get_count_my_likes(message.from_user.id)}</b>\n'
                 f'<code>ПОСТАВЛЕННО ДИЗЛАЙКОВ:</code> <b>{db.get_count_my_dislikes(message.from_user.id)}</b>\n\n'
                 '👨‍💻 <b>Управлять анкетой можно ниже</b>')
    await message.answer(text=mess_text, reply_markup=profile)

@dp.message(F.text == '🥱 Устала смотреть')
async def stop_look_forms(message: Message, state: FSMContext):
    await message.answer(texts.main_menu_love, reply_markup=markups.main_love)
    db.active_now(0, user_id=message.from_user.id)
    await state.clear()


@dp.message(F.text == '🥱 Устал смотреть')
async def stop_look_forms(message: Message, state: FSMContext):
    await message.answer(texts.main_menu_love, reply_markup=markups.main_love)
    db.active_now(0, user_id=message.from_user.id)
    await state.clear()


@dp.message(F.text == '💬 Обратная связь')
async def contact(message: Message, state: FSMContext):
    await message.answer(texts.contact_menu, reply_markup=markups.support, disable_web_page_preview=True)
    await state.clear()


@dp.message(F.text == '📋 Расписание НГК')
async def contact(message: Message, state: FSMContext):
    inline_key = [
        [InlineKeyboardButton(text='ПЕРЕЙТИ', url='https://t.me/ngk_robot')]
    ]
    inline_key = InlineKeyboardMarkup(inline_keyboard=inline_key)
    await message.answer('😉 <b>Залетай и смотри по-настоящему удобное расписание</b>\nНе забудь написать боту волшебное слово "Секрет"', reply_markup=inline_key)
    await state.clear()


@dp.message(F.text == '💌 Смотреть анкеты')
async def look_forms(message: Message):
    if db.get_gender(message.from_user.id) == 1:
        view_form = [
            [KeyboardButton(text='🥱 Устал смотреть')]
        ]
    else:
        view_form = [
            [KeyboardButton(text='🥱 Устала смотреть')]
        ]
    view_form = ReplyKeyboardMarkup(keyboard=view_form, resize_keyboard=True)
    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAMEZTbe9WfdKH2shlZ7JN1G92kGw1gAAmc7AAIVprFJ49vTjbQbWbowBA', reply_markup=view_form)
    await forms(message)


async def forms(message: Message):
    if not db.user_exists_love(message.from_user.id) or not db.get_accept(message.from_user.id):
        await message.answer(text=texts.accept_love, reply_markup=markups.accept_love)
    elif not db.get_prof(message.from_user.id):
        await message.answer(f'<b>👋 Приветствую тебя, {message.from_user.first_name}</b>\n\n'
                             f'💖 <b>Я готов помочь найти тебе новые знакомства в нашем колледже!</b>\n\n'
                             f'💌 <b>Давай создадим тебе анкету, для этого нажми на кнопку ниже</b>',
                             reply_markup=markups.create_prof)
    elif db.get_active_form(message.from_user.id) == 0:
        db.active_now(0, user_id=message.from_user.id)
        await message.answer('<b>Твоя анкета неактивна! Для просмотра анкет включи ее в профиле</b>', reply_markup=markups.main_love)
    else:
        form_for_you = db.get_form(message.from_user.id, db.get_interes(message.from_user.id), db.get_course(message.from_user.id))
        if form_for_you:
            db.active_now(1, user_id=message.from_user.id)
            id_form = form_for_you[0]
            user_id = form_for_you[1]
            len_media = form_for_you[-1]
            text_form = form_for_you[2]
            type1 = db.get_type1(user_id)
            media1 = db.get_media1(user_id)
            if user_id == REMOVED_PRIVATE_VALUE:
                if type1 == 1:
                    await bot.send_photo(message.chat.id,
                                         photo=media1,
                                         caption=f'👨‍💻 <b>Админ, 2 курс</b> \n\n'
                                                 f'👋 <b>Привет, {message.from_user.first_name}!</b> '
                                                 f'Если вдруг у тебя возникнут вопросы или что-то не будет работать, то обязательно свяжись с нами, постараемся помочь как можно быстрее.\n\n'
                                                 f'❤️‍🔥 <b>Желаю тебе удачных знакомств!</b>',
                                         reply_markup=create_form_keyboard(from_user_id=user_id, form=True, not_skip=True, id_form=id_form).as_markup(),
                                         protect_content=True)
            elif len_media >= 2:
                if type1 == 1:
                    await bot.send_photo(message.chat.id,
                                         photo=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(count=1, form=True, from_user_id=user_id, id_form=id_form).as_markup(),
                                         protect_content=True)
                elif type1 == 2:
                    await bot.send_video(message.chat.id,
                                         video=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(count=1, form=True, from_user_id=user_id, id_form=id_form).as_markup(),
                                         protect_content=True)
            else:
                if type1 == 1:
                    await bot.send_photo(message.chat.id,
                                         photo=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(from_user_id=user_id, form=True, not_skip=True, id_form=id_form).as_markup(),
                                         protect_content=True)
                elif type1 == 2:
                    await bot.send_video(message.chat.id,
                                         video=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(from_user_id=user_id, form=True, not_skip=True, id_form=id_form).as_markup(),
                                         protect_content=True)
        else:
            db.active_now(0, user_id=message.from_user.id)
            delete_history = [
                [InlineKeyboardButton(text='Очистить историю', callback_data=f'delete-history_{message.from_user.id}'),
                 InlineKeyboardButton(text='Сменить интересы', callback_data='edit_find')],
                [InlineKeyboardButton(text='Главное меню', callback_data='main_menu_love')]
            ]
            delete_history = InlineKeyboardMarkup(inline_keyboard=delete_history)
            await message.answer('<b>😢 К сожалению, по твоим параметрам поиска, анкеты закончились</b>', reply_markup=types.ReplyKeyboardRemove())
            await message.answer('<b>Можешь попробовать изменить интересы поиска или очистить историю просмотренный анкет</b>', reply_markup=delete_history)


class Message_Love(StatesGroup):
    dis = State()
    text = State()
    voice = State()
    video_note = State()

@dp.callback_query(lambda callback: True)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    call_data = callback_query.data.split('_')
    await callback_query.answer()
    if callback_query.data == 'accept_love':
        await callback_query.message.delete()
        db.add_user_love(callback_query.from_user.id)
        db.set_accept(1, callback_query.from_user.id)
        msg = await callback_query.message.answer('<b>Не забывай быть вежливыми, уважать других пользователей и соблюдать правила нашего бота. Мы стремимся создать дружелюбное и безопасное окружение для всех!</b>')
        await asyncio.sleep(6)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=msg.message_id)
        media_group = MediaGroupBuilder(caption="<b>❗️ Пожалуйста проверь, включена ли у тебя пересылка сообщений!</b>\n\n"
                                                "Это необходимо для того, чтобы пользователи могли тебе писать, если будет взаимная симпатия\n\n"
                                                "👉 <b>Настройки</b> ⮕ <b>Конфиденциальность</b> ⮕ <b>Пересылка сообщений</b> ⮕ <b>Кто может ссылаться</b> ⮕ <b>Все</b>")
        media_group.add(type="photo", media=texts.photo1)
        media_group.add(type="photo", media=texts.photo2)
        await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media_group.build())
        await asyncio.sleep(6)
        await callback_query.message.answer(f'<b>👋 Приветствую тебя, {callback_query.from_user.first_name}</b>\n\n'
                                            f'💖 <b>Я готов помочь найти тебе новые знакомства в нашем колледже!</b>\n\n'
                                            f'💌 <b>Давай создадим тебе анкету, для этого нажми на кнопку ниже</b>',
                                            reply_markup=markups.create_prof)
    elif callback_query.data == 'create_prof':
        name_keyboard = [
            [types.KeyboardButton(text=callback_query.from_user.first_name)]
        ]
        name_keyboard = types.ReplyKeyboardMarkup(keyboard=name_keyboard, resize_keyboard=True,
                                                  input_field_placeholder='Введи свое имя')
        await callback_query.message.delete()
        await callback_query.message.answer('<b>💜 Как тебя зовут?</b>', reply_markup=name_keyboard)
        await state.set_state(Create_Prof.name)
    elif callback_query.data == 'main_menu_love':
        await callback_query.message.answer(texts.main_menu_love, reply_markup=markups.main_love)
        await state.clear()
    elif call_data[0] == 'delete-history':
        user_id = int(call_data[1])
        db.delete_view_form(user_id)
        await callback_query.message.answer('<b>Твоя история просмотренных анкет успешно очищена!</b>', reply_markup=markups.main_love)
        await state.clear()
    elif callback_query.data == 'edite_form_prof':
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='<b>🫧 Выбери, что бы ты хотел изменить</b>',
                                    reply_markup=markups.edite_prof)
    elif callback_query.data == 'off_form_prof':
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='<b>Выбери, почему ты хочешь отключить свою анкету</b>',
                                    reply_markup=markups.off_form)
    elif callback_query.data == 'on_form_prof':
        db.set_active_form(1, callback_query.from_user.id)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='<b>🤗 С возвращением!</b>\nТвоя анкета снова стала доступна другим пользователям')
    elif callback_query.data == 'state_yes_new':
        db.set_off_form('Нашел новые знакомства', callback_query.from_user.id)
        db.set_active_form(0, callback_query.from_user.id)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='<b>🤗 Спасибо за мини-отзыв, рад был помочь)</b>\nНадеюсь, у вас, с твоим новым знакомым, все будет хорошо!')
    elif callback_query.data == 'state_not_new':
        db.set_off_form('Не хочет никого искать', callback_query.from_user.id)
        db.set_active_form(0, callback_query.from_user.id)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='<b>🤗 Спасибо за мини-отзыв!</b>\nЕсли станет скучно, обязательно возвращайся, постараюсь помочь найти новые знакомства!')
    elif callback_query.data == 'state_rofl':
        db.set_off_form('По приколу зашел', callback_query.from_user.id)
        db.set_active_form(0, callback_query.from_user.id)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text='<b>🤗 Спасибо за мини-отзыв!</b>\nЖду твоего возвращения, но уже с целью найти новые знакомства, которую я помогу тебе выполнить)')
    elif callback_query.data == 'edite_about':
        await callback_query.message.delete()
        await callback_query.message.answer('<b>💌 Расскажи о себе, о своих интересах, на каком курсе, кого ищешь.</b>\n'
                                            '<b>Это поможет быстрее найти новые знакомства!</b>', reply_markup=markups.ed_about)
        db.set_active_form(0, callback_query.from_user.id)
        await state.set_state(Edit.edite_about)
    elif callback_query.data == 'edit_find':
        await callback_query.message.delete()
        await callback_query.message.answer('<b>🫰 Чьи анкеты хочешь смотреть?</b>', reply_markup=markups.interes)
        db.set_active_form(0, callback_query.from_user.id)
        await state.set_state(Edit.edit_find)
    elif callback_query.data == 'edite_name':
        name_keyboard = [
            [types.KeyboardButton(text=callback_query.from_user.first_name)]
        ]
        name_keyboard = types.ReplyKeyboardMarkup(keyboard=name_keyboard, resize_keyboard=True,
                                                  input_field_placeholder='Введи свое имя')
        await callback_query.message.delete()
        await callback_query.message.answer('<b>💜 Как тебя зовут?</b>', reply_markup=name_keyboard)
        db.set_active_form(0, callback_query.from_user.id)
        await state.set_state(Edit.edite_name)
    elif callback_query.data == 'edite_group':
        course = [
            [KeyboardButton(text='1 корпус'),
             KeyboardButton(text='2 корпус'),
             KeyboardButton(text='3 корпус')]
        ]
        course = ReplyKeyboardMarkup(keyboard=course, resize_keyboard=True)
        await callback_query.message.delete()
        await callback_query.message.answer('<b>👨‍🎓 В каком корпусе учишься?</b>', reply_markup=course)
        db.set_active_form(0, callback_query.from_user.id)
        await state.set_state(Edit.edite_group)
    elif callback_query.data == 'edite_media':
        name_keyboard = [
            [types.KeyboardButton(text='Оставить текущее')]
        ]
        name_keyboard = types.ReplyKeyboardMarkup(keyboard=name_keyboard, resize_keyboard=True,
                                                  input_field_placeholder='Введи свое имя')
        await callback_query.message.delete()
        await callback_query.message.answer('<b>🖼 Отправь мне свою фотографию или видео</b>',
                                            reply_markup=name_keyboard)
        db.set_active_form(0, callback_query.from_user.id)
        await state.set_state(Media.media1)

    elif callback_query.data == 'edite_all':
        name_keyboard = [
            [types.KeyboardButton(text=callback_query.from_user.first_name)]
        ]
        name_keyboard = types.ReplyKeyboardMarkup(keyboard=name_keyboard, resize_keyboard=True,
                                                  input_field_placeholder='Введи свое имя')
        await callback_query.message.delete()
        await callback_query.message.answer('<b>💜 Как тебя зовут?</b>', reply_markup=name_keyboard)
        db.set_active_form(0, callback_query.from_user.id)
        await state.set_state(Create_Prof.name)
    elif call_data[0] == 'delete-form-mess':
        await state.clear()
        len_media = db.get_len_media(call_data[1])
        type1 = db.get_type1(call_data[1])
        id_form = db.get_id_form(call_data[1])
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        if call_data[3] == 'form':
            if len_media >= 2:
                if type1 == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], 1, form=True, id_form=id_form).as_markup())
                elif type1 == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], 1, form=True, id_form=id_form).as_markup())
            else:
                if type1 == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], form=True, id_form=id_form, not_skip=True).as_markup())
                elif type1 == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], form=True, id_form=id_form, not_skip=True).as_markup())
        else:
            if len_media >= 2:
                if type1 == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], 1, form=True, id_form=id_form, answer_form=True).as_markup())
                elif type1 == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], 1, form=True, id_form=id_form, answer_form=True).as_markup())
            else:
                if type1 == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], form=True, id_form=id_form, not_skip=True, answer_form=True).as_markup())
                elif type1 == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=int(call_data[2]),
                                                 media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                       caption=db.get_text(call_data[1])),
                                                 reply_markup=create_form_keyboard(call_data[1], form=True, id_form=id_form, not_skip=True, answer_form=True).as_markup())

    elif call_data[0] == 'like-form':
        db.set_view_form(id_form=int(call_data[2]), user_id_form=int(call_data[1]), user_id=callback_query.from_user.id, value=1)
        form_for_you = db.get_form(callback_query.from_user.id, db.get_interes(callback_query.from_user.id), db.get_course(callback_query.from_user.id))
        len_media_form = db.get_len_media(call_data[1])
        type1_form = db.get_type1(call_data[1])
        if len_media_form >= 2:
            if type1_form == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1_form == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1_form == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])))
            elif type1_form == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])))
        if form_for_you:
            id_form = form_for_you[0]
            user_id = form_for_you[1]
            len_media = form_for_you[-1]
            text_form = form_for_you[2]
            type1 = db.get_type1(user_id)
            media1 = db.get_media1(user_id)
            if len_media >= 2:
                if type1 == 1:
                    await bot.send_photo(callback_query.from_user.id,
                                         photo=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(count=1, form=True, from_user_id=user_id,
                                                                           id_form=id_form).as_markup(),
                                         protect_content=True)
                elif type1 == 2:
                    await bot.send_video(callback_query.from_user.id,
                                         video=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(count=1, form=True, from_user_id=user_id,
                                                                           id_form=id_form).as_markup(),
                                         protect_content=True)
            else:
                if type1 == 1:
                    await bot.send_photo(callback_query.from_user.id,
                                         photo=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(from_user_id=user_id, form=True,
                                                                           not_skip=True,
                                                                           id_form=id_form).as_markup(),
                                         protect_content=True)
                elif type1 == 2:
                    await bot.send_video(callback_query.from_user.id,
                                         video=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(from_user_id=user_id, form=True,
                                                                           not_skip=True,
                                                                           id_form=id_form).as_markup(),
                                         protect_content=True)
        else:
            db.active_now(0, user_id=callback_query.from_user.id)
            delete_history = [
                [InlineKeyboardButton(text='Очистить историю', callback_data=f'delete-history_{callback_query.from_user.id}'),
                 InlineKeyboardButton(text='Сменить интересы', callback_data='edit_find')],
                [InlineKeyboardButton(text='Главное меню', callback_data='main_menu_love')]
            ]
            delete_history = InlineKeyboardMarkup(inline_keyboard=delete_history)
            await callback_query.message.answer('<b>😢 К сожалению, по твоим параметрам поиска, анкеты закончились</b>',
                                                reply_markup=types.ReplyKeyboardRemove())
            await callback_query.message.answer(
                '<b>Можешь попробовать изменить интересы поиска или очистить историю просмотренный анкет</b>',
                reply_markup=delete_history)

        markup_who = [
            [InlineKeyboardButton(text='ПОКАЖИ',
                                  callback_data=f'answer-mess_{callback_query.from_user.id}_{db.get_id_form(callback_query.from_user.id)}_0')]
        ]
        markup_who = InlineKeyboardMarkup(inline_keyboard=markup_who)
        try:
            await bot.send_photo(chat_id=call_data[1], photo=texts.photo3,
                                 caption=f'<b>🤩 К тебе проявили симпатию!\n\n😏 Показать его/ее анкету?</b>',
                                 reply_markup=markup_who)
        except:
            pass

    elif call_data[0] == 'answer-like-form':
        db.set_view_form(id_form=int(call_data[2]), user_id_form=int(call_data[1]), user_id=callback_query.from_user.id, value=1)
        len_media_form = db.get_len_media(call_data[1])
        type1_form = db.get_type1(call_data[1])
        if len_media_form >= 2:
            if type1_form == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1_form == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1_form == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])))
            elif type1_form == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])))
        await callback_query.message.answer(
            f'<b>🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨<a href="tg://user?id={int(call_data[1])}">{db.get_name(int(call_data[1]))}</a>✨</b>')

        if db.get_gender(callback_query.from_user.id) == 1:
            markup_who = [
                [InlineKeyboardButton(text=f'Напомнить его анкету',
                                      callback_data=f'answer-mess_{callback_query.from_user.id}_{db.get_id_form(callback_query.from_user.id)}_1')]
            ]
            markup_who = InlineKeyboardMarkup(inline_keyboard=markup_who)
        else:
            markup_who = [
                [InlineKeyboardButton(text=f'Напомнить ее анкету',
                                      callback_data=f'answer-mess_{callback_query.from_user.id}_{db.get_id_form(callback_query.from_user.id)}_1')]
            ]
            markup_who = InlineKeyboardMarkup(inline_keyboard=markup_who)
        try:
            if callback_query.from_user.username is not None:
                url_user = f'<a href="https://t.me/{callback_query.from_user.username}">{db.get_name(callback_query.from_user.id)}</a>'
            else:
                url_user = f'<a href="tg://user?id={callback_query.from_user.id}">{db.get_name(callback_query.from_user.id)}</a>'

            await bot.send_photo(chat_id=call_data[1], photo=texts.photo6,
                                 caption=f'<b>🤩 У тебя появилась взаимная симпатия\n\n🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨{url_user}✨</b>', reply_markup=markup_who)
        except:
            pass
    elif call_data[0] == 'dis-form':
        db.set_view_form(id_form=int(call_data[2]), user_id_form=int(call_data[1]), user_id=callback_query.from_user.id, value=0)
        len_media_form = db.get_len_media(call_data[1])
        type1_form = db.get_type1(call_data[1])
        if len_media_form >= 2:
            if type1_form == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1_form == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1_form == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])))
            elif type1_form == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=db.get_media1(call_data[1]),
                                                                   caption=db.get_text(call_data[1])))
        if call_data[-1] == 'form':
            form_for_you = db.get_form(callback_query.from_user.id, db.get_interes(callback_query.from_user.id), db.get_course(callback_query.from_user.id))
            if form_for_you:
                id_form = form_for_you[0]
                user_id = form_for_you[1]
                len_media = form_for_you[-1]
                text_form = form_for_you[2]
                type1 = db.get_type1(user_id)
                media1 = db.get_media1(user_id)
                if len_media >= 2:
                    if type1 == 1:
                        await bot.send_photo(callback_query.from_user.id,
                                             photo=media1,
                                             caption=text_form,
                                             reply_markup=create_form_keyboard(count=1, form=True, from_user_id=user_id,
                                                                               id_form=id_form).as_markup(),
                                             protect_content=True)
                    elif type1 == 2:
                        await bot.send_video(callback_query.from_user.id,
                                             video=media1,
                                             caption=text_form,
                                             reply_markup=create_form_keyboard(count=1, form=True, from_user_id=user_id,
                                                                               id_form=id_form).as_markup(),
                                             protect_content=True)
                else:
                    if type1 == 1:
                        await bot.send_photo(callback_query.from_user.id,
                                             photo=media1,
                                             caption=text_form,
                                             reply_markup=create_form_keyboard(from_user_id=user_id, form=True,
                                                                               not_skip=True,
                                                                               id_form=id_form).as_markup(),
                                             protect_content=True)
                    elif type1 == 2:
                        await bot.send_video(callback_query.from_user.id,
                                             video=media1,
                                             caption=text_form,
                                             reply_markup=create_form_keyboard(from_user_id=user_id, form=True,
                                                                               not_skip=True,
                                                                               id_form=id_form).as_markup(),
                                             protect_content=True)
            else:
                db.active_now(0, user_id=callback_query.from_user.id)
                delete_history = [
                    [InlineKeyboardButton(text='Очистить историю',
                                          callback_data=f'delete-history_{callback_query.from_user.id}'),
                     InlineKeyboardButton(text='Сменить интересы', callback_data='edit_find')],
                    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu_love')]
                ]
                delete_history = InlineKeyboardMarkup(inline_keyboard=delete_history)
                await callback_query.message.answer(
                    '<b>😢 К сожалению, по твоим параметрам поиска, анкеты закончились</b>',
                    reply_markup=types.ReplyKeyboardRemove())
                await callback_query.message.answer(
                    '<b>Можешь попробовать изменить интересы поиска или очистить историю просмотренный анкет</b>',
                    reply_markup=delete_history)

    elif call_data[0] == 'video-note-form':
        message_id = callback_query.message.message_id
        len_media = db.get_len_media(call_data[1])
        text_form = db.get_text(call_data[1])
        type1 = db.get_type1(call_data[1])
        media1 = db.get_media1(call_data[1])
        if len_media >= 2:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form))
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form))
        msg = await callback_query.message.answer('📹 <b>Запиши кружок для этого пользователя</b>', reply_markup=delete_message(int(call_data[1]), message_id))
        await state.update_data(user_id=int(call_data[1]))
        await state.update_data(id_form=int(call_data[2]))
        await state.update_data(my_id_form=db.get_id_form(callback_query.from_user.id))
        await state.update_data(answer=0)
        await state.update_data(mes_id=msg.message_id)
        await state.set_state(Message_Love.video_note)
    elif call_data[0] == 'answer-video-note-form':
        message_id = callback_query.message.message_id
        len_media = db.get_len_media(call_data[1])
        text_form = db.get_text(call_data[1])
        type1 = db.get_type1(call_data[1])
        media1 = db.get_media1(call_data[1])
        if len_media >= 2:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form))
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form))
        msg = await callback_query.message.answer('📹 <b>Запиши кружок для этого пользователя</b>', reply_markup=delete_message(int(call_data[1]), message_id, True))
        await state.update_data(user_id=int(call_data[1]))
        await state.update_data(id_form=int(call_data[2]))
        await state.update_data(my_id_form=db.get_id_form(callback_query.from_user.id))
        await state.update_data(answer=1)
        await state.update_data(mes_id=msg.message_id)
        await state.set_state(Message_Love.video_note)

    elif call_data[0] == 'love-mess-form':
        message_id = callback_query.message.message_id
        len_media = db.get_len_media(call_data[1])
        text_form = db.get_text(call_data[1])
        type1 = db.get_type1(call_data[1])
        media1 = db.get_media1(call_data[1])
        if len_media >= 2:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form))
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form))
        msg = await callback_query.message.answer('💌 <b>Напиши валентинку для этого пользователя</b>',
                                                  reply_markup=delete_message(int(call_data[1]), message_id))
        await state.update_data(user_id=int(call_data[1]))
        await state.update_data(id_form=int(call_data[2]))
        await state.update_data(my_id_form=db.get_id_form(callback_query.from_user.id))
        await state.update_data(answer=0)
        await state.update_data(mes_id=msg.message_id)
        await state.set_state(Message_Love.text)
    elif call_data[0] == 'answer-love-mess-form':
        message_id = callback_query.message.message_id
        len_media = db.get_len_media(call_data[1])
        text_form = db.get_text(call_data[1])
        type1 = db.get_type1(call_data[1])
        media1 = db.get_media1(call_data[1])
        if len_media >= 2:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form))
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form))
        msg = await callback_query.message.answer('💌 <b>Напиши валентинку для этого пользователя</b>',
                                                  reply_markup=delete_message(int(call_data[1]), message_id, True))
        await state.update_data(user_id=int(call_data[1]))
        await state.update_data(id_form=int(call_data[2]))
        await state.update_data(my_id_form=db.get_id_form(callback_query.from_user.id))
        await state.update_data(answer=1)
        await state.update_data(mes_id=msg.message_id)
        await state.set_state(Message_Love.text)

    elif call_data[0] == 'voice-form':
        message_id = callback_query.message.message_id
        len_media = db.get_len_media(call_data[1])
        text_form = db.get_text(call_data[1])
        type1 = db.get_type1(call_data[1])
        media1 = db.get_media1(call_data[1])
        if len_media >= 2:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form))
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form))
        msg = await callback_query.message.answer('🎤 <b>Запиши голосовое сообщение для этого пользователя</b>', reply_markup=delete_message(int(call_data[1]), message_id))
        await state.update_data(user_id=int(call_data[1]))
        await state.update_data(id_form=int(call_data[2]))
        await state.update_data(my_id_form=db.get_id_form(callback_query.from_user.id))
        await state.update_data(answer=0)
        await state.update_data(mes_id=msg.message_id)
        await state.set_state(Message_Love.voice)
    elif call_data[0] == 'answer-voice-form':
        message_id = callback_query.message.message_id
        len_media = db.get_len_media(call_data[1])
        text_form = db.get_text(call_data[1])
        type1 = db.get_type1(call_data[1])
        media1 = db.get_media1(call_data[1])
        if len_media >= 2:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form),
                                             reply_markup=create_form_keyboard(call_data[1], 1).as_markup())
        else:
            if type1 == 1:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaPhoto(media=media1,
                                                                   caption=text_form))
            elif type1 == 2:
                await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id,
                                             media=InputMediaVideo(media=media1,
                                                                   caption=text_form))
        msg = await callback_query.message.answer('🎤 <b>Запиши голосовое сообщение для этого пользователя</b>', reply_markup=delete_message(int(call_data[1]), message_id, True))
        await state.update_data(user_id=int(call_data[1]))
        await state.update_data(id_form=int(call_data[2]))
        await state.update_data(my_id_form=db.get_id_form(callback_query.from_user.id))
        await state.update_data(answer=1)
        await state.update_data(mes_id=msg.message_id)
        await state.set_state(Message_Love.voice)

    elif call_data[0] == 'answer-mess':
        from_id = int(call_data[1])
        id_form = int(call_data[2])
        len_media = db.get_len_media(from_id)
        text_form = db.get_text(from_id)
        type1 = db.get_type1(from_id)
        media1 = db.get_media1(from_id)
        if call_data[3] == '0':
            if len_media >= 2:
                if type1 == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaPhoto(media=media1,
                                                                       caption=text_form),
                                                 reply_markup=create_form_keyboard(count=1, form=True,
                                                                                   from_user_id=from_id,
                                                                                   id_form=id_form,
                                                                                   answer_form=True).as_markup())
                elif type1 == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaVideo(media=media1,
                                                                       caption=text_form),
                                                 reply_markup=create_form_keyboard(count=1, form=True,
                                                                                   from_user_id=from_id,
                                                                                   id_form=id_form,
                                                                                   answer_form=True).as_markup())
            else:
                if type1 == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaPhoto(media=media1,
                                                                       caption=text_form),
                                                 reply_markup=create_form_keyboard(from_user_id=from_id, form=True,
                                                                                   not_skip=True, id_form=id_form,
                                                                                   answer_form=True).as_markup())
                elif type1 == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaVideo(media=media1,
                                                                       caption=text_form),
                                                 reply_markup=create_form_keyboard(from_user_id=from_id, form=True,
                                                                                   not_skip=True, id_form=id_form,
                                                                                   answer_form=True).as_markup())
        else:
            if len_media >= 2:
                if type1 == 1:
                    await bot.send_photo(callback_query.from_user.id,
                                         photo=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(count=1,
                                                                           from_user_id=from_id).as_markup(),
                                         protect_content=True)
                elif type1 == 2:
                    await bot.send_video(callback_query.from_user.id,
                                         video=media1,
                                         caption=text_form,
                                         reply_markup=create_form_keyboard(count=1,
                                                                           from_user_id=from_id,).as_markup(),
                                         protect_content=True)
            else:
                if type1 == 1:
                    await bot.send_photo(callback_query.from_user.id,
                                         photo=media1,
                                         caption=text_form,
                                         protect_content=True)
                elif type1 == 2:
                    await bot.send_video(callback_query.from_user.id,
                                         video=media1,
                                         caption=text_form,
                                         protect_content=True)

    elif call_data[0] == 'next-med':
        call_data[2] = int(call_data[2])
        if call_data[3] == '0':
            if call_data[1] == '2':
                media = db.get_media2(call_data[2])
                if db.get_type2(call_data[2]) == 1:
                    if db.get_type3(call_data[2]) == 0:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 3).as_markup())
                    else:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 2).as_markup())
                elif db.get_type2(call_data[2]) == 2:
                    if db.get_type3(call_data[2]) == 0:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 3).as_markup())
                    else:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 3).as_markup())
            elif call_data[1] == '3':
                media = db.get_media3(call_data[2])
                if db.get_type3(call_data[2]) == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaPhoto(media=media,
                                                                       caption=db.get_text(call_data[2])),
                                                 reply_markup=create_form_keyboard(call_data[2], 4).as_markup())
                elif db.get_type3(call_data[2]) == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaVideo(media=media,
                                                                       caption=db.get_text(call_data[2])),
                                                 reply_markup=create_form_keyboard(call_data[2], 4).as_markup())

        else:
            if call_data[4] == '0':
                if call_data[1] == '2':
                    media = db.get_media2(call_data[2])
                    if db.get_type2(call_data[2]) == 1:
                        if db.get_type3(call_data[2]) == 0:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaPhoto(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 3, form=True, id_form=int(call_data[5])).as_markup())
                        else:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaPhoto(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 2, form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type2(call_data[2]) == 2:
                        if db.get_type3(call_data[2]) == 0:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaVideo(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 3, form=True, id_form=int(call_data[5])).as_markup())
                        else:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaVideo(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 2, form=True, id_form=int(call_data[5])).as_markup())
                elif call_data[1] == '3':
                    media = db.get_media3(call_data[2])
                    if db.get_type3(call_data[2]) == 1:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 4, form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type3(call_data[2]) == 2:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 4, form=True, id_form=int(call_data[5])).as_markup())

            else:
                if call_data[1] == '2':
                    media = db.get_media2(call_data[2])
                    if db.get_type2(call_data[2]) == 1:
                        if db.get_type3(call_data[2]) == 0:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaPhoto(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 3, form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                        else:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaPhoto(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 2, form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type2(call_data[2]) == 2:
                        if db.get_type3(call_data[2]) == 0:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaVideo(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 3, form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                        else:
                            await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                         message_id=callback_query.message.message_id,
                                                         media=InputMediaVideo(media=media,
                                                                               caption=db.get_text(call_data[2])),
                                                         reply_markup=create_form_keyboard(call_data[2], 2, form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                elif call_data[1] == '3':
                    media = db.get_media3(call_data[2])
                    if db.get_type3(call_data[2]) == 1:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 4, form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type3(call_data[2]) == 2:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 4, form=True, answer_form=True, id_form=int(call_data[5])).as_markup())

    elif call_data[0] == 'back-med':
        call_data[2] = int(call_data[2])
        if call_data[3] == '0':
            if call_data[1] == '2':
                media = db.get_media2(call_data[2])
                if db.get_type2(call_data[2]) == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaPhoto(media=media,
                                                                       caption=db.get_text(call_data[2])),
                                                 reply_markup=create_form_keyboard(call_data[2], 2).as_markup())
                elif db.get_type2(call_data[2]) == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaVideo(media=media,
                                                                       caption=db.get_text(call_data[2])),
                                                 reply_markup=create_form_keyboard(call_data[2], 2).as_markup())
            elif call_data[1] == '1':
                media = db.get_media1(call_data[2])
                if db.get_type1(call_data[2]) == 1:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaPhoto(media=media,
                                                                       caption=db.get_text(call_data[2])),
                                                 reply_markup=create_form_keyboard(call_data[2], 1).as_markup())
                elif db.get_type1(call_data[2]) == 2:
                    await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                 message_id=callback_query.message.message_id,
                                                 media=InputMediaVideo(media=media,
                                                                       caption=db.get_text(call_data[2])),
                                                 reply_markup=create_form_keyboard(call_data[2], 1).as_markup())

        else:
            if call_data[4] == '0':
                if call_data[1] == '2':
                    media = db.get_media2(call_data[2])
                    if db.get_type2(call_data[2]) == 1:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 2, form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type2(call_data[2]) == 2:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 2, form=True, id_form=int(call_data[5])).as_markup())
                elif call_data[1] == '1':
                    media = db.get_media1(call_data[2])
                    if db.get_type1(call_data[2]) == 1:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 1, form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type1(call_data[2]) == 2:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 1, form=True, id_form=int(call_data[5])).as_markup())
            else:
                if call_data[1] == '2':
                    media = db.get_media2(call_data[2])
                    if db.get_type2(call_data[2]) == 1:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 2,
                                                                                       form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type2(call_data[2]) == 2:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 2,
                                                                                       form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                elif call_data[1] == '1':
                    media = db.get_media1(call_data[2])
                    if db.get_type1(call_data[2]) == 1:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaPhoto(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 1,
                                                                                       form=True, answer_form=True, id_form=int(call_data[5])).as_markup())
                    elif db.get_type1(call_data[2]) == 2:
                        await bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                     message_id=callback_query.message.message_id,
                                                     media=InputMediaVideo(media=media,
                                                                           caption=db.get_text(call_data[2])),
                                                     reply_markup=create_form_keyboard(call_data[2], 1,
                                                                                       form=True, answer_form=True, id_form=int(call_data[5])).as_markup())


@dp.message(Message_Love.text, F.text)
async def mes_love_text(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    user_id = data['user_id']
    id_form = data['id_form']
    my_id_form = data['my_id_form']
    answer = data['answer']
    mes_id = data['mes_id']
    await bot.delete_message(chat_id=message.chat.id, message_id=mes_id)
    if answer == 0:
        markup_mess_who = [
            [InlineKeyboardButton(text='ПОКАЖИ',
                                  callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_0')]
        ]
        markup_mess_who = InlineKeyboardMarkup(inline_keyboard=markup_mess_who)
        try:
            await bot.send_photo(chat_id=user_id, photo=texts.photo5,
                                 caption=f'<b>🤩 Тебя оценили и даже отправили валентинку\n\n💌 :</b> <span class="tg-spoiler">{text}</span>\n\n<b>😏 Показать его/ее анкету?</b>',
                                 reply_markup=markup_mess_who)
        except:
            pass
        await message.reply('<b>😏 Твоя валентинка отправлена!\n\n❤️‍🔥 Погнали дальше</b>')
        db.set_view_form(id_form=id_form, user_id_form=user_id, user_id=message.from_user.id, value=1)

        await forms(message)
    else:
        try:
            if message.from_user.username is not None:
                url_user = f'<a href="https://t.me/{message.from_user.username}">{db.get_name(message.from_user.id)}</a>'
            else:
                url_user = f'<a href="tg://user?id={message.from_user.id}">{db.get_name(message.from_user.id)}</a>'
            await bot.send_photo(chat_id=user_id, photo=texts.photo6,
                                 caption=f'<b>🤩 У тебя появилась взаимная симпатия\n\n🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨{url_user}✨</b>')
        except:
            pass
        if db.get_gender(message.from_user.id) == 1:
            markup_mess_who = [
                [InlineKeyboardButton(text=f'Напомнить его анкету',
                                      callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_1')]
            ]
            markup_mess_who = InlineKeyboardMarkup(inline_keyboard=markup_mess_who)
            try:
                await bot.send_message(user_id, f'<b>😏 {db.get_name(message.from_user.id)} тебе еще отправил валентинку\n\n💌 :</b> <span class="tg-spoiler">{text}</span>', reply_markup=markup_mess_who)
            except:
                pass
        else:
            markup_mess_who = [
                [InlineKeyboardButton(text=f'Напомнить ее анкету',
                                      callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_1')]
            ]
            markup_mess_who = InlineKeyboardMarkup(inline_keyboard=markup_mess_who)
            try:
                await bot.send_message(user_id, f'<b>😏 {db.get_name(message.from_user.id)} тебе еще отправила валентинку:</b>\n\n💌 <code>{text}</code>', reply_markup=markup_mess_who)
            except:
                pass
        await message.reply('<b>😏 Твоя валентинка отправлена!</b>')
        await message.answer(
            f'<b>🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨<a href="tg://user?id={user_id}">{db.get_name(user_id)}</a>✨</b>')
        db.set_view_form(id_form=id_form, user_id_form=user_id, user_id=message.from_user.id, value=1)

    await state.clear()


@dp.message(Message_Love.text)
async def mes_love_text_err(message: Message):
    await message.answer('<b>Отправь мне текстовую валентинку!</b>')

@dp.message(Message_Love.video_note, F.video_note)
async def mes_love_video_note(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    id_form = data['id_form']
    my_id_form = data['my_id_form']
    answer = data['answer']
    mes_id = data['mes_id']
    await bot.delete_message(chat_id=message.chat.id, message_id=mes_id)
    video_note_id = message.video_note.file_id
    if answer == 0:
        markup_video_note = [
            [InlineKeyboardButton(text='ПОКАЖИ',
                                  callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_0')]
        ]
        markup_video_note = InlineKeyboardMarkup(inline_keyboard=markup_video_note)
        try:
            await bot.send_photo(chat_id=user_id, photo=texts.photo4,
                                 caption='<b>🤩 Тебя оценили и даже отправили кружок!\n\n😏 Показать его/ее анкету?</b>',
                                 reply_markup=markup_video_note)
            await bot.send_video_note(user_id, video_note=video_note_id, reply_markup=markup_video_note)
        except:
            pass
        await message.reply('<b>😏 Твой кружок отправлен!\n\n❤️‍🔥 Погнали дальше</b>')
        db.set_view_form(id_form=id_form, user_id_form=user_id, user_id=message.from_user.id, value=1)

        await forms(message)
    else:
        try:
            if message.from_user.username is not None:
                url_user = f'<a href="https://t.me/{message.from_user.username}">{db.get_name(message.from_user.id)}</a>'
            else:
                url_user = f'<a href="tg://user?id={message.from_user.id}">{db.get_name(message.from_user.id)}</a>'
            await bot.send_photo(chat_id=user_id, photo=texts.photo6,
                                 caption=f'<b>🤩 У тебя появилась взаимная симпатия\n\n🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨{url_user}✨</b>')
        except:
            pass
        if db.get_gender(message.from_user.id) == 1:
            markup_video_note = [
                [InlineKeyboardButton(text=f'Напомнить его анкету',
                                      callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_1')]
            ]
            markup_video_note = InlineKeyboardMarkup(inline_keyboard=markup_video_note)
            try:
                await bot.send_message(user_id, f'<b>😏 {db.get_name(message.from_user.id)} тебе еще отправил кружок</b>')
                await bot.send_video_note(user_id, video_note=video_note_id, reply_markup=markup_video_note)
            except:
                pass
        else:
            markup_video_note = [
                [InlineKeyboardButton(text=f'Напомнить ее анкету',
                                      callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_1')]
            ]
            markup_video_note = InlineKeyboardMarkup(inline_keyboard=markup_video_note)
            try:
                await bot.send_message(user_id, f'<b>😏 {db.get_name(message.from_user.id)} тебе еще отправила кружок</b>')
                await bot.send_video_note(user_id, video_note=video_note_id, reply_markup=markup_video_note)
            except:
                pass

        await message.reply('<b>😏 Твое кружок отправлен!</b>')
        await message.answer(
            f'<b>🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨<a href="tg://user?id={user_id}">{db.get_name(user_id)}</a>✨</b>')
        db.set_view_form(id_form=id_form, user_id_form=user_id, user_id=message.from_user.id, value=1)

    await state.clear()


@dp.message(Message_Love.video_note)
async def mes_love_video_note_err(message: Message):
    await message.answer('<b>Отправь мне именно кружок!</b>')


@dp.message(Message_Love.voice, F.voice)
async def mes_love_voice(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    id_form = data['id_form']
    my_id_form = data['my_id_form']
    answer = data['answer']
    mes_id = data['mes_id']
    await bot.delete_message(chat_id=message.chat.id, message_id=mes_id)
    voice_id = message.voice.file_id
    if answer == 0:
        voice_key = [
            [InlineKeyboardButton(text='ПОКАЖИ', callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_0')]
        ]
        voice_key = InlineKeyboardMarkup(inline_keyboard=voice_key)
        try:
            await bot.send_photo(chat_id=user_id, photo=texts.photo4,
                                 caption='<b>🤩 Тебя оценили и даже отправили голосовое сообщение!\n\n😏 Показать его/ее анкету?</b>',
                                 reply_markup=voice_key)

            await bot.send_voice(user_id, voice=voice_id, reply_markup=voice_key)
        except:
            pass
        await message.reply('<b>😏 Твое голосовое сообщение отправлено!\n\n❤️‍🔥 Погнали дальше</b>')
        db.set_view_form(id_form=id_form, user_id_form=user_id, user_id=message.from_user.id, value=1)

        await forms(message)
    else:
        try:
            if message.from_user.username is not None:
                url_user = f'<a href="https://t.me/{message.from_user.username}">{db.get_name(message.from_user.id)}</a>'
            else:
                url_user = f'<a href="tg://user?id={message.from_user.id}">{db.get_name(message.from_user.id)}</a>'
            await bot.send_photo(chat_id=user_id, photo=texts.photo6,
                                 caption=f'<b>🤩 У тебя появилась взаимная симпатия\n\n🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨{url_user}✨</b>')
        except:
            pass
        if db.get_gender(message.from_user.id) == 1:
            voice_key = [
                [InlineKeyboardButton(text=f'Напомнить его анкету',
                                      callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_1')]
            ]
            voice_key = InlineKeyboardMarkup(inline_keyboard=voice_key)
            try:
                await bot.send_voice(user_id, voice=voice_id, reply_markup=voice_key,
                                     caption=f'<b>😏 {db.get_name(message.from_user.id)} тебе еще отправил голосовое сообщение</b>')
            except:
                pass
        else:
            voice_key = [
                [InlineKeyboardButton(text=f'Напомнить ее анкету',
                                      callback_data=f'answer-mess_{message.from_user.id}_{my_id_form}_1')]
            ]
            voice_key = InlineKeyboardMarkup(inline_keyboard=voice_key)
            try:
                await bot.send_voice(user_id, voice=voice_id, reply_markup=voice_key,
                                     caption=f'<b>😏 {db.get_name(message.from_user.id)} тебе еще отправила голосовое сообщение</b>')
            except:
                pass
            await message.reply('<b>😏 Твое голосовое сообщение отправлено!</b>')
            await message.answer(f'<b>🤗 Начинай общаться, надеюсь у вас все будет хорошо!\n\n✨<a href="tg://user?id={user_id}">{db.get_name(user_id)}</a>✨</b>')

        db.set_view_form(id_form=id_form, user_id_form=user_id, user_id=message.from_user.id, value=1)

    await state.clear()


@dp.message(Message_Love.voice)
async def mes_love_voice_err(message: Message):
    await message.answer('<b>Отправь мне именно голосовое сообщение!</b>')


@dp.message(F.text == '🔝 Главное меню')
async def main_menu(message: Message, state: FSMContext):
    await message.answer(texts.main_menu_love, reply_markup=markups.main_love)
    await state.clear()


@dp.message(Command('admin'))
async def admin_panel(message: Message):
    if message.from_user.id == REMOVED_PRIVATE_VALUE or message.from_user.id == REMOVED_PRIVATE_VALUE:
        await message.answer('👑 Добро пожаловать, дорогой админ', reply_markup=markups.admin_panel_love)
    else:
        await message.answer('<b>❣️ Такая команда доступна только админу</b>')


@dp.message(F.text == '🔝 В Админ панель')
async def back_adm(message: Message, state: FSMContext):
    if message.from_user.id == REMOVED_PRIVATE_VALUE or message.from_user.id == REMOVED_PRIVATE_VALUE:
        await message.answer('👑 Добро пожаловать, дорогой админ', reply_markup=markups.admin_panel_love)
        await state.clear()


@dp.message(F.text == '📊 Статистика')
async def statistics(message: Message):
    if message.from_user.id == REMOVED_PRIVATE_VALUE or message.from_user.id == REMOVED_PRIVATE_VALUE:
        count_user = list(db.get_all_users_love())
        stats = ('📊 <b>АКТУАЛЬНАЯ СТАТИСТИКА</b>\n\n'
                 f'<code>ПОЛЬЗОВАТЕЛЕЙ В БОТЕ:</code> <b>{len(count_user)}</b>\n'
                 f'<code>ПОЛЬЗОВАТЕЛЕЙ С АНКЕТОЙ:</code> <b>{len(db.get_users_prof_love())}</b>\n'
                 f'<code>ПАРНЕЙ В БОТЕ:</code> <b>{len(db.get_users_gender_love(1))}</b>\n'
                 f'<code>ДЕВУШЕК В БОТЕ:</code> <b>{len(db.get_users_gender_love(2))}</b>\n'
                 f'<code>ОТКЛЮЧИЛИ АНКЕТУ:</code> <b>{len(db.get_users_not_active_love())}</b>\n'
                 f'<code>СМОТРЯТ АНКЕТЫ СЕЙЧАС:</code> <b>{len(db.get_users_active_now_love())}</b>')
        await message.answer(text=stats)
    else:
        await message.answer('<b>❣️ Такая команда доступна только админу</b>')


class Spam_all(StatesGroup):
    spam_all = State()

@dp.message(F.text == '👥 Рассылка')
async def send_all(message: types.Message, state: FSMContext):
    if message.from_user.id == REMOVED_PRIVATE_VALUE or message.from_user.id == REMOVED_PRIVATE_VALUE:
        await message.answer('Введите текст текс для рассылки:', reply_markup=markups.back_admin)
        await state.set_state(Spam_all.spam_all)
    else:
        await message.answer('<b>❣️ Такая команда доступна только админу</b>')


@dp.message(Spam_all.spam_all)
async def all_spam(message: types.Message, state: FSMContext):
    spam_text = message.text
    not_active = 0
    active = 0
    for user in db.get_all_users_love():
        try:
            await bot.send_message(user, text=spam_text)
            active += 1
        except:
            not_active += 1
            db.delete_users_love(user)

    await message.answer(f'<b>✅ Рассылка прошла успешно!</b>\nАктивных пользователей: {active}\n<b>Пользователей заблокировавших бота: {not_active}</b>\n\n<b>Неактивные пользователи были удалены</b>')
    await state.clear()


class Send_Mes(StatesGroup):
    id = State()
    send_mes = State()

@dp.message(Command('send_mess'))
async def send_mess(message: Message, state: FSMContext):
     await message.answer('Отправь мне id того, кому бы ты хотел написать')
     await state.set_state(Send_Mes.id)

@dp.message(Send_Mes.id)
async def send_mess(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        await message.answer('Напиши сообщение:')
        await state.set_state(Send_Mes.send_mes)
        await state.update_data(user_id=user_id)
    except ValueError:
        await message.answer(f'Введи число')

@dp.message(Send_Mes.send_mes)
async def send_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    await bot.send_message(user_id, f'<b>Внимание! Тебе отправлено предупреждение:</b>\n\n<code>{message.text}</code>')
    await message.answer('Твое сообщение успешно отправлено')

# @dp.message()
# async def ddddd(message: types.Message):
#     await message.answer(f'{message}')

async def main():
    await bot.delete_webhook(drop_pending_updates=True,)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())