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
    elif re.match(r"^today$", date_str, flags=re.IGNORECASE):
        # today
        return datetime.date.today()
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


def parse_editor(text: str) -> tuple[str, str, str, str]:
    title = ""
    group = ""
    due_date = ""
    comment = ""

    reading_header = True
    for i, raw_line in enumerate(text.splitlines()):
        line = raw_line.split("//")[0].strip()

        if reading_header:
            if raw_line.strip() == "" and title != "":
                reading_header = False
                continue
            elif title == "":
                title = line
            elif line.startswith("#"):
                group = line[1:].strip()
            elif line.startswith("?"):
                due_date = line[1:].strip()
            else:
                e = SyntaxError(
                    'Expected "#", "?" or an empty line, but got `{}`'.format(raw_line)
                )
                e.filename = "<editor>"
                e.lineno = i + 1
                e.offset = 1
                e.text = raw_line
                e.end_lineno = i + 1
                e.end_offset = len(raw_line)
                raise e
        else:
            comment = comment + "\n" + line

    if title == "":
        e = SyntaxError("Title is not given.")
        e.filename = "<editor>"
        e.lineno = 1
        e.offset = 1
        e.text = text
        e.end_lineno = len(text.splitlines()) if text != "" else 1
        e.end_offset = len(text.splitlines()[-1]) if text != "" else 1
        raise e

    comment = comment.strip()  # removes empty line before and after the comment

    return title, group, due_date, comment
