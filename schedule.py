import datetime
import pdfplumber
import re
from bot import db

list_groups = ['11б', '12б', '11л', '12л', '13л', '11п', '12п', '13п', '14п', '11ю',
               '12ю', '13ю', '21б', '22б', '21л', '22л', '21ю', '22ю', '23ю', '32ю',
               '33ю', '21п', '22в', '23п', '24в', '31с', '31б', '31л', '31ю', '31п',
               '32б', '32л', '32в', '33п', '41б', '41п', '42б', '42в', '43п', '44в',
               '11к', '12к', '13к', '14к', '21к', '22к', '23к', '31к', '32к', '31т',
               '21бд', '22бд', '31бд', '32бд', '11доу', '12доу', '21доу', '33доу',
               '31доу', '22доу']

campus_1 = ['11б', '12б', '11л', '12л', '13л', '11п', '12п', '13п', '14п', '11ю',
            '12ю', '13ю', '21б', '22б', '21л', '22л', '21ю', '22ю', '23ю', '32ю',
            '33ю', '21п', '22в', '23п', '24в', '31с', '31б', '31л', '31ю', '31п',
            '32б', '32л', '32в', '33п', '41б', '41п', '42б', '42в', '43п', '44в']

campus_2 = ['11доу', '12доу', '11к', '12к', '21бд', '21доу', '21к', '22к', '33доу',
            '31бд', '31доу', '31к', '32к', '31т', '13к', '14к', '22бд', '22доу',
            '23к', '32бд']

first_course = ['11б', '12б', '11л', '12л', '13л', '11п', '12п', '13п', '14п', '11ю', '12ю', '13ю']
second_course = ['21б', '22б', '21л', '22л', '21п', '22в', '23п', '24в', '31с', '21ю', '22ю', '23ю']
third_course = ['31б', '32б', '31л', '32л', '31п', '32в', '33п', '31ю', '32ю', '33ю']
fourth_course = ['41б', '42б', '41п', '42в', '43п', '44в']
fc2 = ['11доу', '12доу', '11к', '12к', '13к', '14к']
sc2 = ['21бд', '22бд', '21доу', '22доу', '21к', '22к', '23к']
tc2 = ['31бд', '32бд', '31доу', '33доу', '31к', '32к', '31т']


def is_upper_week(date_str):
    date = datetime.datetime.strptime(date_str, '%d.%m')
    first_upper_monday = datetime.datetime(datetime.datetime.now().year, 1, 15)
    delta = date - first_upper_monday
    weeks = delta.days // 7
    return weeks % 2 == 0


def find_prim_changes(week, dates, group, up_weeks):
    text = '<b>Примечания к изменениям:</b>\n'
    if str(group).lower() in campus_1:
        for t in db.get_chang_teach(1, dates):
            name_teach = find_name_teacher(t)
            if name_teach:
                check_name_teach = db.get_all_teach(dates, group, week, up_weeks)
                if name_teach in check_name_teach:
                    text += f'{t}\n'
            else:
                if not find_groups(t) == []:
                    if str(group) in find_groups(t):
                        text += f'{t}\n'

        if text == '<b>Примечания к изменениям:</b>\n':
            return False
        else:
            return text

    elif str(group).lower() in campus_2:
        for t in db.get_chang_teach(2, dates):
            name_teach = find_name_teacher(t)
            if name_teach:
                check_name_teach = db.get_all_teach(dates, group, week, up_weeks)
                if name_teach in check_name_teach:
                    text += f'{t}\n'
            else:
                if not find_groups(t) == []:
                    if str(group) in find_groups(t):
                        text += f'{t}\n'

        if text == '<b>Примечания к изменениям:</b>\n':
            return False
        else:
            return text


def parsing_changes(pdf_file):
    final_list = []
    count = -1
    find_title = []
    dates_list = []
    lists = []
    all_text = ''
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text_pages = page.extract_text()
            all_text += text_pages

        title_pages = all_text.split('ЗАНЯТИЙ\n')
        find_title.append(title_pages)

        for title in find_title:
            title.remove(title[0])
            lists.append(title)

        for finds in lists:
            for date in finds:
                dates_lst = date.split('\nГруппа Номер')
                dates_list.append(dates_lst[0])
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                try:
                    final_list.append(dates_list[0])
                    dates_list.pop(0)
                    count += 1
                except IndexError:
                    pass
                for row in table:
                    lists = []  # Создание нового списка для каждого ряда
                    for it, item in enumerate(row):
                        if item is None or item == '':
                            for index in reversed(range(0, (count + 1))):
                                if final_list[index][it] is not None:
                                    lists.append(final_list[index][it])
                                    break
                        elif '\n' in item:
                            item = str(item).replace('\n', ' ')
                            lists.append(item)
                        else:
                            lists.append(item)

                    if len(lists) == 6:
                        final_list.append(lists)
                        count += 1

    return_list = []
    for i in final_list:
        find_prim = str(i[0]).split()
        if 'Группа' == i[0]:
            pass
        elif len(find_prim) > 2:
            return_list.append(i[0])
        elif 'экзамен' in i[2].lower():
            i[3] = i[2]
            i[4] = i[2]
            i[5] = i[2]
            return_list.append(i)
        elif 'практика' in i[2].lower():
            i[3] = i[2]
            i[4] = i[2]
            i[5] = i[2]
            return_list.append(i)
        elif 'нет замены' in i[4].lower():
            i.pop(-1)
            return_list.append(i)
        elif 'дистанцион' in str(i[4]).lower():
            i.pop(-1)
            return_list.append(i)
        elif 'перенос' in str(i[4]).lower():
            i.pop(-1)
            return_list.append(i)

        elif 'дополнительно' in i[2].lower() or 'дополнительно' in i[3].lower():
            i.pop(3)
            return_list.append(i)

        else:
            return_list.append(i)

    return return_list


def find_name_teacher(initials_string):
    pattern = r"[А-ЯЁа-яё]+\s+[А-ЯЁ]\.[А-ЯЁ]\b"
    name_matches = re.findall(pattern, initials_string)
    if name_matches:
        for name in name_matches:
            return f'{name}.'
    else:
        return False


def find_groups(s: str):
    pattern = r'\d{2}[А-Я]{1,3}'
    groups = re.findall(pattern, s)
    return groups


def add_db_changes(parsing_chang, campus, date_change):
    up_weeks = None
    date = ''
    for i in parsing_chang:
        if 'ВЕРХНЯЯ НЕДЕЛЯ' in i:
            find_date = re.compile(r'\d{2}\.\d{2}\.\d{4}')
            date = find_date.search(i).group()
            up_weeks = 2
        elif 'НИЖНЯЯ НЕДЕЛЯ' in i:
            find_date = re.compile(r'\d{2}\.\d{2}\.\d{4}')
            date = find_date.search(i).group()
            up_weeks = 1
        else:
            if not find_groups(str(i[0])) == []:
                group = str(i[0])
                door_num_par = str(i[1]).split()
                num_par = door_num_par[0]
                door_num_par.pop(0)
                door = ''
                for doors in door_num_par:
                    door += doors

                if 'практика' in str(i[2]).lower():
                    absent1 = str(i[2])
                    par1 = str(i[2])

                elif 'экзамен' in str(i[2]).lower():
                    absent1 = str(i[2])
                    par1 = str(i[2])

                elif 'дополнительно' in str(i[2]).lower():
                    absent1 = str(i[2])
                    par1 = str(i[2])
                else:
                    absent1 = str(i[2])
                    par1 = str(i[3])

                if 'перенос' in str(i[4]).lower():
                    absent2 = str(i[4])
                    par2 = str(i[4])
                elif 'нет замены' in str(i[4]).lower():
                    absent2 = str(i[4])
                    par2 = str(i[4])
                elif 'дистанцион' in str(i[4]).lower():
                    absent2 = str(i[4])
                    par2 = str(i[4])
                else:
                    try:
                        absent2 = str(i[4])
                        par2 = str(i[5])
                    except IndexError:
                        absent2 = str(i[3])
                        par2 = str(i[4])

                db.add_changes(date=date, group=group, up_week=up_weeks, num_par=num_par, door=door, absent1=absent1,
                               par1=par1, absent2=absent2, par2=par2, campus=campus, insert_date=date_change)
            else:
                if type(i) == str:
                    db.add_teach(camp=campus, date=date, chang=i, insert_date=date_change)


def data_processing_teacher(teacher_name: str, date: str) -> dict:
    changes = db.get_changes_teach(date, teacher_name)
    changes = [list(i) for i in changes]
    changes = [i[5:] for i in changes]
    cancel_list = []
    changes_list = []
    pop_list = []
    for change in changes:
        group, count_para, door, name_absent, couple_absent, name, couple = change
        if name_absent == teacher_name and 'перенос' not in str(name).lower() and name != teacher_name:
            cancel_list.append(list(change))
        else:
            changes_list.append(list(change))
    for change in changes_list:
        group, count_para, door, name_absent, couple_absent, name, couple = change
        match = re.search(r'\(ауд\.\s*(\d+)\)', couple)
        if match:
            aud = match.group(1)
            text_not_aud = re.sub(r'\(ауд\.\s*\d+\)', '', couple).strip()
            change[2] = aud
            change[-1] = text_not_aud
        if 'перенос' in str(name).lower():
            numbers = re.findall(r'\d+', couple)
            for number in numbers:
                if 1 <= int(number) <= 6:
                    change[1] = int(number)
                    change[-1] = couple_absent
                    break
        elif 'перенос' in str(couple).lower():
            numbers = re.findall(r'\d+', couple)
            for number in numbers:
                if 1 <= int(number) <= 6:
                    change[1] = int(number)
                    cp = re.split(r'перенос', couple, flags=re.IGNORECASE)[0].strip()
                    change[-1] = cp
                    break
        for cancel in cancel_list:
            if change[1] == cancel[1]:
                pop_list.append(cancel)
    for i in pop_list:
        try:
            cancel_list.remove(i)
        except ValueError:
            pass
    result1 = {i[1]: 'ОТМЕНА' for i in cancel_list}
    result2 = {i[1]: [i[-1], i[0], i[2]] for i in changes_list}
    result = {**result1, **result2}
    result = dict(sorted(result.items()))
    return result


def replace_changes(original: dict, changes: dict) -> dict:
    result = {}
    for change in changes:
        if change in original:
            if changes[change] == 'ОТМЕНА':
                result[change] = ['ОТМЕНА', original[change][0], original[change][1]]
            else:
                result[change] = ['ЗАМЕНА', original[change][0], original[change][1], original[change][2],
                                  changes[change][0], changes[change][1], changes[change][2]]
        else:
            result[change] = ['ДОПОЛНИТЕЛЬНО', changes[change][0], changes[change][1], changes[change][2]]
    for orig in original:
        if orig not in result:
            result[orig] = ['ОБЫЧНАЯ', original[orig][0], original[orig][1], original[orig][2]]
    result = dict(sorted(result.items()))
    return result


def get_times_para(number_para: int, clock: bool = True) -> str:
    if number_para == 1:
        if clock:
            return '🕗 8:00 – 9:30'
        else:
            return '8:00 – 9:30'
    elif number_para == 2:
        if clock:
            return '🕙 9:50 – 11:20'
        else:
            return '9:50 – 11:20'
    elif number_para == 3:
        if clock:
            return '🕛 11:50 – 13:20'
        else:
            return '11:50 – 13:20'
    elif number_para == 4:
        if clock:
            return '🕜 13:30 – 15:00'
        else:
            return '13:30 – 15:00'
    elif number_para == 5:
        if clock:
            return '🕒 15:10 – 16:40'
        else:
            return '15:10 – 16:40'
    else:
        if clock:
            return '🕔 16:50 – 18:20'
        else:
            return '16:50 – 18:20'


def create_schedule(week, current_group, date, up_or_down_week, sub) -> str:
    current_year = datetime.datetime.now().strftime('%Y')
    dates = f'{date}.{current_year}'
    if up_or_down_week == 2:
        up_week_day = 'ВЕРХНЯЯ НЕДЕЛЯ'
    else:
        up_week_day = 'НИЖНЯЯ НЕДЕЛЯ'
    schedule_text = f'<b>🗓 {current_group} {date} {up_week_day}</b>\n\n'
    if db.get_changes(dates, current_group):
        for number_par in range(1, 7):
            list_changes = db.get_chan_1(date=dates, group=current_group, num_par=number_par)
            if list_changes:
                para1_1 = ''
                para1_2 = ''
                hard_changes = f'<b> {number_par} ПАРА – ИЗМЕНЕНИЯ У ОБЕИХ ПГ</b>\n\n'
                simple_changes = f'<b> {number_par} ПАРА – ИЗМЕНЕНИЯ У ПГ</b>\n\n'
                count = 0
                for index in list_changes:  # Перебор списка с изменениями в котором 1 или 2 списка
                    count_teach = str(index[1]).split()
                    if str(index[1]).lower() == 'дополнительно':
                        if len(list_changes) > 1:
                            para1 = (f'<b>✅ {number_par} ПАРА – ДОПОЛНИТЕЛЬНО ПО ПГ</b>\n'
                                     f'<b>{get_times_para(number_par)}</b>\n'
                                     f'    🚪 {list_changes[0][0]}\n'
                                     f'    🧑‍🏫 {list_changes[0][3]}\n'
                                     f'    📖 {list_changes[0][4]}\n\n'
                                     f'    🚪 {list_changes[1][0]}\n'
                                     f'    🧑‍🏫 {list_changes[1][3]}\n'
                                     f'    📖 {list_changes[1][4]}\n\n')
                            count += 1
                            if count == 2:
                                schedule_text += para1
                                count = 0
                        else:
                            para1 = (f'<b>✅ {number_par} ПАРА – ДОПОЛНИТЕЛЬНО</b>\n'
                                     f'<b>{get_times_para(number_par)}</b>\n'
                                     f'🚪 {index[0]}\n'
                                     f'🧑‍🏫 {index[3]}\n'
                                     f'📖 {index[4]}\n\n')
                            schedule_text += para1

                    elif 'параллельно' in str(index[1]).lower():
                        para2 = (f'<b>✅ {number_par} ПАРА – ДОПОЛНИТЕЛЬНО У ПГ</b>\n'
                                 f'<b>{get_times_para(number_par)}</b>\n'
                                 f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                                 f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                                 f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n\n'
                                 f'    🚪 {index[0]}\n'
                                 f'    🧑‍🏫 {index[3]}\n'
                                 f'    📖 {index[4]}\n\n')
                        schedule_text += para2
                    elif db.get_subgroup(para=number_par, day=week,
                                         group=current_group, week=up_or_down_week) > 0:  # Если изменения по подгруппам
                        if str(index[3]).lower() == 'нет замены':  # Отмена у подгрупп
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=1) in index[1]:
                                para1_1 = (
                                    '    <b>❌ ОТМЕНА</b>\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s>\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s>\n\n')
                                count += 1
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=2) in index[1]:
                                para1_2 = (
                                    '    <b>❌ ОТМЕНА</b>\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s>\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s>\n\n')
                                count += 1
                            if count == 1 and len(list_changes) == 1:
                                if db.get_teacher(para=number_par, day=week, group=current_group,
                                                  week=up_or_down_week, subgroup=1) in index[1]:
                                    simple_changes += para1_1
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n')
                                else:
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n')
                                    simple_changes += para1_2
                                schedule_text += simple_changes
                            elif count == 2 and (len(list_changes) == 2 or len(count_teach) >= 3):
                                hard_changes += para1_1 + para1_2
                                schedule_text += hard_changes
                                count = 0
                        elif 'дистанцион' in str(index[4]).lower() and 'дистанцион' not in str(
                                index[3]).lower():  # Перенос с заменой для подгрупп
                            per = str(index[4]).lower().split('дистанцион')
                            name_para = str(per[0]).split('\n')
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=1) in index[1]:
                                para1_1 = (
                                    f'    <b>👨‍💻 ДИСТАНЦИОННО И ЗАМЕНА</b>\n'
                                    f'    <b>{get_times_para(number_par)}</b>\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {index[3]}\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {str(name_para[0]).title()}\n\n'
                                    )
                                count += 1
                            if db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week,
                                              subgroup=2) in index[1]:
                                para1_2 = (
                                    f'    <b>👨‍💻 ДИСТАНЦИОННО И ЗАМЕНА</b>\n'
                                    f'    <b>{get_times_para(number_par)}</b>\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {index[3]}\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {str(name_para[0]).title()}\n\n'
                                    )
                                count += 1
                            if count == 1 and len(list_changes) == 1:
                                if db.get_teacher(para=number_par, day=week, group=current_group,
                                                  week=up_or_down_week, subgroup=1) in index[1]:
                                    simple_changes += para1_1
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'                                        
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                                        )
                                else:
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                                        )
                                    simple_changes += para1_2
                                schedule_text += simple_changes
                            elif count == 2 and (len(list_changes) == 2 or len(count_teach) >= 3):
                                hard_changes += para1_1 + para1_2
                                schedule_text += hard_changes
                                count = 0
                        elif 'дистанцион' in str(index[3]).lower():  # Отмена у подгрупп
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=1) in index[1]:
                                para1_1 = (
                                    '    <b>👨‍💻 ДИСТАНЦИОННО</b>\n'
                                    f'    <b>{get_times_para(number_par)}</b>\n'
                                    f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                    f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                                    )
                                count += 1
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=2) in index[1]:
                                para1_2 = (
                                    '    <b>👨‍💻 ДИСТАНЦИОННО</b>\n'
                                    f'    <b>{get_times_para(number_par)}</b>\n'
                                    f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                    f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                                    )
                                count += 1
                            if count == 1 and len(list_changes) == 1:
                                if db.get_teacher(para=number_par, day=week, group=current_group,
                                                  week=up_or_down_week, subgroup=1) in index[1]:
                                    simple_changes += para1_1
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n')
                                else:
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                                        )
                                    simple_changes += para1_2
                                schedule_text += simple_changes
                            elif count == 2 and (len(list_changes) == 2 or len(count_teach) >= 3):
                                hard_changes += para1_1 + para1_2
                                schedule_text += hard_changes
                                count = 0
                        elif 'перенос на' in str(index[4]).lower() and 'перенос на' not in str(
                                index[3]).lower():  # Перенос с заменой для подгрупп
                            per = str(index[4]).lower().split('перенос ')
                            num = str(per[-1]).split()
                            clocks = get_times_para(number_par).split()[0]
                            name_para = str(per[0]).split('\n')
                            time_par = get_times_para(number_par, False)
                            for times_changes in range(1, 7):
                                try:
                                    if f'{times_changes}' in num[1] or f'{times_changes}' == num[2]:
                                        time_par = get_times_para(times_changes, False)
                                        break
                                except IndexError:
                                    break
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=1) in index[1]:
                                para1_1 = (
                                    f'    <b>❗ ЗАМЕНА И ПЕРЕНОС {str(per[-1]).upper()}</b>\n'
                                    f'    {clocks} <s>{get_times_para(number_par, False)}</s> ⮕ <b>{time_par}</b>\n'
                                    f'    🚪 <s>{db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {index[0]}\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {index[3]}\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {str(name_para[0]).title()}\n\n'
                                    )
                                count += 1
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=2) in index[1]:
                                para1_2 = (
                                    f'    <b>❗ ЗАМЕНА И ПЕРЕНОС {str(per[-1]).upper()}</b>\n'
                                    f'    {clocks} <s>{get_times_para(number_par, False)}</s> ⮕ <b>{time_par}</b>\n'
                                    f'    🚪 <s>{db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {index[0]}\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {index[3]}\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {str(name_para[0]).title()}\n\n'
                                    )
                                count += 1
                            if count == 1 and len(list_changes) == 1:
                                if db.get_teacher(para=number_par, day=week, group=current_group,
                                                  week=up_or_down_week, subgroup=1) in index[1]:
                                    simple_changes += para1_1
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                                        )
                                else:
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                                        )
                                    simple_changes += para1_2
                                schedule_text += simple_changes
                            elif count == 2 and (len(list_changes) == 2 or len(count_teach) >= 3):
                                hard_changes += para1_1 + para1_2
                                schedule_text += hard_changes
                                count = 0
                        elif 'перенос' in str(index[3]).lower():  # Обычный перенос для подгрупп
                            num = str(index[3]).lower().split()
                            clocks = get_times_para(number_par).split()[0]
                            time_par = get_times_para(number_par, False)
                            for times_changes in range(1, 7):
                                try:
                                    if f'{times_changes}' in num[2]:
                                        time_par = get_times_para(times_changes, False)
                                        break
                                except IndexError:
                                    break
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=1) in index[1]:
                                para1_1 = (
                                    f'    <b>❗ {str(index[3]).upper()}</b>\n'
                                    f'    {clocks} <s>{get_times_para(number_par, False)}</s> ⮕ <b>{time_par}</b>\n'
                                    f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                    f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                    f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n')

                                count += 1
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=2) in index[1]:
                                para1_2 = (
                                    f'    <b>❗ {str(index[3]).upper()}</b>\n'
                                    f'    {clocks} <s>{get_times_para(number_par, False)}</s> ⮕ <b>{time_par}</b>\n'
                                    f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                    f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                    f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                                    )
                                count += 1
                            if count == 1 and len(list_changes) == 1:
                                if db.get_teacher(para=number_par, day=week, group=current_group,
                                                  week=up_or_down_week, subgroup=1) in index[1]:
                                    simple_changes += para1_1
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                                        )
                                else:
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                                        )
                                    simple_changes += para1_2
                                schedule_text += simple_changes
                            elif count == 2 and (len(list_changes) == 2 or len(count_teach) >= 3):
                                hard_changes += para1_1 + para1_2
                                schedule_text += hard_changes
                                count = 0
                        else:  # Замена для подгруппы
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=1) in index[1]:
                                para1_1 = (
                                    '    <b>❗ ЗАМЕНА</b>\n'
                                    f'    <b>{get_times_para(number_par)}</b>\n'
                                    f'    🚪 <s>{db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {index[0]}\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {index[3]}\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}</s> ⮕ {index[4]}\n\n'
                                    )

                                count += 1
                            if db.get_teacher(para=number_par, day=week, group=current_group,
                                              week=up_or_down_week, subgroup=2) in index[1]:
                                para1_2 = (
                                    '    <b>❗ ЗАМЕНА</b>\n'
                                    f'    <b>{get_times_para(number_par)}</b>\n'
                                    f'    🚪 <s>{db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {index[0]}\n'
                                    f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {index[3]}\n'
                                    f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}</s> ⮕ {index[4]}\n\n'
                                    )
                                count += 1
                            if count == 1 and len(list_changes) == 1:
                                if db.get_teacher(para=number_par, day=week, group=current_group,
                                                  week=up_or_down_week, subgroup=1) in index[1]:
                                    simple_changes += para1_1
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                                        )
                                else:
                                    simple_changes += (
                                        f'    <b>{get_times_para(number_par)}</b>\n'
                                        f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                        f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                                        )
                                    simple_changes += para1_2
                                schedule_text += simple_changes
                            elif count == 2 and (len(list_changes) == 2 or len(count_teach) >= 3):
                                hard_changes += para1_1 + para1_2
                                schedule_text += hard_changes
                                count = 0

                    else:  # Изменения на обычные пары
                        if str(index[3]).lower() == 'нет замены':  # Отмена обычной пары
                            para1 = (f'<b>❌ {number_par} ПАРА – ОТМЕНА</b>\n'
                                     f'<s>🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s>\n'
                                     f'<s>📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s>\n\n'
                                     )
                            schedule_text += para1
                        else:  # Изменения С Обычных На Подгруппы и Обычные на Обычные
                            if len(list_changes) > 1 or len(count_teach) >= 3:  # Если замена для подгрупп
                                para1 = (f'<b>❗ {number_par} ПАРА – ЗАМЕНА НА ПОДГРУППЫ</b>\n'
                                         f'    🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s>\n'
                                         f'    📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s>\n\n'
                                         f'    <b>{get_times_para(number_par)}</b>\n'
                                         f'    🚪 {list_changes[0][0]}\n'
                                         f'    🧑‍🏫 {list_changes[0][3]}\n'
                                         f'    📖 {list_changes[0][4]}\n\n'
                                         f'    <b>{get_times_para(number_par)}</b>\n'
                                         f'    🧑‍🏫 {list_changes[1][3]}\n'
                                         f'    🚪 {list_changes[1][0]}\n'
                                         f'    📖 {list_changes[1][4]}\n\n'
                                         )
                                count += 1
                                if count == 2:
                                    schedule_text += para1
                                    count = 0
                            else:  # Дефолтные изменения
                                if 'дистанцион' in str(index[4]).lower() and 'дистанцион' not in str(
                                        index[3]).lower():  # Перенос с заменой
                                    per = str(index[4]).lower().split('дистанцион')
                                    name_para = str(per[0]).split('\n')
                                    para1 = (f'<b>👨‍💻 {number_par} ПАРА – ДИСТАНЦИОННО И ЗАМЕНА</b>\n'
                                             f'<b>{get_times_para(number_par)}</b>\n'
                                             f'🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {index[3]}\n'
                                             f'📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {str(name_para[0]).title()}\n\n'
                                             )
                                    schedule_text += para1

                                elif 'дистанцион' in str(index[3]).lower():  # Обычный перенос
                                    para1 = (f'<b>👨‍💻 {number_par} ПАРА – ДИСТАНЦИОННО</b>\n'
                                             f'<b>{get_times_para(number_par)}</b>\n'
                                             f'🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                                             f'📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n\n'
                                             )
                                    schedule_text += para1

                                elif 'перенос на' in str(index[4]).lower() and 'перенос на' not in str(
                                        index[3]).lower():  # Перенос с заменой
                                    per = str(index[4]).lower().split('перенос ')
                                    num = str(per[-1]).split()
                                    clocks = get_times_para(number_par).split()[0]
                                    time_par = get_times_para(number_par, False)
                                    for times_changes in range(1, 7):
                                        try:
                                            if f'{times_changes}' in num[1] or f'{times_changes}' == num[2]:
                                                time_par = get_times_para(times_changes, False)
                                                break
                                        except IndexError:
                                            break
                                    name_para = str(per[0]).split('\n')
                                    para1 = (f'<b>❗ {number_par} ПАРА – ЗАМЕНА И ПЕРЕНОС {str(per[1]).upper()}</b>\n'
                                             f'{clocks} <s>{get_times_para(number_par, False)}</s> ⮕ <b>{time_par}</b>\n'
                                             f'🚪 <s>{db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {index[0]}\n'
                                             f'🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {index[3]}\n'
                                             f'📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {str(name_para[0]).title()}\n\n'
                                             )
                                    schedule_text += para1
                                elif 'перенос' in str(index[3]).lower():  # Обычный перенос
                                    num = str(index[3]).lower().split()
                                    clocks = get_times_para(number_par).split()[0]
                                    time_par = get_times_para(number_par, False)
                                    for times_changes in range(1, 7):
                                        try:
                                            if f'{times_changes}' in num[2]:
                                                time_par = get_times_para(times_changes, False)
                                                break
                                        except IndexError:
                                            break
                                    para1 = (f'<b>❗ {number_par} ПАРА – {str(index[3]).upper()}</b>\n'
                                             f'{clocks} <s>{get_times_para(number_par, False)}</s> ⮕ <b>{time_par}</b>\n'
                                             f'🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                                             f'🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                                             f'📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n\n'
                                             )
                                    schedule_text += para1
                                else:
                                    para1 = (f'<b>❗ {number_par} ПАРА – ЗАМЕНА</b>\n'
                                             f'<b>{get_times_para(number_par)}</b>\n'
                                             f'🚪 <s>{db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {index[0]}\n'
                                             f'🧑‍🏫 <s>{db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {index[3]}\n'
                                             f'📖 <s>{db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}</s> ⮕ {index[4]}\n\n'
                                             )
                                    schedule_text += para1
            else:
                if db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week):
                    if db.get_subgroup(para=number_par, day=week, group=current_group, week=up_or_down_week) > 0:
                        para = (f'<b> {number_par} ПАРА</b>\n'
                                f'<b>{get_times_para(number_para=number_par)}</b>\n'
                                f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                                f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                                f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                                f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                                )
                    else:
                        para = (f'<b> {number_par} ПАРА</b>\n'
                                f'<b>{get_times_para(number_para=number_par)}</b>\n'
                                f'🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                                f'🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                                f'📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n\n'
                                )
                    schedule_text += para

    else:
        for number_par in range(1, 7):
            if db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week):
                if db.get_subgroup(para=number_par, day=week, group=current_group, week=up_or_down_week) > 0:
                    para = (f'<b> {number_par} ПАРА</b>\n'
                            f'<b>{get_times_para(number_para=number_par)}</b>\n'
                            f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                            f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n'
                            f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=1)}\n\n'
                            f'    🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                            f'    🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n'
                            f'    📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=2)}\n\n'
                            )
                else:
                    para = (f'<b> {number_par} ПАРА</b>\n'
                            f'<b>{get_times_para(number_para=number_par)}</b>\n'
                            f'🚪 {db.get_door(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                            f'🧑‍🏫 {db.get_teacher(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n'
                            f'📖 {db.get_para(para=number_par, day=week, group=current_group, week=up_or_down_week, subgroup=0)}\n\n'
                            )
                schedule_text += para

    find_pr_chn = find_prim_changes(week, dates, current_group, up_or_down_week)
    if find_pr_chn:
        schedule_text += f'{find_pr_chn}\n\n'
    tomorrow_chang = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')
    if dates == str(tomorrow_chang):
        if str(current_group).lower() in campus_1:
            if db.check_changes(dates, 1):
                schedule_text += '✔️ ИЗМЕНЕНИЯ 1 КОРПУСА ДОБАВЛЕНЫ'
            else:
                schedule_text += '✖️ ИЗМЕНЕНИЯ 1 КОРПУСА НЕ ВЫЛОЖЕНЫ'
        elif str(current_group).lower() in campus_2:
            if db.check_changes(dates, 2):
                schedule_text += '✔️ ИЗМЕНЕНИЯ 2 КОРПУСА ДОБАВЛЕНЫ'
            else:
                schedule_text += '✖️ ИЗМЕНЕНИЯ 2 КОРПУСА НЕ ВЫЛОЖЕНЫ'
    if schedule_text == f'🗓 {current_group} {date} {up_week_day}\n\n':
        schedule_text += '<b>Занятий на этот день не найдено</b>'

    return schedule_text


def time_schedule(time: int) -> str:
    if time == 1:
        times = '<b>🕗 8:00 – 9:30</b>'
    elif time == 2:
        times = '<b>🕙 9:50 – 11:20</b>'
    elif time == 3:
        times = '<b>🕛 11:50 – 13:20</b>'
    elif time == 4:
        times = '<b>🕜 13:30 – 15:00</b>'
    elif time == 5:
        times = '<b>🕒 15:10 – 16:40</b>'
    else:
        times = '<b>🕔 16:50 – 18:20</b>'
    return times


def create_schedule_teach(week, teacher_name, date, up_or_down_week, sub) -> str:
    current_year = datetime.datetime.now().strftime('%Y')
    dates = f'{date}.{current_year}'
    if up_or_down_week == 2:
        up_week_day = 'ВЕРХНЯЯ НЕДЕЛЯ'
    else:
        up_week_day = 'НИЖНЯЯ НЕДЕЛЯ'
    schedule_text = f'<b>🗓 {teacher_name} {date} {up_week_day}</b>\n\n'
    pars = db.get_para_teach(day=week, teacher=teacher_name, week=up_or_down_week)
    chang = data_processing_teacher(teacher_name=teacher_name, date=dates)
    if chang:  # Есть ли изменения
        schedule_changes = replace_changes(original=pars, changes=chang)
        for couple in schedule_changes:
            time = time_schedule(couple)
            if schedule_changes[couple][0] == 'ДОПОЛНИТЕЛЬНО':
                schedule_text += (f'✅ <b>{couple} ПАРА – ДОПОЛНИТЕЛЬНО</b>\n'
                                  f'{time}\n'
                                  f'🚪 {schedule_changes[couple][3]}\n'
                                  f'👨‍🎓 {schedule_changes[couple][2]}\n'
                                  f'📖 {schedule_changes[couple][1]}\n\n'
                                  )
            elif schedule_changes[couple][0] == 'ОТМЕНА':
                schedule_text += (f'❌ <b>{couple} ПАРА – ОТМЕНА</b>\n'
                                  f'👨‍🎓 <s>{schedule_changes[couple][2]}</s>\n'
                                  f'📖 <s>{schedule_changes[couple][1]}</s>\n\n')
            elif schedule_changes[couple][0] == 'ЗАМЕНА':
                schedule_text += (f'❗ <b>{couple} ПАРА – ЗАМЕНА</b>\n'
                                  f'{time}\n'
                                  f'🚪 <s>{schedule_changes[couple][3]}</s> ⮕ {schedule_changes[couple][6]}\n'
                                  f'👨‍🎓 <s>{schedule_changes[couple][2]}</s> ⮕ {schedule_changes[couple][5]}\n'
                                  f'📖 <s>{schedule_changes[couple][1]}</s> ⮕ {schedule_changes[couple][4]}\n\n'
                                  )
            elif schedule_changes[couple][0] == 'ОБЫЧНАЯ':
                schedule_text += (f'<b> {couple} ПАРА</b>\n'
                                  f'{time}\n'
                                  f'🚪 {schedule_changes[couple][3]}\n'
                                  f'👨‍🎓 {schedule_changes[couple][2]}\n'
                                  f'📖 {schedule_changes[couple][1]}\n\n'
                                  )
    else:  # Нет изменений
        for i in pars:
            time = time_schedule(i)
            schedule_text += (f'<b> {i} ПАРА</b>\n'
                              f'{time}\n'
                              f'🚪 {pars[i][2]}\n'
                              f'👨‍🎓 {pars[i][1]}\n'
                              f'📖 {pars[i][0]}\n\n'
                              )

    if schedule_text == f'<b>🗓 {teacher_name} {date} {up_week_day}</b>\n\n':
        schedule_text += '<b>У преподавателя нет занятий на этот день</b>'

    return schedule_text
