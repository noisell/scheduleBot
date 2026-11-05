import datetime
from bot import db

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📋 Расписание", callback_data="rasp_students")
    keyboard.button(text="👩‍🏫 Учителям", callback_data="rasp_teachers")
    keyboard.button(text="👤 Профиль", callback_data="profile")
    keyboard.button(text="⚙️ Настройки", callback_data="settings")
    keyboard.button(text="📚 Домашка", callback_data="homework")
    keyboard.button(text="📰 Чатик", url="https://t.me/+2GQxu8KT9qZiZDFi")
    keyboard.button(text="💌 Знакомства", url="https://t.me/ngklove_bot")
    keyboard.button(text="🛟 Поддержка", callback_data="support")
    keyboard.adjust(1, 2, 2, 2, 1)
    return keyboard.as_markup()

def profile_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="💰 Пополнить", callback_data="top-up-balance")
    keyboard.button(text="🎁 Потратить", callback_data="bonus")
    keyboard.button(text="👥 Рефералы", callback_data="referrer")
    keyboard.button(text="⚜️ Подписка", callback_data="premium")
    keyboard.button(text="🔙 Назад", callback_data="back_main_menu")
    keyboard.adjust(1, 2, 1, 1)
    return keyboard.as_markup()


def top_up_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="50 RUB", callback_data="top-up_50")
    keyboard.button(text="100 RUB", callback_data="top-up_100")
    keyboard.button(text="150 RUB", callback_data="top-up_150")
    keyboard.button(text="200 RUB", callback_data="top-up_200")
    keyboard.button(text="300 RUB", callback_data="top-up_300")
    keyboard.button(text="500 RUB", callback_data="top-up_500")
    keyboard.button(text="✏️ Ввести вручную", callback_data="enter-summa")
    keyboard.button(text="🔙 Назад", callback_data="back_profile")
    keyboard.adjust(3, 3, 1, 1)
    return keyboard.as_markup()


def premium_sub_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔥 1 МЕСЯЦ | 100 RUB 🔥", callback_data="1-month")
    keyboard.button(text="🔥 5 МЕСЯЦЕВ | 450 RUB 🔥", callback_data="5-month")
    keyboard.button(text="1 ГОД | 900 RUB", callback_data="1-year")
    keyboard.button(text="1 НЕДЕЛЯ | 75 RUB", callback_data="1-week")
    keyboard.button(text="1 ДЕНЬ | 50 RUB", callback_data="1-day")
    keyboard.button(text="🔙 Назад", callback_data="back_profile")
    keyboard.adjust(1)
    return keyboard.as_markup()


def pay_top_up(url: str, label: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="💳 Оплатить", url=url)
    keyboard.button(text="🔍 Проверить оплату", callback_data=f"check-top-up_{label}")
    keyboard.button(text="🔙 Назад", callback_data="back_profile")
    keyboard.adjust(1)
    return keyboard.as_markup()


back_main_menu = [
    [InlineKeyboardButton(text='🔙 Назад', callback_data="back_main_menu")]
]
back_main_menu = InlineKeyboardMarkup(inline_keyboard=back_main_menu)

back_settings = [
    [InlineKeyboardButton(text='🔙 Назад', callback_data="back_settings")]
]
back_settings = InlineKeyboardMarkup(inline_keyboard=back_settings)

back_profile = [
    [InlineKeyboardButton(text='🔙 Назад', callback_data="back_profile")]
]
back_profile = InlineKeyboardMarkup(inline_keyboard=back_profile)

set_group_menu = [
    [InlineKeyboardButton(text='👨‍🎓 Выбрать группу', switch_inline_query_current_chat="group ")],
    [InlineKeyboardButton(text='🔙 Назад', callback_data="back_main_menu")]
]
set_group_menu = InlineKeyboardMarkup(inline_keyboard=set_group_menu)

set_teach_menu = [
    [InlineKeyboardButton(text='👨‍🎓 Выбрать учителя', switch_inline_query_current_chat="")],
    [InlineKeyboardButton(text='🔙 Назад', callback_data="back_main_menu")]
]
set_teach_menu = InlineKeyboardMarkup(inline_keyboard=set_teach_menu)


def create_settings_keyboard(user_id):
    inline_keyboard = InlineKeyboardBuilder()
    not_morn = db.get_notice_morn(user_id)
    not_changes = db.get_notice_changes(user_id)
    not_chang = db.get_not_chang(user_id)
    if not_changes == 1:
        inline_keyboard.button(text='🔕 Изменения', callback_data='off_chang')
    else:
        inline_keyboard.button(text='🔔 Изменения', callback_data='on_chang')

    if not_chang == 1:
        inline_keyboard.button(text='🔕 Без изменений', callback_data='off_not_ch')
    else:
        inline_keyboard.button(text='🔔 Без изменений', callback_data='on_not_ch')

    if not_morn == 1:
        inline_keyboard.button(text='🔕 Напоминания', callback_data='off_morning')
    else:
        inline_keyboard.button(text='🔔 Напоминания', callback_data='on_morning')

    inline_keyboard.button(text='⌛️ Изменить время', callback_data='settings_time')
    inline_keyboard.button(text='🔙 Назад', callback_data="back_main_menu")
    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()


def create_keyboard(date):
    if type(date) == str:
        current_date = datetime.datetime.strptime(date, '%d.%m.%Y')
    else:
        current_date = date
    now_date = datetime.date.today()
    current_weekday = current_date.weekday()
    if current_weekday < 4:
        current_weekday = 0
        current_date += datetime.timedelta(days=0)
    keyboard = {
        "Сегодня": now_date.strftime('%d.%m'),
        "Завтра": (now_date + datetime.timedelta(days=1)).strftime('%d.%m'),
        "Пн": (current_date - datetime.timedelta(days=current_weekday)).strftime('%d.%m'),
        "Вт": (current_date + datetime.timedelta(days=1 - current_weekday)).strftime('%d.%m'),
        "Ср": (current_date + datetime.timedelta(days=2 - current_weekday)).strftime('%d.%m'),
        "Чт": (current_date + datetime.timedelta(days=3 - current_weekday)).strftime('%d.%m'),
        "Пт": (current_date + datetime.timedelta(days=4 - current_weekday)).strftime('%d.%m'),
        "Сб": (current_date + datetime.timedelta(days=5 - current_weekday)).strftime('%d.%m')
    }
    return keyboard


def create_keyboard_hw(date):
    if type(date) == str:
        current_date = datetime.datetime.strptime(date, '%d.%m.%Y')
    else:
        current_date = date
    now_date = datetime.date.today()
    current_weekday = current_date.weekday()
    if current_weekday < 4:
        current_weekday = 0
        current_date += datetime.timedelta(days=0)
    keyboard = {
        "На завтра": (now_date + datetime.timedelta(days=1)).strftime('%d.%m'),
        "Пн": (current_date - datetime.timedelta(days=current_weekday)).strftime('%d.%m'),
        "Вт": (current_date + datetime.timedelta(days=1 - current_weekday)).strftime('%d.%m'),
        "Ср": (current_date + datetime.timedelta(days=2 - current_weekday)).strftime('%d.%m'),
        "Чт": (current_date + datetime.timedelta(days=3 - current_weekday)).strftime('%d.%m'),
        "Пт": (current_date + datetime.timedelta(days=4 - current_weekday)).strftime('%d.%m'),
        "Сб": (current_date + datetime.timedelta(days=5 - current_weekday)).strftime('%d.%m')
    }
    return keyboard


def update_keyboard_dates(date, set_group: str, update_markup=None):
    inline_keyboard = InlineKeyboardBuilder()
    keyboard = create_keyboard(date)
    for day, dates in keyboard.items():
        if day == "Сегодня":
            button_text = f"{day}"
            inline_keyboard.button(text=button_text, callback_data=f'now-day_{set_group}_{dates}')
        elif day == 'Завтра':
            button_text = f"{day}"
            inline_keyboard.button(text=button_text, callback_data=f'tomorrow-day_{set_group}_{dates}')
        else:
            if dates == update_markup:
                button_text = f"⬩ {day} {dates} ⬩"
                inline_keyboard.button(text=button_text, callback_data=f'group_{set_group}_{dates}')
            else:
                button_text = f"ㅤ {day} {dates} ㅤ"
                inline_keyboard.button(text=button_text, callback_data=f'group_{set_group}_{dates}')
    inline_keyboard.button(text='⬅️ Назад', callback_data=f'previous-week-clicked_{set_group}')
    inline_keyboard.button(text='Вперед ➡️', callback_data=f'next-week-clicked_{set_group}')
    inline_keyboard.button(text='👨‍🎓 Выбор группы', switch_inline_query_current_chat="group ")
    inline_keyboard.button(text='🔝 Главное меню', callback_data="back_main_menu")
    inline_keyboard.adjust(2, 3, 3, 2, 1, 1)
    return inline_keyboard.as_markup()


def update_keyboard_dates_teach(date, set_group: str, update_markup=None):
    inline_keyboard = InlineKeyboardBuilder()
    keyboard = create_keyboard(date)
    for day, dates in keyboard.items():
        if day == "Сегодня":
            button_text = f"{day}"
            inline_keyboard.button(text=button_text, callback_data=f'now-day-teach_{set_group}_{dates}')
        elif day == 'Завтра':
            button_text = f"{day}"
            inline_keyboard.button(text=button_text, callback_data=f'tomorrow-day-teach_{set_group}_{dates}')
        else:
            if dates == update_markup:
                button_text = f"⬩ {day} {dates} ⬩"
                inline_keyboard.button(text=button_text, callback_data=f'group-teach_{set_group}_{dates}')
            else:
                button_text = f"ㅤ {day} {dates} ㅤ"
                inline_keyboard.button(text=button_text, callback_data=f'group-teach_{set_group}_{dates}')
    inline_keyboard.button(text='⬅️ Назад', callback_data=f'previous-week-clicked-teach_{set_group}')
    inline_keyboard.button(text='Вперед ➡️', callback_data=f'next-week-clicked-teach_{set_group}')
    inline_keyboard.button(text='👩‍🏫 Выбор учителя', switch_inline_query_current_chat="")
    inline_keyboard.button(text='🔝 Главное меню', callback_data="back_main_menu")
    inline_keyboard.adjust(2, 3, 3, 2, 1, 1)
    return inline_keyboard.as_markup()


def update_keyboard_dates_hw(date, set_group: str):
    inline_keyboard = InlineKeyboardBuilder()
    keyboard = create_keyboard_hw(date)
    for day, dates in keyboard.items():
        if day == 'На завтра':
            button_text = f"{day}"
            inline_keyboard.button(text=button_text, callback_data=f'tomorrow-day-hw_{set_group}_{dates}')
        else:
            button_text = f"ㅤ {day} {dates} ㅤ"
            inline_keyboard.button(text=button_text, callback_data=f'use-date_{set_group}_{dates}')
    inline_keyboard.button(text='⬅️ Назад', callback_data=f'previous-week-clicked-hw_{set_group}')
    inline_keyboard.button(text='Вперед ➡️', callback_data=f'next-week-clicked-hw_{set_group}')
    inline_keyboard.button(text='🔝 Главное меню', callback_data="back_main_menu")
    inline_keyboard.adjust(1, 3, 3, 2, 1)
    return inline_keyboard.as_markup()


def update_keyboard_dates_hw_use(date, set_group: str, update_markup=None):
    inline_keyboard = InlineKeyboardBuilder()
    keyboard = create_keyboard_hw(date)
    for day, dates in keyboard.items():
        if day == 'На завтра':
            button_text = f"{day}"
            inline_keyboard.button(text=button_text, callback_data=f'tomorrow-day-hw-use_{set_group}_{dates}')
        else:
            if dates == update_markup:
                button_text = f"⬩ {day} {dates} ⬩"
                inline_keyboard.button(text=button_text, callback_data=f'use-date-use_{set_group}_{dates}')
            else:
                button_text = f"ㅤ {day} {dates} ㅤ"
                inline_keyboard.button(text=button_text, callback_data=f'use-date-use_{set_group}_{dates}')
    inline_keyboard.button(text='⬅️ Назад', callback_data=f'previous-week-clicked-hw-use_{set_group}')
    inline_keyboard.button(text='Вперед ➡️', callback_data=f'next-week-clicked-hw-use_{set_group}')
    inline_keyboard.button(text='🔝 Главное меню', callback_data="back_main_menu")
    inline_keyboard.adjust(1, 3, 3, 2, 1)
    return inline_keyboard.as_markup()


def create_send_admin_keyboard(mess_id: int):
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text='Отправить', callback_data=f'send-admin_{mess_id}')
    inline_keyboard.button(text='Удалить', callback_data='delete-mess')
    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()

def create_key_edit_hw(data_hw):
    hw_key = [
        [InlineKeyboardButton(text='Назад', callback_data=f'back-hw-edit_{data_hw}')]
    ]
    hw_key = InlineKeyboardMarkup(inline_keyboard=hw_key)
    return hw_key


def create_key_sett_hw(data_hw):
    hw_settings = [
        [InlineKeyboardButton(text='Добавить еще', callback_data=f'plus-hw_{data_hw}')],
        [InlineKeyboardButton(text='Редактировать', callback_data=f'edit-hw_{data_hw}')],
        [InlineKeyboardButton(text='Удалить', callback_data=f'delete-hw_{data_hw}'),
         InlineKeyboardButton(text='Сохранить', callback_data=f'save-hw_{data_hw}')],
    ]
    hw_settings = InlineKeyboardMarkup(inline_keyboard=hw_settings)
    return hw_settings


def number_str(num: int, mes_id, date):
    markup = InlineKeyboardBuilder()
    dop_btn = InlineKeyboardBuilder()
    for i in range(1, num + 1):
        markup.button(text=f'{i}', callback_data=f'edit-str-num_{i}_{date}')
    dop_btn.button(text='Назад', callback_data=f'back-hw-edit_{date}')
    dop_btn.adjust(1)
    markup.adjust(4)
    markup.attach(dop_btn)
    return markup.as_markup()


def premium_pay_ds_kb(price: int, date_end: str):
    markup = InlineKeyboardBuilder()
    markup.button(text="✔️ Подтверждаю", callback_data=f"pay-prem_{price}_{date_end}")
    markup.button(text="🔝 В профиль", callback_data=f"back_profile")
    markup.adjust(1)
    return markup.as_markup()


def premium_pay_bonus_kb(date_end: str):
    markup = InlineKeyboardBuilder()
    markup.button(text="✔️ Подтверждаю", callback_data=f"pay-prem-bonus_{date_end}")
    markup.button(text="🔝 В профиль", callback_data=f"back_profile")
    markup.adjust(1)
    return markup.as_markup()


# ----------------------------------------------------------------------------------------------------------------------
admin_panel = [
    [KeyboardButton(text='📊 Статистика')],
    [KeyboardButton(text='👥 Рассылка'),
     KeyboardButton(text='👥 Пересылка')],
    [KeyboardButton(text='🔗 Сменить ссылку')],
    [KeyboardButton(text='🔝 Главное меню')]
]

admin_panel_love = [
    [KeyboardButton(text='📊 Статистика'),
     KeyboardButton(text='👥 Рассылка')],
    [KeyboardButton(text='⚠️ Предупреждение'),
     KeyboardButton(text='🚫 Заблокировать')],
    [KeyboardButton(text='🔝 Главное меню')]
]
back_admin = [
    [KeyboardButton(text='🔝 В Админ панель')]
]
get_usernames = [
    [KeyboardButton(text='👥 Получить usernames'),
     KeyboardButton(text='🔎 Найти пользователя')],
    [KeyboardButton(text='🔝 В Админ панель')]
]
set_find_user = [
    [KeyboardButton(text='ПО USERNAME'),
     KeyboardButton(text='ПО USER ID')],
    [KeyboardButton(text='🔝 В Админ панель')]
]
campus_spam = [
    [KeyboardButton(text='ВСЕМ')],
    [KeyboardButton(text='1 КОРПУСУ'),
     KeyboardButton(text='2 КОРПУСУ')],
    [KeyboardButton(text='🔝 В Админ панель')]
]
accept_love = [
    [InlineKeyboardButton(text='ПРИНЯТЬ', callback_data='accept_love')]
]
accept_disc = [
    [InlineKeyboardButton(text='Принять', callback_data='accept_disc')]
]
create_prof = [
    [InlineKeyboardButton(text='💌 СОЗДАТЬ АНКЕТУ', callback_data='create_prof')]
]
off_form = [
    [InlineKeyboardButton(text='Нашел себе новые знакомства', callback_data='state_yes_new')],
    [InlineKeyboardButton(text='Уже не хочу никого искать', callback_data='state_not_new')],
    [InlineKeyboardButton(text='Да я по приколу зашел', callback_data='state_rofl')]
]
edite_prof = [
    [InlineKeyboardButton(text='Описание анкеты', callback_data='edite_about'),
     InlineKeyboardButton(text='Интересы поиска', callback_data='edit_find')],
    [InlineKeyboardButton(text='Имя', callback_data='edite_name'),
     InlineKeyboardButton(text='Корпус', callback_data='edite_group')],
    [InlineKeyboardButton(text='Сменить фото/видео', callback_data='edite_media')],
    [InlineKeyboardButton(text='Заполнить заново', callback_data='edite_all')]
]
save_prof = [
    [KeyboardButton(text='Сохранить')],
    [KeyboardButton(text='Изменить анкету')]
]
gender = [
    [KeyboardButton(text='Мужского'),
     KeyboardButton(text='Женского')]
]
interes = [
    [KeyboardButton(text='Парней'),
     KeyboardButton(text='Девушек')],
    [KeyboardButton(text='Все равно')]
]
about = [
    [KeyboardButton(text='Пропустить этот шаг')]
]
ed_about = [
    [KeyboardButton(text='Оставить без описания')]
]
save = [
    [KeyboardButton(text='Закончить добавление')]
]
main_love = [
    [KeyboardButton(text='💌 Смотреть анкеты')],
    [KeyboardButton(text='💬 Обратная связь'),
     KeyboardButton(text='👨‍🎓 Профиль')],
    [KeyboardButton(text='📋 Расписание НГК')]
]
sub_chanel = [
    [InlineKeyboardButton(text='Подписаться', url='https://t.me/+2GQxu8KT9qZiZDFi')],
    [InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub')]
]
remove_date = [
    [InlineKeyboardButton(text='Сменить дату', callback_data='remove_date')]
]
close_mes = [
    [InlineKeyboardButton(text='Скрыть', callback_data='delete-mess')]
]
close_mes = InlineKeyboardMarkup(inline_keyboard=close_mes)

#  Добавление клавиатур
main_love = ReplyKeyboardMarkup(keyboard=main_love, resize_keyboard=True, input_field_placeholder='Используй кнопки')
back_admin = ReplyKeyboardMarkup(keyboard=back_admin, resize_keyboard=True, input_field_placeholder='Введи текст...')
get_usernames = ReplyKeyboardMarkup(keyboard=get_usernames, resize_keyboard=True,
                                    input_field_placeholder='Введи текст...')
set_find_user = ReplyKeyboardMarkup(keyboard=set_find_user, resize_keyboard=True,
                                    input_field_placeholder='Введи текст...')
gender = ReplyKeyboardMarkup(keyboard=gender, resize_keyboard=True, input_field_placeholder='Выбери пол')
about = ReplyKeyboardMarkup(keyboard=about, resize_keyboard=True, input_field_placeholder='Расскажи о себе')
ed_about = ReplyKeyboardMarkup(keyboard=ed_about, resize_keyboard=True, input_field_placeholder='Расскажи о себе')
save = ReplyKeyboardMarkup(keyboard=save, resize_keyboard=True, input_field_placeholder='Отправь медиа')
interes = ReplyKeyboardMarkup(keyboard=interes, resize_keyboard=True, input_field_placeholder='Кого ищешь?')
save_prof = ReplyKeyboardMarkup(keyboard=save_prof, resize_keyboard=True, input_field_placeholder='Выбери действие')
admin_panel = ReplyKeyboardMarkup(keyboard=admin_panel, resize_keyboard=True,
                                  input_field_placeholder='Используй кнопки')
admin_panel_love = ReplyKeyboardMarkup(keyboard=admin_panel_love, resize_keyboard=True,
                                       input_field_placeholder='Используй кнопки')
campus_spam = ReplyKeyboardMarkup(keyboard=campus_spam, resize_keyboard=True,
                                  input_field_placeholder='Выбери корпус...')

create_prof = InlineKeyboardMarkup(inline_keyboard=create_prof)
sub_chanel = InlineKeyboardMarkup(inline_keyboard=sub_chanel)
edite_prof = InlineKeyboardMarkup(inline_keyboard=edite_prof)
accept_love = InlineKeyboardMarkup(inline_keyboard=accept_love)
off_form = InlineKeyboardMarkup(inline_keyboard=off_form)
remove_date = InlineKeyboardMarkup(inline_keyboard=remove_date)
accept_disc = InlineKeyboardMarkup(inline_keyboard=accept_disc)
