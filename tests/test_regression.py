import pytest

import penelopise


def test_complete_without_date():
    """Test that completion without associated date works."""
    parsed = penelopise.Entry("x no date")
    assert parsed.completion_date is None


def test_invalid_pri_value():
    """Test that an invalid priority keyword raises an error."""
    parsed = penelopise.Entry("invalid pri:value")
    with pytest.raises(ValueError, match="Invalid priority"):
        assert parsed.priority
