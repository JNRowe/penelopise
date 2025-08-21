import pytest
from hypothesis import given
from hypothesis import strategies as st

import penelopise

keyword = st.text(
    alphabet=st.characters(min_codepoint=ord("a"), max_codepoint=ord("z")),
    min_size=1,
)


@pytest.mark.parametrize("attr", ["context", "project"])
@given(st.text(), st.data())
def test_add_attribute(attr, base_entry, data):
    """A metamorphic test for adding an attribute to a ``Entry``."""
    e1 = penelopise.Entry(base_entry)
    e1_attrs = getattr(e1, f"{attr}s")

    new_item = ("@" if attr == "context" else "+") + data.draw(keyword)
    e2 = penelopise.Entry(f"{base_entry} {new_item}")
    e2_attrs = getattr(e2, f"{attr}s")

    assert set(e2_attrs) == set(e1_attrs) | {new_item[1:]}
