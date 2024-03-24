import socket
import subprocess
from datetime import datetime, timezone

import requests

from vps_status_common.config import GROUP_FILE_PATH
from vps_status_common.db_helper import DbHelper
from vps_status_common.status import Status


def check_https(url):
    try:
        requests.get(f"https://{url}", verify=True)
        return True
    except (requests.exceptions.SSLError, ConnectionError, Exception) as e:
        return False


def check_dnssec(url):
    cmd = f"dig {url} DNSKEY +short"

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = process.stdout.read().decode("utf-8")

    return out is not None and out.strip() != "" and 'error' not in out


def get_content(url, https=False):
    scheme = "https://" if https else "http://"
    try:
        response = requests.get(scheme + url, verify=False)
        return response.content
    except (requests.exceptions.SSLError, ConnectionError, Exception) as e:
        return ""


def get_ip(url):
    ip = ""
    try:
        ip = socket.gethostbyname(url)
    except Exception:
        pass
    return ip


def now_formated():
    return datetime.now().strftime("%H:%M %d/%m/%Y")


def main():
    db_helper = DbHelper()

    groups = []
    with open(GROUP_FILE_PATH, "r") as f:
        groups = [line.strip() for line in f]

    date_time_batch = now_formated()
    for group_name in groups:
        url_www = f"www.{group_name}.ephec-ti.be"
        url_blog = f"blog.{group_name}.ephec-ti.be"
        ip_web = get_ip(f"www.{group_name}.ephec-ti.be")
        content_www_ssl = get_content(url_www, True)
        content_www_http = get_content(url_www, False)
        content_blog_http = get_content(url_blog)
        www_https_valid = check_https(url_www)
        dnssec = check_dnssec(f"{group_name}.ephec-ti.be")
        date_time = now_formated()
        ip_ns = get_ip(f"ns.{group_name}.ephec-ti.be")
        status = Status(group_name=group_name,
                        date_time_batch=date_time_batch,
                        ip_web=ip_web,
                        url_www=url_www,
                        www_https_valid=www_https_valid,
                        content_www_ssl=content_www_ssl,
                        content_www_http=content_www_http,
                        content_blog_http=content_blog_http,
                        dnssec=dnssec,
                        ip_ns=ip_ns,
                        date_time=date_time)
        db_helper.save_status(status)
    db_helper.con.commit()


if __name__ == "__main__":
    main()
