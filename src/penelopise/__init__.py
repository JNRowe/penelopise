"""penelopise - Basic parsing for ``todo.txt`` files."""

import datetime
import enum
import re

from attrs import define


# Regular expression pattern for matching a string that *may* be an ISO-8601
# date.  This clearly doesn't validate a string, but gets us close enough to
# descend in to date parsing mode.
_ISO_DATE = r"\d{4}-\d{2}-\d{2}"

Priority = enum.IntEnum(
    "Priority", "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
)
Priority.__doc__ = """Enumeration for representing task priority levels.

The ``todo.txt`` specification declares priorities to be any uppercase ASCII
character.  Much of the tooling around the format, however, special cases the
characters ``A``, ``B``, and ``C`` in to a sort of high, medium, and low
arrangement respectively.
"""


@define
class Context:
    """Represent a context associated with a task.

    Commonly contexts are used to specify locations associated with a task, but
    they can simply be thought of as a keyword to make searching across tasks
    simpler.
    """

    name: str


@define
class Project:
    """Represent a project associated with a task.

    Projects are denoted by the `+` symbol in task entry text and are used to
    group tasks under a common goal or initiative.
    """

    name: str


@define
class Entry:
    """Represent a task.

    Encapsulates the complete details of a task; full text description,
    completion status, priority, creation and completion dates, contexts, and
    projects.
    """

    text: str
    complete: bool = False
    completion_date: datetime.date | None = None
    creation_date: datetime.date | None = None
    priority: Priority | None = None
    contexts: list[Context] = []
    projects: list[Project] = []
    attrs: dict[str, str | datetime.date] = {}


def parse_entry(text: str) -> Entry:
    """Parse a singular task string.

    Args:
        text: The text string representing the task entry.

    Returns:
        An ``Entry`` representing parsed task details.
    """
    if m := re.match(f"x (?:({_ISO_DATE})(?: {_ISO_DATE})?)?", text):
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
    if m := re.match(rf"(?:x {_ISO_DATE} |\([A-Z]\) )?({_ISO_DATE}) ", text):
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
    """Parse a file containing tasks in ``todo.txt`` format.

    Args:
        file: The path to the file containing task entries.

    Returns:
        The list of `Entry` objects contained in the given file.
    """
    with open(file) as fh:
        return [parse_entry(line.rstrip()) for line in fh if line.strip()]
