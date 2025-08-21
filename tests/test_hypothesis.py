import datetime
import string
import typing

import attrs
from hypothesis import given
from hypothesis import strategies as st

import penelopise


@attrs.define
class TodoData:
    contexts: list[str]
    projects: list[str]
    attrs: dict[str, str | datetime.date]
    priority: str | None
    complete: bool
    completion_date: datetime.date | None
    creation_date: datetime.date | None


# According to the spec, a project or context contains any non-whitespace
# character.  This is a bit broad for a generation strategy, so we'll limit it
# to something more reasonable.
safe_tags = st.text(
    alphabet=st.characters(
        categories=["L", "N"],
    ),
    min_size=1,
)

# Filler text is largely unrestricted; but not the shape of a context, project,
# or attribute pair
safe_text = st.text(
    alphabet=st.characters(
        exclude_characters=":",
    ).filter(lambda s: not s.startswith(("+", "@"))),
)


@st.composite
def todo_data(draw) -> TodoData:
    is_complete = draw(st.booleans())
    has_priority = draw(st.booleans())
    has_creation_date = draw(st.booleans())

    priority = (
        draw(st.sampled_from(string.ascii_uppercase))
        if has_priority and not is_complete
        else None
    )
    # These dates are excessively large, but the spec only specifies YYYY-MM-DD
    # so we should test acceptable values
    creation_date = draw(st.dates(min_value=datetime.date(1000, 1, 1)))
    completion_date = draw(st.dates(min_value=datetime.date(1000, 1, 1)))

    projects = draw(st.sets(safe_tags))
    contexts = draw(st.sets(safe_tags))
    attrs = draw(st.dictionaries(safe_tags, safe_tags))
    if "pri" in attrs:
        if priority:
            del attrs["pri"]
        else:
            # We'll overwrite this one keyword to match expected values
            attrs["pri"] = draw(st.sampled_from(string.ascii_uppercase))

    if is_complete:
        priority = None
        if not has_creation_date:
            creation_date = None
    else:
        if not has_priority:
            priority = None
        completion_date = None
        if has_creation_date:
            creation_date = None

    return TodoData(
        contexts=contexts,
        projects=projects,
        attrs=attrs,
        priority=priority,
        complete=is_complete,
        completion_date=completion_date,
        creation_date=creation_date,
    )


@st.composite
def todo_testable(draw) -> tuple[str, TodoData]:
    data = draw(todo_data())

    completion_marker = "x " if data.complete else ""
    words = draw(st.lists(safe_text))

    description_parts = (
        words
        + [f"+{s}" for s in data.projects]
        + [f"@{s}" for s in data.contexts]
        + [f"{k}:{v}" for k, v in data.attrs.items()]
    )
    draw(st.randoms()).shuffle(description_parts)
    description = " ".join(description_parts)

    entry = ""
    if data.complete:
        entry += completion_marker
        entry += data.completion_date.strftime("%F ")
        if data.creation_date:
            entry += data.creation_date.strftime("%F ")
    else:
        if data.priority:
            entry += f"({data.priority}) "
        if data.creation_date:
            entry += data.creation_date.strftime("%F ")

    entry += description

    return entry, data


@given(todo_testable())
def test_fuzz_parse(testable):
    entry, known = testable
    parsed = penelopise.Entry(entry)
    assert parsed.complete == known.complete
    if known.priority:
        assert (
            typing.cast(penelopise.Priority, parsed.priority).name
            == known.priority
        )
    elif "pri" in known.attrs:
        pri = known.attrs.pop("pri")
        assert typing.cast(penelopise.Priority, parsed.priority).name == pri
    else:
        assert parsed.priority is None
    # Order is unimportant for contexts and projects
    assert set(parsed.contexts) == known.contexts
    assert set(parsed.projects) == known.projects
    assert parsed.attrs == known.attrs
    assert parsed.complete is known.complete
    assert parsed.completion_date == known.completion_date
    assert parsed.creation_date == known.creation_date
