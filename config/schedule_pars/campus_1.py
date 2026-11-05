import re
import pdfplumber


def find_groups(s: str):
    pattern = r'\d{2}[А-Я]{1,3}'
    groups = re.findall(pattern, s)
    return groups


def process_schedule_item(items):
    day, number, description = items
    if not description or not day:
        return [[day, number, '', description, '']]
    else:
        teacher_pattern = re.compile(r'[А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.')
        teachers = teacher_pattern.findall(description)
        modified_description = description
        for i in teachers:
            modified_description = modified_description.replace(f"{i}", '_TEACHER_')
        res = modified_description.split('_TEACHER_')
        work_lists = []
        if len(teachers) > 1:
            for index, i in enumerate(res):
                try:
                    number_and_door = number.split()
                except AttributeError:
                    work = [day, number, '']
                    if index == 0:
                        work.append(str(i).strip())
                        work.append(teachers[0])
                        work_lists.append(work)
                        continue
                    elif index == 1:
                        if str(i).strip():
                            work.append(str(i).strip())
                        else:
                            work.append(str(res[0]).strip())
                        work.append(teachers[1])
                        work_lists.append(work)
                        break
                else:
                    work = [day, str(number).strip()[0]]
                    if index == 0:
                        try:
                            work.append(number_and_door[1])
                        except IndexError:
                            work.append('')
                        work.append(str(i).strip())
                        work.append(teachers[0])
                        work_lists.append(work)
                        continue
                    elif index == 1:
                        try:
                            work.append(number_and_door[2])
                        except IndexError:
                            work.append('')
                        if str(i).strip():
                            work.append(str(i).strip())
                        else:
                            work.append(str(res[0]).strip())
                        work.append(teachers[1])
                        work_lists.append(work)
                        break
        else:
            try:
                if number:
                    number = number.split()
                else:
                    raise AttributeError
            except AttributeError:
                return [[day, number, '', str(res[0]).strip(), teachers[0]]]
            else:
                work = [day, number[0]]
                try:
                    if len(number) > 2:
                        work.append(f'{number[1]} {number[2]}')
                    else:
                        work.append(number[1])
                except IndexError:
                    work.append('')
                work.append(str(res[0]).strip())
                work.append(teachers[0])
                work_lists.append(work)

        return work_lists


# my = [
#     ['понедельник', '1 301', 'МДК 02.01 Практ. осн. БУ источн. формир. активов организ. Морозова И.Г.'],
#     ['вторник', '2 310 414', 'Иностр. язык в проф. деятельности Сатаева Т.И. Никитина И.А.'],
#     ['среда', '3 405', 'МДК 06.01 Выполн. работ «Кассир» Зубарева Е.Д.'],
#     ['вторник', None, 'МДК 04.01 Мухин Н.А. Архитектура апп. ср. Циркова В.В.'],
#     ['среда', '4 409 101', 'Ин. яз. в проф. деят. Канакова А.Е. Осн. алг. и прогр. Мамшева Ю.С.']
# ]
# for i in my:
#     print(process_schedule_item(i))


def parsing_changes(pdf_file):
    work_list = []
    count_group_list = 0
    count_page = -1
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            count_page += 1
            back_day = 0
            day_weeks = ''
            for table in tables:
                day_week = ''
                for index_row, row in enumerate(table):
                    if index_row == 0:
                        lst = []
                        for index, rw in enumerate(row):
                            try:
                                at = find_groups(rw)
                                if at:
                                    lst.append(at[0])
                            except TypeError:
                                pass
                        if lst:
                            row = tuple(lst)
                            count_group_list += 1
                        else:
                            for index, rw in enumerate(row):
                                try:
                                    if '\n' in rw:
                                        if index == 0:
                                            if count_group_list == 2:
                                                if count_page % 2 == 0:
                                                    a = rw.replace('\n', '')
                                                    day_week = a[::-1]
                                                    row[index] = a[::-1]
                                                else:
                                                    row[index] = rw.replace('\n', ' ')
                                            else:
                                                a = rw.replace('\n', '')
                                                day_week = a[::-1]
                                                row[index] = a[::-1]
                                        else:
                                            row[index] = rw.replace('\n', ' ')

                                except TypeError:
                                    if index == 0:
                                        row[index] = day_week
                            if count_group_list == 2:
                                if count_page % 2 == 0:
                                    row.pop(1)
                            else:
                                row.pop(1)
                    else:
                        for index, rw in enumerate(row):
                            try:
                                if '\n' in rw:
                                    if '\n' in rw:
                                        if index == 0:
                                            if count_group_list == 2:
                                                if count_page % 2 == 0:
                                                    a = rw.replace('\n', '')
                                                    day_week = a[::-1]
                                                    row[index] = a[::-1]
                                                else:
                                                    row[index] = rw.replace('\n', ' ')
                                            else:
                                                a = rw.replace('\n', '')
                                                day_week = a[::-1]
                                                row[index] = a[::-1]
                                        else:
                                            row[index] = rw.replace('\n', ' ')

                            except TypeError:
                                if index == 0:
                                    row[index] = day_week
                        if count_group_list == 2:
                            if count_page % 2 == 0:
                                row.pop(1)
                        else:
                            row.pop(1)
                    if count_page % 2 != 0 and type(row) == list and count_group_list == 2:
                        if count_page == 1:
                            if row[0] and row[0][0] == '1':
                                if back_day == 0:
                                    day_weeks = 'понедельник'
                                    row.insert(0, day_weeks)
                                else:
                                    day_weeks = 'вторник'
                                    row.insert(0, day_weeks)
                                back_day = 1
                            else:
                                row.insert(0, day_weeks)
                        elif count_page == 3:
                            if row[0] and row[0][0] == '1':
                                if back_day == 0:
                                    day_weeks = 'среда'
                                    row.insert(0, day_weeks)
                                else:
                                    day_weeks = 'четверг'
                                    row.insert(0, day_weeks)
                                back_day = 1
                            else:
                                row.insert(0, day_weeks)
                        elif count_page == 5:
                            if row[0] and row[0][0] == '1':
                                if back_day == 0:
                                    day_weeks = 'пятница'
                                    row.insert(0, day_weeks)
                                else:
                                    day_weeks = 'суббота'
                                    row.insert(0, day_weeks)
                                back_day = 1
                            else:
                                row.insert(0, day_weeks)
                    work_list.append(row)
    schedule_dict = {}
    if count_group_list == 2:
        steps = 0
        groups_one = []
        groups_two = []
        srd = 0
        pt = 0
        for index, work in enumerate(work_list):
            if type(work) == tuple:
                if steps == 1:
                    groups_two = work
                    steps = 2
                else:
                    groups_one = work
                    steps = 1
            else:
                count_step = 1
                if work[0] == 'понедельник':
                    if steps == 2:
                        for group in groups_two:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                    else:
                        for group in groups_one:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                elif work[0] == 'вторник':
                    if steps == 2:
                        for group in groups_two:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                    else:
                        for group in groups_one:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                elif work[0] == 'среда':
                    if work_list[index - 1][0] == 'четверг' or srd == 1:
                        for group in groups_two:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                        srd = 1
                    else:
                        for group in groups_one:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                elif work[0] == 'четверг':
                    if srd == 1:
                        for group in groups_two:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                    else:
                        for group in groups_one:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                elif work[0] == 'пятница':
                    if work_list[index - 1][0] == 'суббота' or pt == 1:
                        for group in groups_two:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                        pt = 1
                    else:
                        for group in groups_one:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                elif work[0] == 'суббота':
                    if pt == 1:
                        for group in groups_two:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
                    else:
                        for group in groups_one:
                            if group in schedule_dict:
                                rasp = schedule_dict[group]
                                rasp.append([work[0], work[count_step], work[count_step + 1]])
                                schedule_dict[group] = rasp
                            else:
                                schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                            count_step += 2
    else:
        groups = []
        for index, work in enumerate(work_list):
            if type(work) == tuple:
                groups = work
            else:
                count_step = 1
                for group in groups:
                    if group in schedule_dict:
                        rasp = schedule_dict[group]
                        rasp.append([work[0], work[count_step], work[count_step + 1]])
                        schedule_dict[group] = rasp
                    else:
                        schedule_dict[group] = [[work[0], work[count_step], work[count_step + 1]]]
                    count_step += 2

    for i in schedule_dict:
        new_list = []
        for j in schedule_dict[i]:
            new_list.extend(process_schedule_item(j))
        schedule_dict[i] = new_list

    for i in schedule_dict:
        true_list = []
        count = -1
        for index, j in enumerate(schedule_dict[i]):
            week_day, num_par, door, para, teacher = j
            if num_par is None or num_par == '': # Если верхняя или нижняя
                if para == '' and true_list[count][3] != '' and true_list[count][3] is not None: # только верхняя
                    true_list[count].append(2)
                    true_list[count].append(0)
                elif para != '' and para is not None and schedule_dict[i][index - 1][3] == '': # только нижняя
                    j[1] = schedule_dict[i][index - 1][1]
                    j.append(1)
                    j.append(0)
                    true_list.append(j)
                    count += 1
                elif para != '' and para is not None and true_list[count][3] != '' and true_list[count][3] is not None: # верхняя и нижняя
                    if j[2] == '':
                        doors = str(true_list[count][2]).split()
                        if len(doors) > 1:
                            true_list[count][2] = doors[0]
                            j[2] = doors[1]
                        else:
                            j[2] = true_list[count][2]
                    j[1] = true_list[count][1]
                    j.append(1)
                    j.append(0)
                    true_list[count].append(2)
                    true_list[count].append(0)
                    true_list.append(j)
                    count += 1
                else:
                    continue
            elif not para or not teacher:
                continue
            elif true_list and true_list[count][1] == num_par and week_day == true_list[count][0]:
                true_list[count].append(0)
                true_list[count].append(1)
                j.append(0)
                j.append(2)
                true_list.append(j)
                count += 1
            else:
                true_list.append(j)
                count += 1
        for tl in true_list:
            if None not in tl:
                if len(tl) < 7:
                    tl.append(0)
                    tl.append(0)
        schedule_dict[i] = true_list

    for i in schedule_dict:
        for j in schedule_dict[i]:
            week_day = j[0]
            if week_day == 'понедельник':
                j[0] = 0
            elif week_day == 'вторник':
                j[0] = 1
            elif week_day == 'среда':
                j[0] = 2
            elif week_day == 'четверг':
                j[0] = 3
            elif week_day == 'пятница':
                j[0] = 4
            elif week_day == 'суббота':
                j[0] = 5
            if len(j[1]) > 1:
                nm = j[1].split()
                j[1] = nm[0]
                j[2] = nm[1]

    for i in schedule_dict:
        print(i)
        for j in schedule_dict[i]:
            print(j)
        print()
    return schedule_dict


# parsing_changes("config/1_1_ВБ.pdf")