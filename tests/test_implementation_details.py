import pytest

import penelopise


def test_set_cached_property():
    """Test properties are frozen."""
    entry = penelopise.Entry("some task")
    with pytest.raises(AttributeError):
        entry.complete = True
