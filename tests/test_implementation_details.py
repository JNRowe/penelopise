import pytest

import penelopise


def test_set_cached_property():
    """Test properties are frozen."""
    entry = penelopise.Entry("some task")
    with pytest.raises(AttributeError):
        entry.complete = True


def test_priority_with_pri_tag():
    """Test priority as metadata is not duplicated."""
    entry = penelopise.Entry("some task pri:A")
    assert entry.priority == penelopise.Priority.A
    assert entry.attrs == {}
