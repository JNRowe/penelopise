# Example text extracted from https://github.com/todotxt/todo.txt which, like
# this module, is GPL-3 licensed

import datetime

import pytest

import todo_txt

TEST_DATA = [
    "(A) Thank Mom for the meatballs @phone",
    "(B) Schedule Goodwill pickup +GarageSale @phone",
    "Post signs around the neighborhood +GarageSale",
    "@GroceryStore Eskimo pies",
]
TEST_RESULTS = [
    todo_txt.Entry(
        text="(A) Thank Mom for the meatballs @phone",
        priority=todo_txt.Priority.A,
        contexts=[todo_txt.Context(name="phone")],
    ),
    todo_txt.Entry(
        text="(B) Schedule Goodwill pickup +GarageSale @phone",
        priority=todo_txt.Priority.B,
        contexts=[todo_txt.Context(name="phone")],
        projects=[todo_txt.Project(name="GarageSale")],
    ),
    todo_txt.Entry(
        text="Post signs around the neighborhood +GarageSale",
        projects=[todo_txt.Project(name="GarageSale")],
    ),
    todo_txt.Entry(
        text="@GroceryStore Eskimo pies",
        contexts=[todo_txt.Context(name="GroceryStore")],
    ),
]

# Incomplete Tasks


@pytest.mark.parametrize("input_, expected", zip(TEST_DATA, TEST_RESULTS))
def test_basic(input_, expected):
    parsed = todo_txt.parse_data(input_)
    assert parsed == expected


def test_context_filter():
    result = [
        e for e in TEST_RESULTS if todo_txt.Context("phone") in e.contexts
    ]
    assert len(result) == 2


def test_project_filter():
    result = [
        e for e in TEST_RESULTS if todo_txt.Project("GarageSale") in e.projects
    ]
    assert len(result) == 2


# Rule 1
def test_priority():
    parsed = todo_txt.parse_data("(A) Call Mom")
    assert parsed.priority == todo_txt.Priority.A


@pytest.mark.parametrize(
    "input_",
    [
        "Really gotta call Mom (A) @phone @someday",
        "(b) Get back to the boss",
        "(B)->Submit TPS report",
    ],
)
def test_no_priority(input_):
    assert todo_txt.parse_data(input_).priority is None


# Rule 2
@pytest.mark.parametrize(
    "input_, expected",
    [
        ("2011-03-02 Document +TodoTxt task format", datetime.date(2011, 3, 2)),
        ("(A) 2011-03-02 Call Mom", datetime.date(2011, 3, 2)),
    ],
)
def test_creation_date(input_, expected):
    assert todo_txt.parse_data(input_).creation_date == expected


def test_no_creation_date():
    assert todo_txt.parse_data("(A) Call Mom 2011-03-02").creation_date is None


# Rule 3
def test_projects_and_contexts():
    parsed = todo_txt.parse_data(
        "(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone"
    )
    assert todo_txt.Project("Family") in parsed.projects
    assert todo_txt.Project("PeaceLoveAndHappiness") in parsed.projects
    assert todo_txt.Context("iphone") in parsed.contexts
    assert todo_txt.Context("phone") in parsed.contexts


def test_no_contexts():
    assert (
        todo_txt.parse_data("Email SoAndSo at soandso@example.com").contexts
        == []
    )


def test_no_projects():
    assert todo_txt.parse_data("Learn how to add 2+2").projects == []


# Complete tasks


# Rule 1
def test_complete():
    assert todo_txt.parse_data("x 2011-03-03 Call Mom").complete is True


@pytest.mark.parametrize(
    "input_",
    [
        "xylophone lesson",
        "X 2012-01-01 Make resolutions",
        "(A) x Find ticket prices",
    ],
)
def test_not_complete(input_):
    parsed = todo_txt.parse_data(input_)
    assert parsed.complete is False
    assert parsed.completion_date is None


# Rule 2
def test_completion_date():
    parsed = todo_txt.parse_data(
        "x 2011-03-02 2011-03-01 Review Tim's pull request +TodoTxtTouch @github"
    )
    assert parsed.complete is True
    assert parsed.completion_date == datetime.date(2011, 3, 2)
