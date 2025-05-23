# Example text extracted from https://github.com/todotxt/todo.txt which, like
# this module, is GPL-3 licensed

import datetime

import pytest

import penelopise

TEST_DATA = [
    "(A) Thank Mom for the meatballs @phone",
    "(B) Schedule Goodwill pickup +GarageSale @phone",
    "Post signs around the neighborhood +GarageSale",
    "@GroceryStore Eskimo pies",
]
"""List of example ``todo.txt`` entries used as test input data extracted from
the documentation_.

.. _documentation: https://github.com/todotxt/todo.txt
"""

TEST_RESULTS = [
    {
        "priority": penelopise.Priority.A,
        "contexts": ["phone"],
    },
    {
        "priority": penelopise.Priority.B,
        "contexts": ["phone"],
        "projects": ["GarageSale"],
    },
    {
        "projects": ["GarageSale"],
    },
    {
        "contexts": ["GroceryStore"],
    },
]
"""List of expected parsed results corresponding to ``TEST_DATA``."""


# Incomplete Tasks {{{
@pytest.mark.parametrize("input_, expected", zip(TEST_DATA, TEST_RESULTS))
def test_basic(input_, expected):
    """Test basic parsing of entries and comparison with expected results."""
    parsed = penelopise.Entry(input_)
    for k, v in expected.items():
        match k:
            case "priority":
                assert parsed.priority == v
            case "contexts" | "projects":
                assert getattr(parsed, k) == v
            case _:
                raise ValueError(f"Unknown property {k}")


@pytest.mark.parametrize("input_, expected", zip(TEST_DATA, TEST_RESULTS))
def test_context_filter(input_, expected):
    """Test filtering entries by context."""
    parsed = penelopise.Entry(input_)
    assert len(parsed.contexts) == len(expected.get("contexts", []))


@pytest.mark.parametrize("input_, expected", zip(TEST_DATA, TEST_RESULTS))
def test_project_filter(input_, expected):
    """Test filtering entries by project."""
    parsed = penelopise.Entry(input_)
    assert len(parsed.projects) == len(expected.get("projects", []))


# Rule 1 {{{2
def test_priority():
    """Test parsing of priority in entries.

    Asserts:
        The parsed priority of the entry is 'A'.
    """
    parsed = penelopise.Entry("(A) Call Mom")
    assert parsed.priority == penelopise.Priority.A


@pytest.mark.parametrize(
    "input_",
    [
        "Really gotta call Mom (A) @phone @someday",
        "(b) Get back to the boss",
        "(B)->Submit TPS report",
    ],
)
def test_no_priority(input_):
    """Test entries without valid priority."""
    assert penelopise.Entry(input_).priority is None


# }}}2


# Rule 2 {{{2
@pytest.mark.parametrize(
    "input_, expected",
    [
        ("2011-03-02 Document +TodoTxt task format", datetime.date(2011, 3, 2)),
        ("(A) 2011-03-02 Call Mom", datetime.date(2011, 3, 2)),
    ],
)
def test_creation_date(input_, expected):
    """Test parsing of creation date in entries."""
    assert penelopise.Entry(input_).creation_date == expected


def test_no_creation_date():
    """Test entries without a creation date."""
    assert penelopise.Entry("(A) Call Mom 2011-03-02").creation_date is None


# }}}2


# Rule 3 {{{2
def test_projects_and_contexts():
    """Test parsing of projects and contexts in entries."""
    parsed = penelopise.Entry(
        "(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone"
    )
    assert penelopise.Project("Family") in parsed.projects
    assert penelopise.Project("PeaceLoveAndHappiness") in parsed.projects
    assert penelopise.Context("iphone") in parsed.contexts
    assert penelopise.Context("phone") in parsed.contexts


def test_no_contexts():
    """Test entries without any contexts."""
    assert (
        penelopise.Entry("Email SoAndSo at soandso@example.com").contexts == []
    )


def test_no_projectss():
    """Test entries without any projects."""
    assert penelopise.Entry("Learn how to add 2+2").projects == []


# }}}2

# }}}


# Complete tasks {{{
# Rule 1 {{{2
def test_complete():
    """Test parsing of completed tasks."""
    assert penelopise.Entry("x 2011-03-03 Call Mom").complete is True


@pytest.mark.parametrize(
    "input_",
    [
        "xylophone lesson",
        "X 2012-01-01 Make resolutions",
        "(A) x Find ticket prices",
    ],
)
def test_not_complete(input_):
    """Test entries that are not marked as complete."""
    assert penelopise.Entry(input_).complete is False


# }}}2


# Rule 2 {{{2
def test_completion_date():
    """Test parsing of completion date in completed tasks."""
    parsed = penelopise.Entry(
        "x 2011-03-02 2011-03-01 Review Tim's pull request +TodoTxtTouch @github"
    )
    assert parsed.complete is True
    assert parsed.completion_date == datetime.date(2011, 3, 2)


# }}}2
# }}}
