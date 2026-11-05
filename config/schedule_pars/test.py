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
        find_doors = re.compile(r'\(\s*(\d+ корпус|\d+|сп\. зал)\s*\)')
        if len(res) > 2:
            for index, i in enumerate(res):
                work = [day, number]
                if index == 1:
                    match = find_doors.search(i)
                    if match:
                        work.append(match.group(1))
                        res[1] = res[1].replace(match.group(1), "")
                        if '()' in res[1]:
                            res[1] = res[1].replace("()", "")
                    else:
                        work.append('')
                    work.append(str(res[0]).strip())
                    work.append(teachers[0])
                    work_lists.append(work)
                    continue
                elif index == 2:
                    match = find_doors.search(i)
                    if match:
                        work.append(match.group(1))
                    else:
                        work.append('')
                    work.append(str(res[1]).strip())
                    work.append(teachers[1])
                    work_lists.append(work)
                    break
        else:
            work = [day, number]
            match = find_doors.search(res[-1])
            if match:
                work.append(match.group(1))
            else:
                work.append('')
            work.append(str(res[0]).strip())
            work.append(teachers[0])
            work_lists.append(work)

        return work_lists

def parsing_changes(pdf_file):
    work_list = []
    count_group_list = 0
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
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
                                            a = rw.replace('\n', '')
                                            day_week = a[::-1]
                                            row[index] = a[::-1]
                                        else:
                                            row[index] = rw.replace('\n', ' ')

                                except TypeError:
                                    if index == 0:
                                        row[index] = day_week
                            row.pop(1)
                    else:
                        for index, rw in enumerate(row):
                            try:
                                if '\n' in rw:
                                    if index == 0:
                                        a = rw.replace('\n', '')
                                        day_week = a[::-1]
                                        row[index] = a[::-1]
                                    else:
                                        row[index] = rw.replace('\n', ' ')

                            except TypeError:
                                if index == 0:
                                    row[index] = day_week
                        row.pop(1)

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
            if num_par is None: # Если верхняя или нижняя
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

    # for i in schedule_dict:
    #     print(i)
    #     for j in schedule_dict[i]:
    #         print(j)
    #     print()
    return schedule_dict


# parsing_changes("config/1_курс.pdf")
