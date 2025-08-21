import datetime
import typing

from hypothesis import given

import penelopise
from .strategies import todo_testable


def wrapped_type(type_) -> typing.Type:
    """Hack to workaround ``NewType`` use in ``isinstance``.

    .. note::

        This shouldn't be required, but ``NewType`` aliases aren't valid for
        ``isinstance`` calls.
    """
    return type_.__supertype__


@given(todo_testable())
def test_text_property(todo_testable):
    """Test that the text property is always a string."""
    text, _ = todo_testable
    assert isinstance(penelopise.Entry(text).text, str)


@given(todo_testable())
def test_priority_property(todo_testable):
    """Test that the priority property is always a Priority object or None."""
    text, _ = todo_testable
    assert isinstance(
        penelopise.Entry(text).priority, (penelopise.Priority, type(None))
    )


@given(todo_testable())
def test_contexts_property(todo_testable):
    """Test that the contexts property is always a list of strings."""
    text, _ = todo_testable
    entry = penelopise.Entry(text)
    assert isinstance(entry.contexts, list)
    assert all(
        isinstance(c, wrapped_type(penelopise.Context)) for c in entry.contexts
    )


@given(todo_testable())
def test_projects_property(todo_testable):
    """Test that the projects property is always a list of strings."""
    text, _ = todo_testable
    entry = penelopise.Entry(text)
    assert isinstance(entry.projects, list)
    assert all(
        isinstance(p, wrapped_type(penelopise.Project)) for p in entry.projects
    )


@given(todo_testable())
def test_completion_date_property(todo_testable):
    """Test that the completion_date property is always a date or None."""
    text, _ = todo_testable
    assert isinstance(
        penelopise.Entry(text).completion_date, (datetime.date, type(None))
    )
