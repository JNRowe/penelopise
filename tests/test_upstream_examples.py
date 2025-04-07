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
TEST_RESULTS = [
    penelopise.Entry(
        text="(A) Thank Mom for the meatballs @phone",
        priority=penelopise.Priority.A,
        contexts=[penelopise.Context(name="phone")],
    ),
    penelopise.Entry(
        text="(B) Schedule Goodwill pickup +GarageSale @phone",
        priority=penelopise.Priority.B,
        contexts=[penelopise.Context(name="phone")],
        projects=[penelopise.Project(name="GarageSale")],
    ),
    penelopise.Entry(
        text="Post signs around the neighborhood +GarageSale",
        projects=[penelopise.Project(name="GarageSale")],
    ),
    penelopise.Entry(
        text="@GroceryStore Eskimo pies",
        contexts=[penelopise.Context(name="GroceryStore")],
    ),
]

# Incomplete Tasks


@pytest.mark.parametrize("input_, expected", zip(TEST_DATA, TEST_RESULTS))
def test_basic(input_, expected):
    parsed = penelopise.parse_entry(input_)
    assert parsed == expected


def test_context_filter():
    result = [
        e for e in TEST_RESULTS if penelopise.Context("phone") in e.contexts
    ]
    assert len(result) == 2


def test_project_filter():
    result = [
        e
        for e in TEST_RESULTS
        if penelopise.Project("GarageSale") in e.projects
    ]
    assert len(result) == 2


# Rule 1
def test_priority():
    parsed = penelopise.parse_entry("(A) Call Mom")
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
    assert penelopise.parse_entry(input_).priority is None


# Rule 2
@pytest.mark.parametrize(
    "input_, expected",
    [
        ("2011-03-02 Document +TodoTxt task format", datetime.date(2011, 3, 2)),
        ("(A) 2011-03-02 Call Mom", datetime.date(2011, 3, 2)),
    ],
)
def test_creation_date(input_, expected):
    assert penelopise.parse_entry(input_).creation_date == expected


def test_no_creation_date():
    assert (
        penelopise.parse_entry("(A) Call Mom 2011-03-02").creation_date is None
    )


# Rule 3
def test_projects_and_contexts():
    parsed = penelopise.parse_entry(
        "(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone"
    )
    assert penelopise.Project("Family") in parsed.projects
    assert penelopise.Project("PeaceLoveAndHappiness") in parsed.projects
    assert penelopise.Context("iphone") in parsed.contexts
    assert penelopise.Context("phone") in parsed.contexts


def test_no_contexts():
    assert (
        penelopise.parse_entry("Email SoAndSo at soandso@example.com").contexts
        == []
    )


def test_no_projects():
    assert penelopise.parse_entry("Learn how to add 2+2").projects == []


# Complete tasks


# Rule 1
def test_complete():
    assert penelopise.parse_entry("x 2011-03-03 Call Mom").complete is True


@pytest.mark.parametrize(
    "input_",
    [
        "xylophone lesson",
        "X 2012-01-01 Make resolutions",
        "(A) x Find ticket prices",
    ],
)
def test_not_complete(input_):
    parsed = penelopise.parse_entry(input_)
    assert parsed.complete is False
    assert parsed.completion_date is None


# Rule 2
def test_completion_date():
    parsed = penelopise.parse_entry(
        "x 2011-03-02 2011-03-01 Review Tim's pull request +TodoTxtTouch @github"
    )
    assert parsed.complete is True
    assert parsed.completion_date == datetime.date(2011, 3, 2)
