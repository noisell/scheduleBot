-- Database structure only; no user data.
CREATE TABLE actions (day INTEGER, requests INTEGER DEFAULT (0));

CREATE TABLE changes (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, insert_date TEXT, campus INTEGER, up_week INTEGER, "group" TEXT NOT NULL, num_par INTEGER, door TEXT, absent1 TEXT, par1 TEXT, absent2 TEXT, par2 TEXT);

CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher INTEGER, user_id INTEGER, comm TEXT DEFAULT "", status TEXT DEFAULT "", rating INTEGER DEFAULT (0));

CREATE TABLE dates (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, "update" TEXT, url TEXT);

CREATE TABLE homework (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, "group" TEXT, day TEXT, hw TEXT, active INTEGER DEFAULT (0));

CREATE TABLE leaders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, "group" TEXT);

CREATE TABLE likes (id INTEGER PRIMARY KEY AUTOINCREMENT, id_comm INTEGER, user_id INTEGER, "like" INTEGER);

CREATE TABLE premium (user_id INTEGER PRIMARY KEY, balance INTEGER, active INTEGER (1) DEFAULT (0), date_start TEXT, date_end TEXT, bonus INTEGER DEFAULT (0), free_bonus INTEGER DEFAULT (0));

CREATE TABLE quotes (id INTEGER PRIMARY KEY AUTOINCREMENT, teacher INTEGER, quote TEXT);

CREATE TABLE rasp ("group" TEXT, day INTEGER, count_para INTEGER, door TEXT, name_para TEXT, teacher TEXT, up_week INTEGER, subgroup INTEGER DEFAULT (0));

CREATE TABLE rating (id INTEGER PRIMARY KEY AUTOINCREMENT, FIO TEXT, campus INTEGER, rating INTEGER, comment TEXT);

CREATE TABLE reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, comment TEXT);

CREATE TABLE sub (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, date_start TEXT, date_end TEXT);

CREATE TABLE teach (id INTEGER PRIMARY KEY AUTOINCREMENT, insert_date TEXT, campus INTEGER, date TEXT, chang TEXT);

CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE NOT NULL, username TEXT, cur_date TEXT DEFAULT пустая, current_group TEXT DEFAULT (0), current_teacher TEXT DEFAULT (0), current_cabinet INTEGER DEFAULT (0), notice_morning INTEGER DEFAULT (1), notice_morning_time TEXT DEFAULT "07:40", notice_changes INTEGER DEFAULT (1), send_mes INTEGER DEFAULT (0), not_chang INTEGER DEFAULT (1), referrer_id INTEGER, get_bonus INTEGER (1));
