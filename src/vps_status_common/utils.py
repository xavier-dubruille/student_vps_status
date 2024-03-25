from datetime import datetime


def now_formated():
    return datetime.now().strftime("%H:%M %d/%m/%Y")