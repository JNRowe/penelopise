import pytest
from hypothesis import given
from hypothesis import strategies as st

import penelopise
from .strategies import todo_testable

keyword = st.text(
    alphabet=st.characters(min_codepoint=ord("a"), max_codepoint=ord("z")),
    min_size=1,
)


@pytest.mark.parametrize("attr", ["context", "project"])
@given(todo_testable(), st.data())
def test_add_attribute(attr, todo_testable, data):
    """A metamorphic test for adding an attribute to a ``Entry``."""
    text, known = todo_testable
    known_attrs = getattr(known, f"{attr}s")

    new_item = ("@" if attr == "context" else "+") + data.draw(keyword)
    e = penelopise.Entry(f"{text} {new_item}")
    e_attrs = getattr(e, f"{attr}s")

    assert set(e_attrs) == set(known_attrs) | {new_item[1:]}
