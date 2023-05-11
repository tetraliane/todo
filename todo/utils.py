import datetime


def date_to_relative(date: datetime.date) -> str:
    today = datetime.date.today()
    if date == today:
        return "today"
    elif (date - today).days == 1:
        return "tomorrow"
    elif (date - today).days == -1:
        return "yesterday"
    elif (date - today).days < 7:
        weekdays = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        return weekdays[date.weekday()]
    else:
        return date.isoformat()
