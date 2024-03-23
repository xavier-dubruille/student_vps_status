from datetime import datetime

from db_helper import DbHelper
from vps import VPS


def main():
    db_helper = DbHelper()

    all_vps = []
    with open("vps.txt", "r") as f:
        all_vps = [line.strip() for line in f]

    date_time_batch = datetime.now()
    for vps in all_vps:
        ip = vps.split()[0]
        student = vps.split()[1]
        vps = VPS(ip=ip, student=student, date_time_batch=date_time_batch)
        db_helper.save_vps(vps)
    db_helper.con.commit()


if __name__ == "__main__":
    main()
