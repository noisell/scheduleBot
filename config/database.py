import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cur = self.conn.cursor()

    def user_exists(self, user_id):
        with self.conn:
            result = self.cur.execute('SELECT * FROM `users` WHERE `user_id` = ?',
                                      (user_id,)).fetchall()
            return bool(len(result))

    def user_exists_leader(self, user_id):
        with self.conn:
            result = self.cur.execute('SELECT * FROM `leaders` WHERE `user_id` = ?',
                                      (user_id,)).fetchall()
            return bool(len(result))

    def group_exists_leader(self, group):
        with self.conn:
            result = self.cur.execute('SELECT * FROM `leaders` WHERE `group` = ?',
                                      (group,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id: int, username: str = None, referrer_id: int = False):
        with self.conn:
            if referrer_id:
                if username is not None:
                    return self.cur.execute('INSERT INTO `users` (`user_id`, `username`, `referrer_id`, `get_bonus`) VALUES (?,?,?,0)',
                                            (user_id, username, referrer_id))
                else:
                    return self.cur.execute('INSERT INTO `users` (`user_id`, `referrer_id`, `get_bonus`) VALUES (?,?,0)', (user_id, referrer_id))
            else:
                if username is not None:
                    return self.cur.execute('INSERT INTO `users` (`user_id`, `username`) VALUES (?,?)',
                                            (user_id, username,))
                else:
                    return self.cur.execute('INSERT INTO `users` (`user_id`) VALUES (?)', (user_id,))

    def user_exists_love(self, user_id):
        with self.conn:
            result = self.cur.execute('SELECT * FROM `love` WHERE `user_id` = ?',
                                      (user_id,)).fetchall()
            return bool(len(result))

    def add_user_love(self, user_id):
        with self.conn:
            return self.cur.execute('INSERT INTO `love` (`user_id`) VALUES (?)',
                                    (user_id,))

    def add_leader_user(self, user_id, group):
        with self.conn:
            return self.cur.execute('INSERT INTO `leaders` (`user_id`, `group`) VALUES (?,?)',
                                    (user_id, group,))

    def update_date(self, current_date, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `users` SET `cur_date` = ? WHERE `user_id` = ?', (current_date, user_id,))

    def select_cur_date(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `cur_date` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_group(self, group, user_id):
        with self.conn:
            try:
                return self.cur.execute('UPDATE `users` SET `current_group` = ? WHERE `user_id` = ?', (group, user_id,))
            except Exception as e:
                print(f'Произошла ошибка: {e}')

    def select_current_group(self, user_id):
        with self.conn:
            try:
                return self.cur.execute('SELECT `current_group` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[0]
            except Exception as e:
                print(f'Произошла ошибка: {e}')

    # Для получения расписания #############################################################################################################################################

    def get_para(self, para, day, group, week, subgroup=None):
        with self.conn:
            try:
                if subgroup is not None:
                    return self.cur.execute(
                        'SELECT `name_para` FROM `rasp` WHERE `count_para` = ? and `group` = ? and `day` = ? and (`up_week` = ? or `up_week` = 0) and `subgroup` = ?',
                        (para, group, day, week, subgroup,)).fetchone()[0]
                else:
                    return self.cur.execute(
                        'SELECT `name_para` FROM `rasp` WHERE `count_para` = ? and `group` = ? and `day` = ? and (`up_week` = ? or `up_week` = 0)',
                        (para, group, day, week,)).fetchone()[0]
            except:
                return False

    def get_para_teach(self, day, teacher, week):
        with self.conn:
            result = {}
            try:
                res = self.cur.execute(
                    'SELECT `count_para`, `name_para`, `group`, `door` FROM `rasp` WHERE `teacher` = ? and `day` = ? and (`up_week` = ? or `up_week` = 0)',
                    (teacher, day, week,)).fetchall()
                for i in res:
                    result[i[0]] = [i[1], i[2], i[3]]
                sorted_dict = {k: result[k] for k in sorted(result)}
                return sorted_dict
            except:
                return False

    def get_door(self, para, day, group, week, subgroup):
        with self.conn:
            try:
                return self.cur.execute(
                    'SELECT `door` FROM `rasp` WHERE `count_para` = ? and `group` = ? and `day` = ? and (`up_week` = ? or `up_week` = 0) and `subgroup` = ?',
                    (para, group, day, week, subgroup,)).fetchone()[0]
            except:
                return False

    def get_teacher(self, para, day, group, week, subgroup):
        with self.conn:
            try:
                return self.cur.execute(
                    'SELECT `teacher` FROM `rasp` WHERE `count_para` = ? and `group` = ? and `day` = ? and (`up_week` = ? or `up_week` = 0) and `subgroup` = ?',
                    (para, group, day, week, subgroup,)).fetchone()[0]
            except:
                return False

    def get_subgroup(self, para, day, group, week):
        with self.conn:
            try:
                return self.cur.execute(
                    'SELECT `subgroup` FROM `rasp` WHERE `group` = ? and `day` = ? and (`up_week` = ? or `up_week` = 0) and `count_para` = ?',
                    (group, day, week, para)).fetchone()[0]
            except Exception as e:
                print(f"Произошла ошибка: {e}")

    # Для Изменений ############################################################################################################################################

    def add_changes(self, date, insert_date, campus, group, up_week, num_par, door, absent1, par1, absent2, par2):
        with self.conn:
            return self.cur.execute(
                'INSERT INTO `changes` (`date`, `insert_date`, `campus`, `group`, `up_week`, `num_par`, `door`, `absent1`, `par1`, `absent2`, `par2`) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (date, insert_date, campus, group, up_week, num_par, door, absent1, par1, absent2, par2,))

    def get_changes(self, date, group):
        with self.conn:
            result = self.cur.execute('SELECT * FROM changes WHERE `date` = ? and `group` = ?',
                                      (date, group,)).fetchall()
            if len(result) > 0:
                return True
            else:
                return False

    def get_changes_teach(self, date, teacher):
        with self.conn:
            result = self.cur.execute('SELECT * FROM changes WHERE `date` = ? and (`absent1` = ? or `absent2` = ?)',
                                      (date, teacher, teacher,)).fetchall()
            return result

    def get_chan_1(self, date, group, num_par):
        with self.conn:
            try:
                result = []
                res = self.cur.execute(
                    'SELECT `door`, `absent1`, `par1`, `absent2`, `par2` FROM changes WHERE `date` = ? and `group` = ? and `num_par` = ?',
                    (date, group, num_par,)).fetchall()
                for it in res:
                    count = []
                    for i in it:
                        count.append(i)
                    result.append(count)
                return result
            except IndexError:
                return False

    def get_date(self, camp):
        with self.conn:
            return self.cur.execute('SELECT `date` FROM `dates` WHERE `id` = ?', (camp,)).fetchone()[0]

    def set_date(self, date, camp):
        with self.conn:
            return self.cur.execute('UPDATE `dates` SET `date` = ? WHERE `id` = ?', (date, camp,))

    def get_update(self, camp):
        with self.conn:
            return self.cur.execute('SELECT `update` FROM `dates` WHERE `id` = ?', (camp,)).fetchone()[0]

    def set_update(self, date, camp):
        with self.conn:
            return self.cur.execute('UPDATE `dates` SET `update` = ? WHERE `id` = ?', (date, camp,))

    def len_para(self, para, date, group):
        with self.conn:
            result = self.cur.execute('SELECT * FROM changes WHERE `group` = ? and `date` = ? and `num_par` = ?',
                                      (group, date, para,)).fetchall()
            return len(result)

    def get_id_chan(self, date, campus):
        with self.conn:
            try:
                result = []
                res = self.cur.execute('SELECT `id` FROM changes WHERE `insert_date` = ? and `campus` = ?',
                                       (date, campus,)).fetchall()
                for it in res:
                    for i in it:
                        result.append(i)
                return result
            except:
                return False

    def get_id_teach(self, date, campus):
        with self.conn:
            try:
                result = []
                res = self.cur.execute('SELECT `id` FROM `teach` WHERE `insert_date` = ? and `campus` = ?',
                                       (date, campus,)).fetchall()
                for it in res:
                    for i in it:
                        result.append(i)
                return result
            except:
                return False

    def delete_changes(self, id_ch):
        with self.conn:
            return self.cur.execute('DELETE FROM `changes` WHERE `id` = ?', (id_ch,))

    def delete_teach(self, id_tch):
        with self.conn:
            return self.cur.execute('DELETE FROM `teach` WHERE `id` = ?', (id_tch,))

    def get_notice_time(self, user_id):
        with self.conn:
            return \
                self.cur.execute('SELECT `notice_morning_time` FROM `users` WHERE `user_id` = ?',
                                 (user_id,)).fetchone()[0]

    def get_notice_changes(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `notice_changes` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[
                0]

    def get_notice_morn(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `notice_morning` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[
                0]

    def set_notice_time(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `users` SET `notice_morning_time` = ? WHERE `user_id` = ?',
                                    (value, user_id,))

    def set_notice_changes(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `users` SET `notice_changes` = ? WHERE `user_id` = ?', (value, user_id,))

    def set_notice_morn(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `users` SET `notice_morning` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_all_users(self):
        with self.conn:
            list_users = []
            result = self.cur.execute('SELECT `user_id` FROM `users`').fetchall()
            for i in range(len(result)):
                list_users.append(result[i][0])
            return list_users

    def get_all_users_love(self):
        with self.conn:
            list_users = []
            result = self.cur.execute('SELECT `user_id` FROM `love`').fetchall()
            for i in range(len(result)):
                list_users.append(result[i][0])
            return list_users

    def get_users_gender_love(self, gender):
        with self.conn:
            list_users = []
            result = self.cur.execute('SELECT `user_id` FROM `love` WHERE `gender` = ?', (gender,)).fetchall()
            for i in range(len(result)):
                list_users.append(result[i][0])
            return list_users

    def get_users_prof_love(self):
        with self.conn:
            list_users = []
            result = self.cur.execute('SELECT `user_id` FROM `love` WHERE `profile` = 1').fetchall()
            for i in range(len(result)):
                list_users.append(result[i][0])
            return list_users

    def get_users_not_active_love(self):
        with self.conn:
            list_users = []
            result = self.cur.execute('SELECT `user_id` FROM `forms` WHERE `active` = 0').fetchall()
            for i in range(len(result)):
                list_users.append(result[i][0])
            return list_users

    def get_users_active_now_love(self):
        with self.conn:
            list_users = []
            result = self.cur.execute('SELECT `user_id` FROM `love` WHERE `active_now` = 1').fetchall()
            for i in range(len(result)):
                list_users.append(result[i][0])
            return list_users

    def set_url(self, url, campus):
        with self.conn:
            return self.cur.execute('UPDATE `dates` SET `url` = ? WHERE `id` = ?', (url, campus))

    def get_url(self, campus):
        with self.conn:
            return self.cur.execute('SELECT `url` FROM `dates` WHERE `id` = ?', (campus,)).fetchone()[0]

    def add_teach(self, camp, date, chang, insert_date):
        with self.conn:
            return self.cur.execute('INSERT INTO `teach` (`campus`, `date`, `chang`, `insert_date`) VALUES (?,?,?,?)',
                                    (camp, date, chang, insert_date,))

    def get_chang_teach(self, camp, date):
        with self.conn:
            list_chang = []
            result = self.cur.execute('SELECT `chang` FROM `teach` WHERE `campus` = ? and `date` = ?',
                                      (camp, date,)).fetchall()
            for i in range(len(result)):
                list_chang.append(result[i][0])
            return list_chang

    def count_users_group(self, group):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id`) FROM `users` WHERE `current_group` = ?', (group,)).fetchone()[0]

    def count_users_notice(self, value):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id`) FROM `users` WHERE `notice_morning` = ?', (value,)).fetchone()[
                0]

    def count_users_chang(self, value):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id`) FROM `users` WHERE `notice_changes` = ?', (value,)).fetchone()[
                0]

    def delete_users(self, user_id):
        with self.conn:
            return self.cur.execute('DELETE FROM `users` WHERE `user_id` = ?', (user_id,))

    def delete_users_love(self, user_id):
        with self.conn:
            return self.cur.execute('DELETE FROM `love` WHERE `user_id` = ?', (user_id,))

    def delete_view_form(self, user_id):
        with self.conn:
            return self.cur.execute('DELETE FROM `view_form` WHERE `user_id` = ?', (user_id,))

    def get_all_teach(self, date, group, day, up_week):
        with self.conn:
            lists = []
            result = self.cur.execute(
                'SELECT `teacher` FROM `rasp` WHERE `day` = ? and `group` = ? and (`up_week` = ? or `up_week` = 0)',
                (day, group, up_week,)).fetchall()
            result1 = self.cur.execute('SELECT `absent2` FROM `changes` WHERE `date` = ? and `group` = ?',
                                       (date, group,)).fetchall()

            for i in result:
                lists.append(i[0])
            for i in result1:
                lists.append(i[0])
            return set(lists)

    def check_changes(self, date, campus):
        with self.conn:
            result = self.cur.execute('SELECT `id` FROM `changes` WHERE `date` = ? and `campus` = ?',
                                      (date, campus,)).fetchall()
            return bool(len(result))

    def get_username(self, group):
        with self.conn:
            lists_usernames = []
            result = self.cur.execute('SELECT `username` FROM `users` WHERE `current_group` = ?', (group,)).fetchall()
            for i in result:
                if i[0] is None or i[0] == '':
                    lists_usernames.append('Без username')
                else:
                    lists_usernames.append(i[0])
            return lists_usernames

    def find_users(self, username=None, user_id=None):
        with self.conn:
            return_list = []
            if username is not None:
                result = self.cur.execute(
                    'SELECT `user_id`, `current_group`, `notice_morning`, `notice_morning_time`, `notice_changes` FROM `users` WHERE `username` = ?',
                    (username,)).fetchall()
                for i in result:
                    for i1 in i:
                        return_list.append(i1)
            elif user_id is not None:
                result = self.cur.execute(
                    'SELECT `username`, `current_group`, `notice_morning`, `notice_morning_time`, `notice_changes` FROM `users` WHERE `user_id` = ?',
                    (user_id,)).fetchall()
                for i in result:
                    for i1 in i:
                        return_list.append(i1)

            return return_list

    def get_not_chang(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `not_chang` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_not_chang(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `users` SET `not_chang` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_accept(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `accept` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_accept(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `accept` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_prof(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `profile` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_prof(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `profile` = ? WHERE `user_id` = ?', (value, user_id,))

    def set_name(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `name` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_name(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `name` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_gender(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `gender` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_gender(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `gender` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_course(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `course` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_course(self, user_id):
        with self.conn:
            try:
                return self.cur.execute('SELECT `course` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]
            except TypeError:
                return False

    def set_year(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `year` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_year(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `year` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_interes(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `interes` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_interes(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `interes` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_about(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `about` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_about(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `about` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_media1(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `media1` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_media1(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `media1` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_media2(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `media2` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_media2(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `media2` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_media3(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `media3` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_media3(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `media3` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_type1(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `type1` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_type1(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `type1` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_type2(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `type2` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_type2(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `type2` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_type3(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `type3` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_type3(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `type3` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def set_text(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `text` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_text(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `text` FROM `love` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def get_form(self, user_id, interes, campus):
        with self.conn:
            list_forms = []
            list_view = []
            if interes != 3:
                result = self.cur.execute('SELECT `id_form` FROM `forms` WHERE `active` = 1 and `gender` = ?',
                                          (interes,)).fetchall()
            else:
                result = self.cur.execute('SELECT `id_form` FROM `forms` WHERE `active` = 1').fetchall()

            for i in range(len(result)):
                list_forms.append(result[i][0])

            result_view = self.cur.execute('SELECT `id_form` FROM `view_form` WHERE `user_id` = ?',
                                           (user_id,)).fetchall()
            for i in range(len(result_view)):
                list_view.append(result_view[i][0])

            my_id = self.cur.execute('SELECT `id_form` FROM `forms` WHERE `user_id` = ?', (user_id,)).fetchone()[0]
            try:
                list_forms.remove(my_id)
            except ValueError:
                pass
            for i in list_view:
                if i in list_forms:
                    list_forms.remove(i)
            my_campus = []

            for i in list_forms:
                user_id_user = \
                self.cur.execute('SELECT `user_id` FROM `forms` WHERE `id_form` = ?', (int(i),)).fetchone()[0]
                if self.get_course(user_id_user) == campus:
                    my_campus.append(i)

            if not my_campus == []:
                return_list = []
                id_form = my_campus[0]
                full_data = self.cur.execute(
                    'SELECT `id_form`, `user_id`, `text_form`, `len_media` FROM `forms` WHERE `id_form` = ?',
                    (id_form,)).fetchall()
                for i in range(len(full_data[0])):
                    return_list.append(full_data[0][i])
                return return_list

            elif not list_forms == []:
                return_list = []
                id_form = list_forms[0]
                full_data = self.cur.execute(
                    'SELECT `id_form`, `user_id`, `text_form`, `len_media` FROM `forms` WHERE `id_form` = ?',
                    (id_form,)).fetchall()
                for i in range(len(full_data[0])):
                    return_list.append(full_data[0][i])
                return return_list
            else:
                return False

    def add_forms(self, user_id, text_form, len_media, gender):
        with self.conn:
            return self.cur.execute(
                'INSERT INTO `forms` (`user_id`, `text_form`, `len_media`, `gender`) VALUES (?,?,?,?)',
                (user_id, text_form, len_media, gender,))

    def form_exists(self, user_id):
        with self.conn:
            result = self.cur.execute('SELECT * FROM `forms` WHERE user_id = ?',
                                      (user_id,)).fetchall()
            return bool(len(result))

    def update_forms(self, text_form, len_media, gender, user_id):
        with self.conn:
            return self.cur.execute(
                'UPDATE `forms` SET `text_form` = ?, `len_media` = ?, `gender` = ? WHERE `user_id` = ?',
                (text_form, len_media, gender, user_id,))

    def get_len_media(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `len_media` FROM `forms` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()[0]

    def get_id_form(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `id_form` FROM `forms` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()[0]

    def set_view_form(self, id_form, user_id_form, user_id, value):
        with self.conn:
            return self.cur.execute(
                'INSERT INTO `view_form` (`id_form`, `user_id_form`, `user_id`, `value`) VALUES (?,?,?,?)',
                (id_form, user_id_form, user_id, value,))

    def active_now(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `active_now` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_active_now(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `active_now` FROM `love` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()[0]

    def get_active_form(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `active` FROM `forms` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()[0]

    def set_active_form(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `forms` SET `active` = ? WHERE `user_id` = ?', (value, user_id,))

    def set_off_form(self, value, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `love` SET `off_form` = ? WHERE `user_id` = ?', (value, user_id,))

    def get_count_view_form(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id_form`) FROM `view_form` WHERE `user_id_form` = ?',
                                    (user_id,)).fetchone()[0]

    def get_count_look_form(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id_form`) FROM `view_form` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()[0]

    def get_count_likes(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id_form`) FROM `view_form` WHERE `user_id_form` = ? and `value` = 1',
                                    (user_id,)).fetchone()[0]

    def get_count_my_likes(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id_form`) FROM `view_form` WHERE `user_id` = ? and `value` = 1',
                                    (user_id,)).fetchone()[0]

    def get_count_my_dislikes(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id_form`) FROM `view_form` WHERE `user_id` = ? and `value` = 0',
                                    (user_id,)).fetchone()[0]

    def add_hw(self, user_id, group, day, hw):
        with self.conn:
            return self.cur.execute('INSERT INTO `homework` (`user_id`, `group`, `day`, `hw`) VALUES (?,?,?,?)',
                                    (user_id, group, day, hw,))

    def get_hw(self, group, day):
        with self.conn:
            try:
                return self.cur.execute('SELECT `hw` FROM `homework` WHERE `group` = ? and `day` = ?',
                                        (group, day,)).fetchone()[0]
            except TypeError:
                return False

    def get_hw_use(self, group, day):
        with self.conn:
            try:
                return self.cur.execute('SELECT `hw` FROM `homework` WHERE `group` = ? and `day` = ? and `active` = 1',
                                        (group, day,)).fetchone()[0]
            except TypeError:
                return False

    def update_hw(self, hw, group, day):
        with self.conn:
            return self.cur.execute('UPDATE `homework` SET `hw` = ? WHERE `group` = ? and `day` = ?', (hw, group, day,))

    def active_hw(self, value, group, day):
        with self.conn:
            return self.cur.execute('UPDATE `homework` SET `active` = ? WHERE `group` = ? and `day` = ?',
                                    (value, group, day,))

    def set_active_hw(self, group, day):
        with self.conn:
            try:
                return self.cur.execute('SELECT `active` FROM `homework` WHERE `group` = ? and `day` = ?',
                                        (group, day,)).fetchone()[0]
            except TypeError:
                return False

    def delete_hw(self, group, day):
        with self.conn:
            return self.cur.execute('DELETE FROM `homework` WHERE `group` = ? and `day` = ?', (group, day,))

    def get_group_leader(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `group` FROM `leaders` WHERE `user_id` = ?',
                                    (user_id,)).fetchone()[0]

    def get_teach_list(self):
        with self.conn:
            return_array = {}
            result = self.cur.execute('SELECT `FIO`, `campus`, `id` FROM `rating`').fetchall()
            for i in result:
                return_array[i[0]] = [i[1], i[2]]
            return return_array

    def get_teach_campus(self, teacher_name):
        with self.conn:
            return self.cur.execute('SELECT `campus` FROM `rating` WHERE `FIO` = ?', (teacher_name,)).fetchone()[0]

    def get_teach_fio(self, id_teach):
        with self.conn:
            return self.cur.execute('SELECT `FIO` FROM `rating` WHERE `id` = ?', (id_teach,)).fetchone()[0]

    def set_cur_teach(self, teacher, user_id):
        with self.conn:
            return self.cur.execute('UPDATE `users` SET `current_teacher` = ? WHERE `user_id` = ?', (teacher, user_id,))

    def get_cur_teach(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `current_teacher` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    def update_actions(self, day):
        with self.conn:
            return self.cur.execute('UPDATE `actions` SET `requests` = `requests` + 1 WHERE `day` = ?', (day,))

    def set_reviews(self, user_id, comment):
        with self.conn:
            return self.cur.execute('INSERT INTO `reviews` (`user_id`, `comment`) VALUES (?,?)', (user_id, comment,))

    def get_reviews(self, id_comm):
        with self.conn:
            try:
                return self.cur.execute('SELECT `comment` FROM `reviews` WHERE `id` = ?', (id_comm, )).fetchone()[0]
            except TypeError:
                return False

    def get_reviews_admin(self):
        with self.conn:
            result = []
            res = self.cur.execute('SELECT `user_id`, `comment` FROM `reviews`').fetchall()
            for i in res:
                result.append([i[0], i[-1]])
            return result

    def check_reviews(self, user_id):
        with self.conn:
            res = self.cur.execute('SELECT * FROM `reviews` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(res))

    def delete_reviews(self, user_id):
        with self.conn:
            return self.cur.execute('DELETE FROM `reviews` WHERE `user_id` = ?', (user_id,))

    def get_rating(self, teacher):
        with self.conn:
            res = self.cur.execute('SELECT `rating` FROM `comments` WHERE `teacher` = ?', (teacher,)).fetchall()
            work = []
            for i in res:
                if i[0] != 0:
                    work.append(i[0])
            try:
                return [f"{sum(work) / len(work):.{2}f}", len(work)]
            except ZeroDivisionError:
                return [0.00, len(work)]

    def update_rating(self, rat, fio):
        with self.conn:
            return self.cur.execute('UPDATE `rating` SET `summa` = `summa` + ?, `count` = `count` + 1 WHERE `FIO` = ?', (rat, fio,))

    def get_count_comm(self, id_teacher):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id`) FROM `comments` WHERE `teacher` = ? and `comm` != ""',
                                    (id_teacher,)).fetchone()[0]

    def get_count_reactions(self, id_teacher):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id`) FROM `comments` WHERE `teacher` = ? and `status` != ""',
                                    (id_teacher,)).fetchone()[0]

    def get_count_quotes(self, id_teacher):
        with self.conn:
            return self.cur.execute('SELECT COUNT(`id`) FROM `quotes` WHERE `teacher` = ?',
                                    (id_teacher,)).fetchone()[0]

    def get_status(self, teacher):
        with self.conn:
            love = self.cur.execute('SELECT COUNT(`id`) FROM `comments` WHERE `teacher` = ? and `status` = "🥰"', (teacher,)).fetchone()[0]
            ha = self.cur.execute('SELECT COUNT(`id`) FROM `comments` WHERE `teacher` = ? and `status` = "😂"', (teacher,)).fetchone()[0]
            clown = self.cur.execute('SELECT COUNT(`id`) FROM `comments` WHERE `teacher` = ? and `status` = "🤡"', (teacher,)).fetchone()[0]
            bad = self.cur.execute('SELECT COUNT(`id`) FROM `comments` WHERE `teacher` = ? and `status` = "🤬"', (teacher,)).fetchone()[0]
            array = {
                '🥰': love,
                '😂': ha,
                '🤡': clown,
                '🤬': bad
            }
            return [max(array, key=array.get), array]

    def get_user_star(self, user_id, teacher):
        with self.conn:
            res = self.cur.execute('SELECT `rating` FROM `comments` WHERE `user_id` = ? and `teacher` = ?', (user_id, teacher,)).fetchall()
            if res:
                return res[0][0]
            else:
                return 0

    def get_user_reaction(self, user_id, teacher):
        with self.conn:
            res = self.cur.execute('SELECT `status` FROM `comments` WHERE `user_id` = ? and `teacher` = ?', (user_id, teacher,)).fetchall()
            if res:
                return res[0][0]
            else:
                return 0

    def check_exists_like(self, id_comm: int, user_id: int):
        with self.conn:
            return self.cur.execute('SELECT `like` FROM `likes` WHERE `id_comm` = ? and `user_id` = ?', (id_comm, user_id,)).fetchall()

    def create_likes(self, user_id: int, id_comm: int):
        with self.conn:
            exists = self.cur.execute('SELECT * FROM `likes` WHERE `user_id` = ? and `id_comm` = ?', (user_id, id_comm,)).fetchall()
            if not bool(len(exists)):
                return self.cur.execute('INSERT INTO `likes` (`user_id`, `id_comm`) VALUES (?,?)', (user_id, id_comm,))
            else:
                return True

    def set_like_comm(self, user_id: int, id_comm: int, like: int | None = None):
        with self.conn:
            self.create_likes(user_id, id_comm)
            if like is not None:
                self.cur.execute('UPDATE `likes` SET `like` = ? WHERE `user_id` = ? and `id_comm` = ?', (like, user_id, id_comm,))

    def create_comm(self, user_id: int, teacher_id: int):
        with self.conn:
            exists = self.cur.execute('SELECT * FROM `comments` WHERE `user_id` = ? and `teacher` = ?', (user_id, teacher_id,)).fetchall()
            if not bool(len(exists)):
                return self.cur.execute('INSERT INTO `comments` (`user_id`, `teacher`) VALUES (?,?)', (user_id, teacher_id,))
            else:
                return True

    def set_comm_rating(self, user_id: int, teacher_id: int, rating: int | None = None, status: str | None = None, comm: str | None = None):
        with self.conn:
            self.create_comm(user_id, teacher_id)
            if rating is not None:
                self.cur.execute('UPDATE `comments` SET `rating` = ? WHERE `user_id` = ? and `teacher` = ?', (rating, user_id, teacher_id,))
            if status is not None:
                self.cur.execute('UPDATE `comments` SET `status` = ? WHERE `user_id` = ? and `teacher` = ?', (status, user_id, teacher_id,))
            if comm is not None:
                self.cur.execute('UPDATE `comments` SET `comm` = ? WHERE `user_id` = ? and `teacher` = ?', (comm, user_id, teacher_id,))

    def check_exists_comm(self, user_id, teacher_id):
        with self.conn:
            res = self.cur.execute('SELECT * FROM `comments` WHERE `user_id` = ? and `teacher` = ? and `comm` != ""', (user_id, teacher_id,)).fetchall()
            return bool(len(res))

    def get_my_comm(self, user_id, teacher_id):
        with self.conn:
            return self.cur.execute('SELECT `comm`, `id` FROM `comments` WHERE `user_id` = ? and `teacher` = ?', (user_id, teacher_id,)).fetchone()

    def check_exists_comm_teacher(self, teacher_id: int):
        with self.conn:
            return self.cur.execute('SELECT COUNT(*) FROM `comments` WHERE `teacher` = ? and `comm` != ""', (teacher_id,)).fetchone()[0]

    def get_comments_teacher(self, teacher_id: int, id_comm: int):
        with self.conn:
            return self.cur.execute('SELECT `comm`, `id` FROM `comments` WHERE `teacher` = ? and `comm` != ""', (teacher_id,)).fetchall()[id_comm - 1]

    def get_likes_comm(self, id_comm):
        with self.conn:
            res = self.cur.execute('SELECT `like` FROM `likes` WHERE `id_comm` = ?', (id_comm,)).fetchall()
            result = []
            for i in res:
                result.append(i[0])
            return [result.count(1), result.count(0)]

    def get_id_comm(self, user_id):
        with self.conn:
            return self.cur.execute('SELECT `id` FROM `comments` WHERE `user_id` = ?', (user_id,)).fetchall()

    def add_teacher(self, name):
        with self.conn:
            return self.cur.execute('UPDATE `rating` SET `FIO` = ? WHERE `id` = 79', (name,))

    def check_disk(self, user_id: int, accept: bool):
        with self.conn:
            if not accept:
                return self.cur.execute('SELECT `send_mes` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[0]
            else:
                return self.cur.execute('UPDATE `users` SET `send_mes` = 1 WHERE `user_id` = ?', (user_id,))

    # --------------------------------------- PREMIUM ------------------------- PREMIUM ------------------------ PREMIUM ----------------------------
    def user_exists_premium(self, user_id):
        with self.conn:
            return bool(self.cur.execute('SELECT COUNT(*) FROM premium WHERE user_id = ?',
                                         (user_id,)).fetchone()[0])

    def new_premium_user(self, user_id: int, balance: int):
        with self.conn:
            return self.cur.execute("INSERT INTO premium (user_id, balance) VALUES (?,?)", (user_id, balance))

    def update_balance(self, user_id: int, balance: int):
        with self.conn:
            return self.cur.execute("UPDATE premium SET balance = ? WHERE user_id = ?", (balance, user_id))

    def new_sub_premium(self, user_id: int, price: int, date_start: str, date_end: str):
        with self.conn:
            self.cur.execute("UPDATE premium SET balance = balance - ?, date_start = ?, date_end = ?, active = 1 WHERE user_id = ?", (price, date_start, date_end, user_id))
            self.cur.execute("INSERT INTO sub (user_id, date_start, date_end) VALUES (?,?,?)", (user_id, date_start, date_end))
            return True

    def count_referrers(self, user_id: int):
        with self.conn:
            return self.cur.execute("SELECT COUNT(id) FROM users WHERE referrer_id = ?", (user_id,)).fetchone()[0]

    def get_my_ref(self, user_id: int):
        with self.conn:
            return self.cur.execute("SELECT referrer_id, get_bonus FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def update_get_bonus(self, user_id: int):
        with self.conn:
            return self.cur.execute("UPDATE users SET get_bonus = 1 WHERE user_id = ?", (user_id,))

    def get_my_referrers(self, user_id: int):
        with self.conn:
            return [i[0] for i in self.cur.execute("SELECT user_id FROM users WHERE referrer_id = ?", (user_id,)).fetchall()]

    def update_bonus(self, user_id: int):
        with self.conn:
            return self.cur.execute("UPDATE premium SET bonus = bonus + 1, free_bonus = free_bonus + 1 WHERE user_id = ?", (user_id,))

    def update_bonus_minus(self, user_id: int):
        with self.conn:
            return self.cur.execute("UPDATE premium SET free_bonus = free_bonus - 1 WHERE user_id = ?", (user_id,))

    def get_bonus(self, user_id: int):
        with self.conn:
            return self.cur.execute("SELECT bonus FROM premium WHERE user_id = ?", (user_id,)).fetchone()[0]

    def get_free_bonus(self, user_id: int):
        with self.conn:
            if self.user_exists_premium(user_id=user_id):
                return self.cur.execute("SELECT free_bonus FROM premium WHERE user_id = ?", (user_id,)).fetchone()[0]
            else:
                return 0

    def get_usernames_ref(self, user_id: int):
        with self.conn:
            return [i[0] for i in self.cur.execute("SELECT username FROM users WHERE referrer_id = ?", (user_id,)).fetchall()]

    def get_balance(self, user_id: int):
        with self.conn:
            if self.user_exists_premium(user_id=user_id):
                return self.cur.execute("SELECT balance FROM premium WHERE user_id = ?",
                                        (user_id,)).fetchone()[0]
            else:
                return 0

    def get_active_prem(self, user_id: int):
        with self.conn:
            if self.user_exists_premium(user_id=user_id):
                return self.cur.execute("SELECT active FROM premium WHERE user_id = ?",
                                        (user_id,)).fetchone()[0]
            else:
                return "Неактивна"

    def set_active_prem(self, user_id: int, active: int):
        with self.conn:
            return self.cur.execute("UPDATE premium SET active = ? WHERE user_id = ?", (active, user_id))

    def get_end_date(self, user_id: int):
        with self.conn:
            if self.user_exists_premium(user_id=user_id):
                return self.cur.execute("SELECT date_end FROM premium WHERE user_id = ?",
                                        (user_id,)).fetchone()[0]
            else:
                return None

    def get_teachers_fio(self):
        with self.conn:
            return [i[0] for i in self.cur.execute("SELECT FIO FROM rating").fetchall()]

    def teacher_set(self, fio, id_t):
        with self.conn:
            return self.cur.execute("UPDATE rating SET rating = ? WHERE id = ?", (fio, id_t))

    def insert_main_rasp(self, group: str, day: int, count_para: int, door: str, name_para: str, teacher: str, up_week: int, subgroup: int):
        with self.conn:
            return self.cur.execute("INSERT INTO `rasp` (`group`, `day`, `count_para`, `door`, `name_para`, `teacher`, `up_week`, `subgroup`) VALUES (?,?,?,?,?,?,?,?)",
                                    (group, day, count_para, door, name_para, teacher, up_week, subgroup))


# db = Database('database.db')



