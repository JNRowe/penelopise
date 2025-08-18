import pytest

import penelopise


def test_invalid_pri_value():
    """Test that a context at the start of a line is parsed correctly."""
    parsed = penelopise.Entry("invalid pri:value")
    with pytest.raises(ValueError, match="Invalid priority"):
        assert parsed.priority
