import sqlite3

from flask import Flask, render_template

from vps_status.status import Status

app = Flask(__name__)


def dataclass_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return Status(**{k: v for k, v in zip(fields, row)})


def get_status():
    con = sqlite3.connect("status.db")
    con.row_factory = dataclass_factory
    res = con.execute("SELECT * FROM status").fetchall()
    print(res)
    return res



@app.route('/')
def index():
    return render_template('table.html', title='VPS Status', status=get_status())


app.run(debug=True)
