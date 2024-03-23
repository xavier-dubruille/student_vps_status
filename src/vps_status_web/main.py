import sqlite3
from datetime import datetime

from flask import Flask, render_template
from flask_htpasswd import HtPasswdAuth

from vps_status_common.config import sqlite_db_file, FLASK_HTPASSWD_PATH, FLASK_SECRET, FLASK_PORT, FLASK_DEBUG
from vps_status_common.status import Status

app = Flask(__name__)
app.config['FLASK_HTPASSWD_PATH'] = FLASK_HTPASSWD_PATH
app.config['FLASK_SECRET'] = FLASK_SECRET

htpasswd = HtPasswdAuth(app)


def dataclass_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return Status(**{k: v for k, v in zip(fields, row)})


def get_status():
    con = sqlite3.connect(sqlite_db_file)
    con.row_factory = dataclass_factory
    res = con.execute("SELECT * FROM status").fetchall()
    print(res)
    return res


@app.route('/')
@htpasswd.required
def index(user):
    status = get_status()
    time = '-' if (status is None or len(status) == 0) else status[0].date_time_batch
    return render_template('table.html', title='Gtoups Status', time=time, status=status)


@app.route('/vps/<ip>')
@htpasswd.required
def single_ip(ip, user):
    data = {'ip': ip}
    time = datetime.now()
    return render_template('table_single_vps.html', title='VPS Status', time=time, data=data)


app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
