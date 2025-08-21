import datetime
import typing

from hypothesis import given
from hypothesis import strategies as st

import penelopise


# A weak for generating todo.txt entries.  Note: There are definitely cases this
# *could* produce that would break tests, but right now I just want to get the
# scaffolding in place.
entries = st.text()


def wrapped_type(type_) -> typing.Type:
    """Hack to workaround ``NewType`` use in ``isinstance``.

    .. note::

        This shouldn't be required, but ``NewType`` aliases aren't valid for
        ``isinstance`` calls.
    """
    return type_.__supertype__


@given(entries)
def test_text_property(text):
    """Test that the text property is always a string."""
    assert isinstance(penelopise.Entry(text).text, str)


@given(entries)
def test_priority_property(text):
    """Test that the priority property is always a Priority object or None."""
    assert isinstance(
        penelopise.Entry(text).priority, (penelopise.Priority, type(None))
    )


@given(entries)
def test_contexts_property(text):
    """Test that the contexts property is always a list of strings."""
    entry = penelopise.Entry(text)
    assert isinstance(entry.contexts, list)
    assert all(
        isinstance(c, wrapped_type(penelopise.Context)) for c in entry.contexts
    )


@given(entries)
def test_projects_property(text):
    """Test that the projects property is always a list of strings."""
    entry = penelopise.Entry(text)
    assert isinstance(entry.projects, list)
    assert all(
        isinstance(p, wrapped_type(penelopise.Project)) for p in entry.projects
    )


@given(entries)
def test_completion_date_property(text):
    """Test that the completion_date property is always a date or None."""
    assert isinstance(
        penelopise.Entry(text).completion_date, (datetime.date, type(None))
    )
