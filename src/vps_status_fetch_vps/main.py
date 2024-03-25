from datetime import datetime
import nmap

from vps_status_common.db_helper import DbHelper
from vps_status_common.vps import VPS


def main():
    db_helper = DbHelper("vps")

    all_vps = []
    with open("vps.txt", "r") as f:
        all_vps = [line.strip() for line in f]

    nmScan = nmap.PortScanner()
    date_time_batch = datetime.now()
    for vps in all_vps:
        ip = vps.split()[0]
        student = vps.split()[1]
        nmap_result = nmScan.scan(ip, '1-65535')
        scan = nmap_result['scan'][ip]['tcp']
        vps = VPS(ip=ip, student=student, date_time_batch=date_time_batch, scan=scan)
        db_helper.save_vps(vps)
    db_helper.con.commit()


if __name__ == "__main__":
    main()
