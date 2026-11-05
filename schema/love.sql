-- Database structure only; no user data.
CREATE TABLE forms (id_form INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, text_form TEXT, len_media INTEGER, gender INTEGER, active INTEGER DEFAULT (0));

CREATE TABLE love (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, accept INTEGER DEFAULT (0), profile INTEGER DEFAULT (0), name TEXT DEFAULT (0), gender INTEGER DEFAULT (0), course TEXT DEFAULT (0), year INTEGER DEFAULT (0), interes INTEGER DEFAULT (0), about TEXT DEFAULT (0), text TEXT DEFAULT (0), media1 TEXT DEFAULT (0), type1 INTEGER DEFAULT (0), media2 TEXT DEFAULT (0), type2 INTEGER DEFAULT (0), media3 TEXT DEFAULT (0), type3 INTEGER DEFAULT (0), active_now INTEGER DEFAULT (0), off_form TEXT DEFAULT (0));

CREATE TABLE view_form (id_form INTEGER, user_id_form INTEGER, user_id INTEGER, value INTEGER);
