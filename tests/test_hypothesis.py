import typing

from hypothesis import given

import penelopise
from .strategies import todo_testable


@given(todo_testable())
def test_fuzz_parse(todo_testable):
    text, known = todo_testable
    parsed = penelopise.Entry(text)
    assert parsed.complete == known.complete
    if known.priority:
        assert (
            typing.cast(penelopise.Priority, parsed.priority).name
            == known.priority
        )
    elif "pri" in known.attrs:
        pri = known.attrs.pop("pri")
        assert typing.cast(penelopise.Priority, parsed.priority).name == pri
    else:
        assert parsed.priority is None
    # Order is unimportant for contexts and projects
    assert set(parsed.contexts) == known.contexts
    assert set(parsed.projects) == known.projects
    assert parsed.attrs == known.attrs
    assert parsed.complete is known.complete
    assert parsed.completion_date == known.completion_date
    assert parsed.creation_date == known.creation_date
