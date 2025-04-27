import pytest

import penelopise


# Complete tasks {{{
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
