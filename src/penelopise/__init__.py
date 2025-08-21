"""penelopise - Basic parsing for ``todo.txt`` files."""

import datetime
import enum
import functools
import re
import string
import typing


# Regular expression pattern for matching a string that *may* be an ISO-8601
# date.  This clearly doesn't validate a string, but gets us close enough to
# descend in to date parsing mode.
_ISO_DATE = r"\d{4}-\d{2}-\d{2}"


class Priority(enum.IntEnum):  # ruff: disable=E741
    """Enumeration for representing task priority levels.

    The ``todo.txt`` specification declares priorities to be any uppercase ASCII
    character.  Much of the tooling around the format, however, special cases the
    characters ``A``, ``B``, and ``C`` in to a sort of high, medium, and low
    arrangement respectively.
    """

    # This *awful* block exists because if we use the dynamic interface for
    # IntEnum setup then we can't use the typechecker to guarantee our usage at
    # call sites.
    #
    # The one good thing about this method is that it reminds us how useful
    # vim's "g C-x" can be when combined with nrformats=alpha.
    Z = enum.auto()  # NoQA: E741
    Y = enum.auto()  # NoQA: E741
    X = enum.auto()  # NoQA: E741
    W = enum.auto()  # NoQA: E741
    V = enum.auto()  # NoQA: E741
    U = enum.auto()  # NoQA: E741
    T = enum.auto()  # NoQA: E741
    S = enum.auto()  # NoQA: E741
    R = enum.auto()  # NoQA: E741
    Q = enum.auto()  # NoQA: E741
    P = enum.auto()  # NoQA: E741
    O = enum.auto()  # NoQA: E741
    N = enum.auto()  # NoQA: E741
    M = enum.auto()  # NoQA: E741
    L = enum.auto()  # NoQA: E741
    K = enum.auto()  # NoQA: E741
    J = enum.auto()  # NoQA: E741
    I = enum.auto()  # NoQA: E741
    H = enum.auto()  # NoQA: E741
    G = enum.auto()  # NoQA: E741
    F = enum.auto()  # NoQA: E741
    E = enum.auto()  # NoQA: E741
    D = enum.auto()  # NoQA: E741
    C = enum.auto()  # NoQA: E741
    B = enum.auto()  # NoQA: E741
    A = enum.auto()  # NoQA: E741


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


@functools.total_ordering
class Entry:
    """Represent a task.

    Encapsulates the complete details of a task; full text description,
    completion status, priority, creation and completion dates, contexts, and
    projects.
    """

    def __init__(self, text: str, /) -> None:
        self._text: str = text

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.text!r})"

    def __setattr__(self, name, value, /):
        if isinstance(
            getattr(type(self), name, None), functools.cached_property
        ):
            raise AttributeError(f"Cannot set attribute '{name}'.")
        super().__setattr__(name, value)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str, /) -> None:
        if value != self._text:
            self._text = value
            for attr in (
                "complete",
                "completion_date",
                "creation_date",
                "priority",
                "contexts",
                "projects",
                "attrs",
            ):
                self.__dict__.pop(attr, None)

    @functools.cached_property
    def complete(self) -> bool:
        return self.text.startswith("x ")

    @functools.cached_property
    def completion_date(self) -> datetime.date | None:
        if m := re.match(
            rf"x (?:\([A-Z]\) )?(?:({_ISO_DATE})(?: {_ISO_DATE})?)", self.text
        ):
            return datetime.date.fromisoformat(m.group(1))
        return None

    @functools.cached_property
    def creation_date(self) -> datetime.date | None:
        if m := re.match(
            rf"(?:x {_ISO_DATE} |\([A-Z]\) )?({_ISO_DATE}) ", self.text
        ):
            return datetime.date.fromisoformat(m.group(1))
        else:
            return None

    @functools.cached_property
    def priority(self) -> Priority | None:
        if m := re.match(r"(?:x )?\(([A-Z])\) ", self.text, re.ASCII):
            return Priority[m.group(1)]
        elif m := re.search(r"\bpri:([^\s:]+)", self.text):
            if m.group(1) not in string.ascii_uppercase:
                raise ValueError(f"Invalid priority value {m.group(1)}")
            return Priority[m.group(1)]
        else:
            return None

    @functools.cached_property
    def contexts(self) -> list[Context]:
        return [Context(v) for v in re.findall(r"\B@(\S+)\b", self.text)]

    @functools.cached_property
    def projects(self) -> list[Project]:
        return [Project(v) for v in re.findall(r"\B\+(\S+)\b", self.text)]

    @functools.cached_property
    def attrs(self) -> dict[str, str | datetime.date]:
        d: dict[str, str | datetime.date] = {}
        for k, v in re.findall(r"([^\s:]+):([^\s:]+)", self.text):
            if k == "pri":
                if v not in string.ascii_uppercase:
                    raise ValueError(f"Invalid priority value {v}")
                continue
            if k in d:
                raise KeyError(f"Duplicate key {k}")
            try:
                v = datetime.date.fromisoformat(v)
            except ValueError:
                pass
            d[k] = v
        return d

    def __eq__(self, other, /):
        if not hasattr(other, "text"):
            return NotImplemented
        return self.text == other.text

    def __lt__(self, other, /):
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
