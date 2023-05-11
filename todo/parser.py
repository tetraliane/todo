import datetime
import re


WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def parse_date(date_str: str) -> datetime.date:
    if re.match(r"^\d{8}$", date_str):
        # 20230530
        return datetime.date.fromisoformat(date_str)
    elif re.match(r"^\d{4}-\d{1,2}-\d{1,2}$", date_str):
        # 2023-05-30 or 2023-5-30
        y, m, d = list(map(int, date_str.split("-")))
        return datetime.date(y, m, d)
    elif re.match(r"^\d{4}/\d{1,2}/\d{1,2}$", date_str):
        # 2023/05/30 or 2023/5/30
        y, m, d = list(map(int, date_str.split("/")))
        return datetime.date(y, m, d)

    elif re.match(r"^\d{3,4}$", date_str):
        # 0530 or 530
        y = datetime.date.today().year
        m = int(date_str[:-2])
        d = int(date_str[-2:])
        return datetime.date(y, m, d)
    elif re.match(r"^\d{1,2}-\d{1,2}", date_str):
        # 05-30 or 5-30
        y = datetime.date.today().year
        m, d = list(map(int, date_str.split("-")))
        return datetime.date(y, m, d)
    elif re.match(r"^\d{1,2}/\d{1,2}", date_str):
        # 05/30 or 5/30
        y = datetime.date.today().year
        m, d = list(map(int, date_str.split("/")))
        return datetime.date(y, m, d)

    elif re.match(r"^\d+ days?$", date_str, flags=re.IGNORECASE):
        # 3 day(s)
        today = datetime.date.today()
        days = int(date_str.split()[0])
        return today + datetime.timedelta(days)
    elif re.match(r"^\d+ weeks?$", date_str, flags=re.IGNORECASE):
        # 3 week(s)
        today = datetime.date.today()
        weeks = int(date_str.split()[0])
        return today + datetime.timedelta(days=weeks * 7)
    elif re.match(r"^\d+ months?$", date_str, flags=re.IGNORECASE):
        # 3 month(s)
        today = datetime.date.today()
        months = int(date_str.split()[0])
        y = today.year + (today.month + months - 1) // 12
        m = (today.month + months - 1) % 12 + 1
        d = today.day
        return datetime.date(y, m, d)

    elif re.match(r"^\d+d$", date_str, flags=re.IGNORECASE):
        # 3d
        today = datetime.date.today()
        days = int(date_str[:-1])
        return today + datetime.timedelta(days)
    elif re.match(r"^\d+w$", date_str, flags=re.IGNORECASE):
        # 3w
        today = datetime.date.today()
        weeks = int(date_str[:-1])
        return today + datetime.timedelta(days=weeks * 7)
    elif re.match(r"^\d+m$", date_str, flags=re.IGNORECASE):
        # 3m
        today = datetime.date.today()
        months = int(date_str[:-1])
        y = today.year + (today.month + months - 1) // 12
        m = (today.month + months - 1) % 12 + 1
        d = today.day
        return datetime.date(y, m, d)

    elif re.match(r"^yesterday$", date_str, flags=re.IGNORECASE):
        # yesterday
        return datetime.date.today() - datetime.timedelta(days=1)
    elif re.match(r"^tomorrow$", date_str, flags=re.IGNORECASE):
        # tomorrow
        return datetime.date.today() + datetime.timedelta(days=1)

    elif date_str.lower() in WEEKDAYS:
        # monday
        today = datetime.date.today()
        i = WEEKDAYS.index(date_str.lower())
        diff = (7 + i - today.weekday()) % 7
        return today + datetime.timedelta(days=diff)

    raise ValueError(f'"{date_str}" is not a valid format for date.')
