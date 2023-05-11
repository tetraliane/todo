from __future__ import annotations
import datetime

from .parser import parse_date
from .utils import date_to_relative


class TodoRule:
    id: int  # 0 means this rule is not registered to Manager
    title: str
    group: str
    due_date: datetime.date | None
    comment: str
    status: str

    def __init__(
        self,
        title: str,
        group: str,
        due_date: str,
        comment: str,
        id: int = 0,
        status: str = "uncompleted",
    ) -> None:
        self.id = id
        self.title = title
        self.group = group
        self.due_date = parse_date(due_date) if due_date != "" else None
        self.comment = comment
        self.status = status

    def into_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "group": self.group,
            "due_date": self.due_date.isoformat() if self.due_date else "",
            "comment": self.comment,
            "status": self.status,
        }

    def fmt_full(self) -> str:
        return self.fmt_editor()

    def fmt_editor(self) -> str:
        out = self.title + "\n"
        if self.group:
            out += "# {}\n".format(self.group)
        if self.due_date:
            out += "? {}\n".format(date_to_relative(self.due_date))
        if self.comment:
            out += "\n"
            out += self.comment + "\n"
        return out.strip()

    def fmt_line(self) -> str:
        return "{:<6}{:<41}{:<12}{:<20}".format(
            self.id,
            self.title,
            date_to_relative(self.due_date) if self.due_date else "",
            self.group,
        )

    def set_status(self, status) -> None:
        if status not in ["completed", "uncompleted", "not-planed"]:
            raise ValueError(f"Unknown status: {status}")
        self.status = status
