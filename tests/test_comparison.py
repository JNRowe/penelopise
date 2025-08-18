import pytest

import penelopise


def test_non_Entry_comparison():
    """Basic comparison should follow Python-style."""
    assert penelopise.Entry("example") != "example"
    with pytest.raises(TypeError):
        _ = penelopise.Entry("example") < "example"


def test_basic_comparison():
    """Objects are equal if text is a match."""
    assert penelopise.Entry("example") == penelopise.Entry("example")
    assert penelopise.Entry("example") != penelopise.Entry("different")


def test_relative_priority():
    """Entries should be ordered by priority."""
    no_pri = penelopise.Entry("floating")
    high_pri = penelopise.Entry("(A) put out fire")
    low_pri = penelopise.Entry("(C) buy more firelighters")
    assert no_pri < low_pri
    assert low_pri < high_pri
    assert high_pri > no_pri
