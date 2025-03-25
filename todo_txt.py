import datetime
import enum
import re
import string

from attrs import define


Priority = enum.IntEnum("Priority", list(string.ascii_uppercase))


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
    contexts: [Context] = []
    projects: [Project] = []
    attrs: dict[str, str | datetime.date] = {}


def parse_entry(text: str) -> Entry:
    d_str = r"\d{4}-\d{2}-\d{2}"
    if m := re.match(rf"x (?:({d_str})(?: {d_str})?)?", text):
        complete = True
        if m.lastindex:
            completion_date = datetime.date.fromisoformat(m.group(1))
        else:
            completion_date = None
    else:
        complete = False
        completion_date = None
    if m := re.match(r"(?:x )?\(([A-Z])\) ", text):
        prio = Priority[m.group(1)]
    else:
        prio = None
    if m := re.match(rf"(?:x {d_str} |\([A-Z]\) )?({d_str}) ", text):
        creation_date = datetime.date.fromisoformat(m.group(1))
    else:
        creation_date = None
    cs = []
    ps = []
    for t, v in re.findall(r"\B([@\+])(\S+)\b", text):
        if t == "@":
            cs.append(Context(v))
        elif t == "+":
            ps.append(Project(v))
    kws = {}
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


def parse_file(file: str) -> [Entry]:
    with open(file) as fh:
        return [parse_entry(line.rstrip()) for line in fh if line.strip()]
