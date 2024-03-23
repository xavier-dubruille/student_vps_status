import sqlite3
from dataclasses import fields, astuple

from vps_status.status import Status


class DbHelper():
    def __init__(self):
        fi = fields(Status)
        self.headers = ','.join(f.name for f in fi)
        self.placeholders = ','.join(['?'] * len(fi))

        self.con = sqlite3.connect("status.db")
        self.cur = self.con.cursor()
        self.cur.execute("DROP TABLE IF EXISTS status")  # todo: update instead of drop ...

        self.cur.execute(f"CREATE TABLE status ( {self.headers})")

    def save_status(self, status: Status):
        query = f"INSERT INTO status VALUES({self.placeholders})"
        self.cur.execute(query, astuple(status))
