import sqlite3
from datetime import datetime

from flask import Flask, render_template
from flask_htpasswd import HtPasswdAuth

from vps_status_common.vps import VPS
from vps_status_common.config import sqlite_db_file, FLASK_HTPASSWD_PATH, FLASK_SECRET, FLASK_PORT, FLASK_DEBUG
from vps_status_common.status import Status

app = Flask(__name__)
app.config['FLASK_HTPASSWD_PATH'] = FLASK_HTPASSWD_PATH
app.config['FLASK_SECRET'] = FLASK_SECRET

htpasswd = HtPasswdAuth(app)


def dataclass_factory(cursor, row):
    fields = [column[0] for column in cursor.description]

    # let's remove the "id" column
    fields = fields[1:]
    row = row[1:]
    return Status(**{k: v for k, v in zip(fields, row)})


def dataclass_factory_vps(cursor, row):
    fields = [column[0] for column in cursor.description]

    # let's remove the "id" column
    fields = fields[1:]
    row = row[1:]
    return VPS(**{k: v for k, v in zip(fields, row)})


def get_status():
    con = sqlite3.connect(sqlite_db_file)

    cur = con.cursor()
    max_id = cur.execute("SELECT MAX(id) FROM status;").fetchone()[0]
    max_date = cur.execute(f"SELECT date_time_batch FROM status WHERE id={max_id}").fetchone()[0]

    con.row_factory = dataclass_factory
    res = con.execute(f"SELECT * FROM status WHERE date_time_batch='{max_date}'").fetchall()
    # print(res)
    return res

def get_all_vps():
    con = sqlite3.connect(sqlite_db_file)

    keys = ["ip", "student"]
    res = con.execute(f"SELECT DISTINCT ip, student FROM vps ").fetchall()
    res_dic = [dict(zip(keys, t)) for t in res]

    return res_dic


def get_vps_data(ip):
    con = sqlite3.connect(sqlite_db_file)

    cur = con.cursor()
    max_id = cur.execute(f"SELECT MAX(id) FROM vps WHERE ip='{ip}'").fetchone()[0]

    con.row_factory = dataclass_factory_vps
    res = con.execute(f"SELECT * FROM vps WHERE id='{max_id}'").fetchall()
    # print(res)
    return res


@app.route('/')
# @htpasswd.required
def index():
    status = get_status()
    time = '-' if (status is None or len(status) == 0) else status[0].date_time_batch
    return render_template('table.html', title='Status', time=time, status=status)

@app.route('/vps')
# @htpasswd.required
def all_vps():
    status = get_all_vps()
    return render_template('liste_vps.html', title='all_vps', status=status)


@app.route('/vps/<ip>')
# @htpasswd.required
def single_ip(ip):
    vps_data: VPS = get_vps_data(ip)[0]
    return render_template('table_single_vps.html', title='VPS Status', time=vps_data.now, data=vps_data)


app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
