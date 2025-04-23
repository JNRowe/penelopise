"""penelopise - Basic parsing for ``todo.txt`` files."""

import dataclasses
import datetime
import enum
import functools
import re
import typing


Priority = enum.IntEnum(
    "Priority", "Z Y X W V U T S R Q P O N M L K J I H G F E D C B A"
)
Priority.__doc__ = """Enumeration for representing task priority levels.

The ``todo.txt`` specification declares priorities to be any uppercase ASCII
character.  Much of the tooling around the format, however, special cases the
characters ``A``, ``B``, and ``C`` in to a sort of high, medium, and low
arrangement respectively.
"""

Context = typing.NewType("Context", str)
"""Represent a context associated with a task.

Commonly contexts are used to specify locations associated with a task, but they
can simply be thought of as a keyword to make searching across tasks simpler.
"""

Project = typing.NewType("Project", str)
"""Represent a project associated with a task.

Projects are denoted by the ``+`` symbol in task entry text and are used to
group tasks under a common goal or initiative.
"""


@dataclasses.dataclass
@functools.total_ordering
class Entry:
    """Represent a task.

    Encapsulates the complete details of a task; full text description,
    completion status, priority, creation and completion dates, contexts, and
    projects.
    """

    text: str
    complete: bool = dataclasses.field(default=False, init=False)
    completion_date: datetime.date | None = dataclasses.field(
        default=None, init=False
    )
    creation_date: datetime.date | None = dataclasses.field(
        default=None, init=False
    )
    priority: Priority | None = dataclasses.field(default=None, init=False)
    contexts: list[Context] = dataclasses.field(
        default_factory=list, init=False
    )
    projects: list[Project] = dataclasses.field(
        default_factory=list, init=False
    )
    attrs: dict[str, str | datetime.date] = dataclasses.field(
        default_factory=dict, init=False
    )

    def __post_init__(self) -> None:
        """Parse a singular task string."""
        offset = 0
        if self.text.startswith("x "):
            self.complete = True
            offset += 2
        a, b, c, d = self.text[offset : offset + 4]
        if (a, c, d) == ("(", ")", " ") and b.isupper():
            self.priority = Priority[b]
            offset += 4
        if self.complete:
            try:
                self.completion_date = datetime.date.fromisoformat(
                    self.text[offset : offset + 10]
                )
                offset += 11
                _ = datetime.date.fromisoformat(
                    self.text[offset + 11 : offset + 21]
                )
                offset += 11
            except ValueError:
                pass
        try:
            self.creation_date = datetime.date.fromisoformat(
                self.text[offset : offset + 10]
            )
        except ValueError:
            pass
        for t, v in re.findall(r"\B([@\+])(\S+)\b", self.text):
            if t == "@":
                self.contexts.append(Context(v))
            else:
                self.projects.append(Project(v))
        for k, v in re.findall(r"([^\s:]+):([^\s:]+)", self.text):
            if k == "pri":
                self.priority = Priority[v]
            else:
                try:
                    v = datetime.date.fromisoformat(v)
                except ValueError:
                    pass
                self.attrs[k] = v

    def __eq__(self, other):
        if not hasattr(other, "text"):
            return NotImplemented
        return self.text == other.text

    def __lt__(self, other):
        if not hasattr(other, "priority"):
            return NotImplemented
        if self.priority and other.priority:
            return self.priority < other.priority
        elif self.priority is None:
            return True
        else:
            return False


class Entries(list):
    """Represent a task list.

    This is simply a convenience class for holding a collection of ``Entry``
    objects, and a space to tie custom methods for operating on them.
    """

    @classmethod
    def parse_file(cls, file: str) -> typing.Self:
        """Parse a file containing tasks in ``todo.txt`` format.

        Args:
            file: The path to the file containing task entries.

        Returns:
            The list of ``Entry`` objects contained in the given file.
        """
        with open(file) as fh:
            return cls(Entry(line.rstrip()) for line in fh if line.strip())
