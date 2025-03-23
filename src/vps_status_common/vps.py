from dataclasses import dataclass


@dataclass
class VPS:
    student: str
    now: str
    ip: str
    scan: str
    ssh_port: str
    ts: str
    password_disabled: str
    fail2ban : str
