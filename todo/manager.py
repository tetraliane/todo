import datetime
from pathlib import Path
import yaml

from .parser import parse_date
from .rule import TodoRule


DATA_PATH = Path.home() / Path(".local/share/todo/data.yaml")


class Manager:
    data: list[TodoRule]
    next_id: int

    def __init__(self) -> None:
        self.data = []
        self.next_id = 1

        if not DATA_PATH.exists():
            return

        with DATA_PATH.open("r") as f:
            raw_data = yaml.load(f, yaml.Loader)
        for d in raw_data:
            rule = TodoRule(**d)
            self.data.append(rule)
            self.next_id = max(self.next_id, d["id"] + 1)

    def instances(self, date: str | None, status: str) -> list[TodoRule]:
        with_date: list[TodoRule] = []
        without_date: list[TodoRule] = []
        for rule in self.data:
            if date and rule.due_date != parse_date(date):
                continue
            if rule.status != status:
                continue

            if rule.due_date:
                with_date.append(rule)
            else:
                without_date.append(rule)

        with_date.sort(key=lambda rule: (rule.due_date,))
        if status != "uncompleted":
            with_date.reverse()

        return without_date + with_date

    def index(self, id: int) -> int:
        for ind, d in enumerate(self.data):
            if d.id == id:
                return ind
        raise KeyError(f"ID not found: {id}")

    def info(self, id: int) -> TodoRule:
        return self.data[self.index(id)]

    def save(self) -> None:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        data_dict: list[dict] = list(map(lambda rule: rule.into_dict(), self.data))
        with DATA_PATH.open("w") as f:
            yaml.dump(data_dict, f)

    def append(self, rule: TodoRule) -> int:
        rule.id = self.next_id
        self.data.append(rule)
        self.next_id += 1
        return rule.id

    def update(self, id: int, rule: TodoRule):
        rule.id = id
        self.data[self.index(id)] = rule

    def mark(self, id: int, status: str):
        self.data[self.index(id)].set_status(status)

    def remove(self, id: int):
        self.data.pop(self.index(id))


def rule_to_dict(item: tuple[int, TodoRule]) -> dict:
    return item[1].into_dict() | {"id": item[0]}
