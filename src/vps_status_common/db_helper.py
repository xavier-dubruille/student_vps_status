import sqlite3
from dataclasses import fields, astuple

from .vps import VPS
from .config import sqlite_db_file
from .status import Status


class DbHelper:
    def __init__(self):
        fi = fields(Status)
        self.headers = ','.join(f.name for f in fi)
        self.placeholders = ','.join(['?'] * len(fi))

        self.con = sqlite3.connect(sqlite_db_file)
        self.cur = self.con.cursor()

        self.cur.execute(f"CREATE TABLE IF NOT EXISTS status ( id integer primary key autoincrement, {self.headers})")

        status_columns = self.cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('status');").fetchall()

        set_db = set(t[0] for t in status_columns)
        set_code = set(self.headers.split(','))
        for c in set_code.difference(set_db):
            self.cur.execute(f"ALTER TABLE status ADD COLUMN {c} TEXT")

    def save_status(self, status: Status):
        query = f"INSERT INTO status ({self.headers}) VALUES({self.placeholders})"
        self.cur.execute(query, astuple(status))

    def save_vps(self, vps: VPS):
        query = f"INSERT INTO status VALUES({self.placeholders})"
        self.cur.execute(query, astuple(vps))
