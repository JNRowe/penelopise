import pytest

import penelopise


# Complete tasks {{{
def test_complete_without_date():
    """Test parsing of completed tasks without date stamp."""
    assert penelopise.Entry("x shake bugs free").complete is True


# Rule 2 {{{2
@pytest.mark.parametrize(
    "input_",
    [
        "x 2025-04-27 extract priority pri:B",
        "x (B) 2025-04-27 extract priority pri:B",
    ],
)
def test_completed_with_priority(input_):
    """Test parsing of completed tasks that have priority.

    As noted in the documentation *some* clients will move priority to generic
    metadata on completion.
    """
    parsed = penelopise.Entry(input_)
    assert parsed.complete is True
    assert parsed.priority == penelopise.Priority.B


# }}}2
# }}}


@pytest.mark.parametrize(
    "input_",
    [
        "duplicate key:value1 key:value2",
        "duplicate datetime:2025-08-16 datetime:2025-08-17",
    ],
)
def test_duplicate_attr_keys(input_: str):
    """Test parsing of tasks that have duplicate keys.

    The documentation has no consideration for duplicate metadata keys.  In the
    wild, I've never seen a file that relies on the behaviour.
    """
    parsed = penelopise.Entry(input_)
    with pytest.raises(KeyError, match="Duplicate key"):
        _ = parsed.attrs
