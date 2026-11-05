import os
from bot import db

BOT_TOKEN_LOVE = os.getenv("BOT_TOKEN_LOVE", "")
TOKEN_YOO_MONEY = os.getenv("YOOMONEY_TOKEN", "")
photo1 = 'AgACAgIAAxkBAAID0GU4BjrvZfdqbMFCKpEMxox9wuVAAAIa1TEbgivASXjQuf52qVD_AQADAgADcwADMAQ'
photo2 = 'AgACAgIAAxkBAAID0mU4BpQoaXCFY6DXZPVzQ4COJwNUAAId1TEbgivASTEI8mCWuaGMAQADAgADcwADMAQ'
photo3 = 'AgACAgIAAxkBAAJxBGU5omtD1fKS6PPqhbEl22_HBB3tAAJQ0jEbW27IScNrfZwl4HgjAQADAgADcwADMAQ'  # Возможно любовь
photo4 = 'AgACAgIAAxkBAAJtoWU5h7A-xi5-ET9B98y8-Lu02ifWAALo0TEbW27ISVqk4j0Lmyc4AQADAgADcwADMAQ'  # Голосовое
photo5 = 'AgACAgIAAxkBAAJto2U5h9FYzjnpSb1Kb61RS8Urtd_RAALGzjEbsl_JSQ3S7XaTHNRFAQADAgADcwADMAQ'  # Валентинка
photo6 = 'AgACAgIAAxkBAAJtn2U5h5R78QfvugqnKtX76DdNDSTVAALn0TEbW27ISbKF5tZ5wCHgAQADAgADcwADMAQ'  # Взаимная
about = 'AgACAgIAAxkBAAIuKWWXXZNd0kesmUQyPKrSXN6EVhPOAALWzzEbturASGuWMF7YgMNcAQADAgADcwADNAQ'
settings = 'AgACAgIAAxkBAAIuJ2WXXXCdnPR-p3TEWhEuDkAnF1S6AALVzzEbturASJatiTHuD-HpAQADAgADcwADNAQ'
main_photo = 'AgACAgIAAxkBAAIF6mV7J0gDLrCskVWB54PBRwABxeEqwgACiNUxG4AF2EsTbLbf1aEK_gEAAwIAA20AAzME'
rasp_photo = 'AgACAgIAAxkBAAIr8mWUO-cYbt0u56YP0zbsEcZWtzZWAAJR1jEblCOhSPPquu58Q7lSAQADAgADcwADNAQ'
profile_photo = 'AgACAgIAAxkBAAIuJWWXXUA-gEn1aVu0FiHLhPBsfk4YAALUzzEbturASLYQ5wbpEaqvAQADAgADcwADNAQ'
homework_photo = 'AgACAgIAAxkBAAIuK2WXXccgDpoFBk6WJ2oTBqmhaN9JAALXzzEbturASLxn6qh3CUhmAQADAgADbQADNAQ'
changes_photo = 'AgACAgIAAxkBAAIuu2We7ht0Z-SAfYbLwAzuutyoJHOcAAKU1jEbCYr4SNKFWuIw4H_nAQADAgADcwADNAQ'
notice_morning_photo = 'AgACAgIAAxkBAAIuvmWe75a_zxlizywm8GnwOkrCEB5wAAKX1jEbCYr4SGGmjyB8vRjqAQADAgADcwADNAQ'

teachers_photo = [
    'https://cdn-icons-png.flaticon.com/512/9473/9473007.png',
    'https://cdn-icons-png.flaticon.com/256/9890/9890271.png',
    'https://cdn-icons-png.flaticon.com/512/7107/7107941.png',
    'https://cdn-icons-png.flaticon.com/512/9473/9473009.png',
    'https://cdn-icons-png.flaticon.com/256/6101/6101814.png',
]


def profile_text(user_id: int) -> int:
    group = db.select_current_group(user_id=user_id)
    teacher = db.get_cur_teach(user_id=user_id)
    if group == '0':
        group = 'не задана'
    if teacher == '0':
        teacher = 'не задан'

    balance = db.get_balance(user_id=user_id)
    premium = db.get_active_prem(user_id=user_id)
    if premium == 1:
        premium = "✅ АКТИВНА"
    else:
        premium = "❌ НЕАКТИВНА"
    if db.user_exists_premium(user_id=user_id):
        date_end = db.get_end_date(user_id=user_id)
        if date_end is None or premium == "❌ НЕАКТИВНА":
            message = ("👤 <b>ТВОЙ ПРОФИЛЬ</b>\n\n"
                       f"🗝 USER ID: <b>{user_id}</b>\n"
                       f"👨‍🎓 Группа: <b>{group}</b>\n"
                       f"👩‍🏫 Учитель: <b>{teacher}</b>\n\n"
    
                       f"💰 Баланс: <b>{balance} RUB</b>\n"
                       f"⚜️ Подписка: <b>{premium}</b>\n")
        else:
            message = ("👤 <b>ТВОЙ ПРОФИЛЬ</b>\n\n"
                       f"🗝 USER ID: <b>{user_id}</b>\n"
                       f"👨‍🎓 Группа: <b>{group}</b>\n"
                       f"👩‍🏫 Учитель: <b>{teacher}</b>\n\n"

                       f"💰 Баланс: <b>{balance} RUB</b>\n"
                       f"⚜️ Подписка: <b>{premium}</b>\n"
                       f"⌛️ Действует до: <b>{date_end}</b>\n\n")
    else:
        message = ("👤 <b>ТВОЙ ПРОФИЛЬ</b>\n\n"
                   f"🗝 USER ID: <b>{user_id}</b>\n"
                   f"👨‍🎓 Группа: <b>{group}</b>\n"
                   f"👩‍🏫 Учитель: <b>{teacher}</b>\n\n"

                   f"💰 Баланс: <b>{balance} RUB</b>\n"
                   f"⚜️ Подписка: <b>{premium}</b>\n")
    return message


def premium_sub_text(user_id: int):
    balance = db.get_balance(user_id=user_id)
    message = ("⚜️ <b>ПРЕМИУМ ПОДПИСКА</b>\n\n"
               f"💰 Баланс: <b>{balance} RUB</b>\n\n"
               f"<b>Премиум подписка - это:</b>\n\n"
               f"✅ Уведомления об изменениях\n"
               f"✅ Утренние напоминания\n"
               f"✅ Улучшенная поддержка\n\n"
               f"Мы никого не призываем покупать подписку, но приобретая ее, вы очень помогаете в развитии проекта и делаете большой вклад, для дальнейшего поддержания, развития и улучшения всей инфраструктуры бота.\n"
               )
    return message


def create_settings_text(user_id):
    not_morn = db.get_notice_morn(user_id)
    not_morn_time = db.get_notice_time(user_id)
    not_changes = db.get_notice_changes(user_id)
    not_chang = db.get_not_chang(user_id)
    setting_text = ('<b>⚙️ ТВОИ НАСТРОЙКИ</b>\n\n'
                    '<b>┌ ✉️ Уведомления</b>\n')

    if not_changes == 1:
        setting_text += '<b>├</b> Изменения: 🔔\n'
    else:
        setting_text += '<b>├</b> Изменения: 🔕\n'

    if not_chang == 1:
        setting_text += '<b>└</b> Без изменений: 🔔\n\n'
    else:
        setting_text += '<b>└</b> Без изменений: 🔕\n\n'

    setting_text += '<b>┌ ⏰ Напоминания</b>\n'

    if not_morn == 1:
        setting_text += '<b>├</b> Расписание: 🔔\n'
    else:
        setting_text += '<b>├</b> Расписание: 🔕\n'

    setting_text += f'<b>└</b> Время отправки: <b>{not_morn_time}</b>'
    return setting_text


def main_menu(first_name):
    text = f'<b>{first_name}</b>, работа бота восстановиться по результатам опроса.'
    return text


support_menu = ('– Нашли ошибку?\n'
                '– Не правильно показывается расписание?\n'
                '– Бот не работает должным образом?\n'
                '– Хотите узнать больше о том, как использовать наш сервис?\n'
                '– Появилась идея по улучшению работы бота?\n\n'
                '<b>Задайте свой вопрос прямо в бота и мы постараемся ответить вам как можно скорее!</b>')

contact_menu = ('<b>– Хочешь пожаловаться на студента?</b>\n'
                '<b>– Бот не работает должным образом?</b>\n'
                '<b>– Хотите узнать больше о том, как использовать наш сервис?</b>\n'
                '<b>– Появилась идея по улучшению работы бота?</b>\n\n'
                '🤗 <b>Мы всегда рады помочь вам решить ваш вопрос!</b>\n\n'
                '<b>Отправьте вопрос прям в бота и мы постараемся ответить вам как можно быстрее!</b>')

accept_love = '<b>Для продолжения необходимо принять</b> <a href="https://ngkrobot.ru/doc/terms-of-use.pdf"><b>пользовательское соглашение</b></a> <b>и</b> <a href="https://ngkrobot.ru/doc/privacy-policy.pdf"><b>политику конфиденциальности</b></a>'

main_menu_love = ('🫶🏻 <b>Добро пожаловать в Знакомства НГК!</b>\n\n'
                  '🤍 <b>Наша цель - объединить студентов и помочь найти им друзей!</b>\n\n'
                  '🤗 <b>Откройся новым знакомствам, экспериментируй и наслаждайся просмотром анкет. Мы верим, что лучшие друзья и любимые люди могут быть рядом, и это место поможет тебе найти их!</b>\n\n'
                  '❤️‍🔥 <b>Желаю тебе только удачи!</b>')

disclaimer = ('<b>❗️ Отказ об ответственности ❗️</b>\n\n'
              ' Настоящий уведомляем, что информация, предоставляемая через данный бот, включая расписание занятий, идентификационные данные преподавателей, номера учебных групп, рейтинги преподавателей и отзывы преподавателей, является условной и создана исключительно в иллюстративных целях и (или) показать пример возможностей данного бота.\n\n'
              ' Все представленные данные не имеют отношения к фактическим сведениям, и не предназначены для отражения реальной информационной среды учебного заведения, и не характеризуют прямого профессионализма или личных качеств преподователей или мнений его студентов, персонала и иных лиц.\n\n'
              ' Любое сходство между данными, представленными в боте, и реальными данными, относящимися к учебному заведению, его сотрудникам или студентам, является абсолютно случайным и не должно интерпретироваться как преднамеренное. Этот бот не предназначен для использования в качестве авторитетного источника информации о расписании занятий, личных данных преподавательского состава или их профессиональной и личной оценки.\n\n'
              ' Мы настоятельно рекомендуем пользователям получать верифицированную информацию непосредственно из официальных источников учебного заведения.\n\n'
              ' Создатель бота отказывается от любой ответственности за любые последствия, возникающие в результате использования информации, представленной ботом, включая, но не ограничиваясь, любые прямые или косвенные убытки и (или) ущерб.\n\n'
              ' Создатель бота также не несет ответственности за точность, актуальность и полноту представленных данных, а также за любые действия, совершенные на основании этой информации.\n\n'
              ' Согласно статье 10.6 149 Федерального закона "Об информации, информационных технологиях и о защите информации" текущий администратор и создатель не несут ответственности за оставленные оценки и отзывы, и не имеют возможности их контролировать и взаимодействовать с ними, т.к. данный бот не имеет более пятисот тысяч пользователей в течении суток и в целом.\n\n'
              ' Нажимая «Принять», вы подтверждаете, что ознакомились и соглашаетесь со всем вышеприведенным и готовы использовать данного бота на свой страх и риск, под свою ответственность.')

list_groups = {
    '11Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '12Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '21Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '22Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '31Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '32Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '41Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '42Б': ['Экономика и бух. учет', 'https://em-content.zobj.net/source/apple/354/fax-machine_1f4e0.png'],
    '21БД': ['Банковское дело', 'https://em-content.zobj.net/source/apple/354/money-with-wings_1f4b8.png'],
    '22БД': ['Банковское дело', 'https://em-content.zobj.net/source/apple/354/money-with-wings_1f4b8.png'],
    '31БД': ['Банковское дело', 'https://em-content.zobj.net/source/apple/354/money-with-wings_1f4b8.png'],
    '32БД': ['Банковское дело', 'https://em-content.zobj.net/source/apple/354/money-with-wings_1f4b8.png'],
    '22В': ['Веб разработка', 'https://em-content.zobj.net/source/apple/354/laptop_1f4bb.png'],
    '24В': ['Веб разработка', 'https://em-content.zobj.net/source/apple/354/laptop_1f4bb.png'],
    '32В': ['Веб разработка', 'https://em-content.zobj.net/source/apple/354/laptop_1f4bb.png'],
    '42В': ['Веб разработка', 'https://em-content.zobj.net/source/apple/354/laptop_1f4bb.png'],
    '44В': ['Веб разработка', 'https://em-content.zobj.net/source/apple/354/laptop_1f4bb.png'],
    '11ДОУ': ['Док. обеспечение управ-ия', 'https://em-content.zobj.net/source/apple/354/page-facing-up_1f4c4.png'],
    '12ДОУ': ['Док. обеспечение управ-ия', 'https://em-content.zobj.net/source/apple/354/page-facing-up_1f4c4.png'],
    '21ДОУ': ['Док. обеспечение управ-ия', 'https://em-content.zobj.net/source/apple/354/page-facing-up_1f4c4.png'],
    '22ДОУ': ['Док. обеспечение управ-ия', 'https://em-content.zobj.net/source/apple/354/page-facing-up_1f4c4.png'],
    '31ДОУ': ['Док. обеспечение управ-ия', 'https://em-content.zobj.net/source/apple/354/page-facing-up_1f4c4.png'],
    '33ДОУ': ['Док. обеспечение управ-ия', 'https://em-content.zobj.net/source/apple/354/page-facing-up_1f4c4.png'],
    '11К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '12К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '13К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '14К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '21К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '22К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '23К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '31К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '32К': ['Коммерция', 'https://em-content.zobj.net/source/apple/354/chart-increasing_1f4c8.png'],
    '11Л': ['Логистика', 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png'],
    '12Л': ['Логистика', 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png'],
    '13Л': ['Логистика', 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png'],
    '21Л': ['Логистика', 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png'],
    '22Л': ['Логистика', 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png'],
    '31Л': ['Логистика', 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png'],
    '32Л': ['Логистика', 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png'],
    '11П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '12П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '13П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '14П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '21П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '23П': ['Программирование',
            'https://img.freepik.com/premium-vector/heart-in-fire-hot-emoji-black-burning-heart-with-fire-on-a-black-background-vector-illustration_155957-1294.jpg'],
    '31П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '33П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '41П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '43П': ['Программирование', 'https://em-content.zobj.net/source/apple/354/technologist_1f9d1-200d-1f4bb.png'],
    '11Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '12Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '13Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '21Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '22Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '23Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '31Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '32Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '33Ю': ['Юриспруденция', 'https://em-content.zobj.net/source/apple/354/woman-judge_1f469-200d-2696-fe0f.png'],
    '31С': ['Сурдокоммуникация', 'https://cdn.icon-icons.com/icons2/1686/PNG/512/12056loveyougesture_111440.png'],
    '31Т': ['Товароведение',
            'https://creazilla-store.fra1.digitaloceanspaces.com/emojis/53157/shopping-cart-emoji-clipart-xl.png'],
}


def referrer_text(user_id: int):
    bonus_count = db.get_bonus(user_id=user_id)
    bonus_free = db.get_free_bonus(user_id=user_id)
    count_referrals = db.count_referrers(user_id=user_id)
    text = ("👥 <b>РЕФЕРАЛЬНАЯ СИСТЕМА</b>\n\n"
            f"<b>Твоя реферальная ссылка:</b>\n"
            f"👉 <code>https://t.me/ngk_robot?start={user_id}</code> 👈\n\n"
            f"💝 Всего: <b>{bonus_count} мес. подписки</b>\n"
            f"🎁 Доступно: <b>{bonus_free} мес. подписки</b>\n\n")
    if count_referrals > 0:
        referrals = db.get_usernames_ref(user_id=user_id)
        text += f"┌ 👥 Ваши рефералы ({count_referrals} чел.):\n"
        for index, element in enumerate(referrals):
            if index == len(referrals) - 1:
                text += f'└ @{element}\n\n'
            else:
                text += f'├ @{element}\n'
    else:
        text += "👥 Всего рефералов: <b>0 чел.</b>\n\n"
    text += ("🤩 Приглашай друзей в бота и получай <b>бесплатную подписку на месяц</b>, за каждого нового пользователя.\n\n"
             "<b>Условия акции:</b>\n"
             "- Приглашенный пользователь не должен был быть зарегистрирован ранее в боте;\n"
             "- Приглашающий пользователь должен был хотя бы раз пополнить счет, на любую сумму.")

    return text


def premium_pay_ds(price: int, date_end: str) -> str:
    return (
        '<b>1.</b> Оплата подписки на услуги Telegram-бота "Расписание" является <b>добровольной</b> и <b>не подлежит</b> возврату.\n'
        "<b>2.</b> Покупая подписку вы <b>подтверждаете свое совершеннолетие.</b>\n"
        "<b>3.</b> Подписка предоставляет доступ к премиум-функциям бота на определенный период времени, который написан ниже.\n"
        "<b>4.</b> Администрация бота <b>не несет ответственности</b> за временные сбои и прерывания в работе сервиса, вызванные факторами, находящимися вне нашего контроля.\n\n"
        f"💸 Будет списано: <b>{price} RUB</b>\n"
        f"⌛️ Будет действовать до: <b>{date_end}</b>\n\n"
        f"<b>Для продолжения подтвердите согласие с условиями</b> 👇")


def premium_bonus(date_end: str, count_free: int) -> str:
    return (
        f"💝 Всего активных бонусов: <b>{count_free} мес.</b>\n"
        f"🎁 Будет списано: <b>1 мес. подписки</b>\n"
        f"⌛️ Будет действовать до: <b>{date_end}</b>\n\n"
        f"<b>Для продолжения подтвердите, что готовы потратить бонус</b> 👇")