import datetime
import enum
import re

from attrs import define


_ISO_DATE = r"\d{4}-\d{2}-\d{2}"

Priority = enum.IntEnum(
    "Priority", "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
)


@define
class Context:
    name: str


@define
class Project:
    name: str


@define
class Entry:
    text: str
    complete: bool = False
    completion_date: datetime.date | None = None
    creation_date: datetime.date | None = None
    priority: Priority | None = None
    contexts: list[Context] = []
    projects: list[Project] = []
    attrs: dict[str, str | datetime.date] = {}


def parse_entry(text: str) -> Entry:
    if text.startswith("x "):
        complete = True
        try:
            completion_date = datetime.date.fromisoformat(text[2:12])
            _ = datetime.date.fromisoformat(text[13:23])
        except ValueError:
            completion_date = None
    else:
        complete = False
        completion_date = None
    if m := re.match(r"(?:x )?\(([A-Z])\) ", text):
        prio = Priority[m.group(1)]
    else:
        prio = None
    try:
        offset = 0
        if complete:
            offset += 2
        if prio:
            offset += 4
        creation_date = datetime.date.fromisoformat(text[offset : offset + 10])
    except ValueError:
        creation_date = None
    cs = []
    ps = []
    for t, v in re.findall(r"\B([@\+])(\S+)\b", text):
        if t == "@":
            cs.append(Context(v))
        elif t == "+":
            ps.append(Project(v))
    kws: dict[str, str | datetime.date] = {}
    for k, v in re.findall(r"([^\s:]+):([^\s:]+)", text):
        if k == "pri":
            prio = Priority[v]
        else:
            try:
                kws[k] = datetime.date.fromisoformat(v)
            except ValueError:
                kws[k] = v
    return Entry(
        text, complete, completion_date, creation_date, prio, cs, ps, kws
    )


def parse_file(file: str) -> list[Entry]:
    with open(file) as fh:
        return [parse_entry(line.rstrip()) for line in fh if line.strip()]
