import datetime
import string

from hypothesis import given
from hypothesis import strategies as st

import penelopise


# According to the spec, a project or context contains any non-whitespace
# character.  This is a bit broad for a generation strategy, so we'll limit it
# to something more reasonable.
safe_text = st.text(
    alphabet=st.characters(
        categories=["L", "N"],
        exclude_characters="+@:",
    ),
    min_size=1,
)


@st.composite
def todo_entries(draw):
    is_complete = draw(st.booleans())
    has_priority = draw(st.booleans())
    has_creation_date = draw(st.booleans())

    completion_marker = "x " if is_complete else ""
    priority = (
        draw(st.sampled_from(string.ascii_uppercase))
        if has_priority and not is_complete
        else ""
    )
    creation_date = draw(
        st.dates(
            min_value=datetime.date(1970, 1, 1),
            max_value=datetime.date(2038, 1, 18),
        )
    )
    completion_date = draw(
        st.dates(
            min_value=datetime.date(1970, 1, 1),
            max_value=datetime.date(2038, 1, 18),
        )
    )

    words = draw(st.lists(safe_text))
    projects = draw(st.sets(safe_text))
    contexts = draw(st.sets(safe_text))
    kv_pairs = draw(st.dictionaries(safe_text, safe_text))

    description_parts = (
        words
        + [f"+{s}" for s in projects]
        + [f"@{s}" for s in contexts]
        + [f"{k}:{v}" for k, v in kv_pairs.items()]
    )
    draw(st.randoms()).shuffle(description_parts)
    description = " ".join(description_parts)

    # Construct the final entry
    entry = ""
    known_valid = {
        "contexts": contexts,
        "projects": projects,
        "attrs": kv_pairs,
    }
    if is_complete:
        known_valid["priority"] = None
        known_valid["complete"] = True
        entry += completion_marker
        known_valid["completion_date"] = completion_date
        entry += completion_date.strftime("%F ")
        if has_creation_date:
            known_valid["creation_date"] = creation_date
            entry += creation_date.strftime("%F ")
        else:
            known_valid["creation_date"] = None
    else:
        if has_priority:
            known_valid["priority"] = priority
            entry += f"({priority}) "
        else:
            known_valid["priority"] = None
        known_valid["complete"] = False
        known_valid["completion_date"] = None
        if has_creation_date:
            known_valid["creation_date"] = creation_date
            entry += creation_date.strftime("%F ")
        else:
            known_valid["creation_date"] = None

    entry += description

    return entry, known_valid


@given(todo_entries())
def test_fuzz_parse(data):
    text, known_valid = data
    parsed = penelopise.Entry(text)
    assert parsed.complete == known_valid["complete"]
    if known_valid["priority"]:
        assert parsed.priority.name == known_valid["priority"]
    else:
        assert parsed.priority is None
    # Order is unimportant for contexts and projects
    assert set(parsed.contexts) == known_valid["contexts"]
    assert set(parsed.projects) == known_valid["projects"]
    if "pri" in known_valid["attrs"]:
        pri = known_valid["attrs"].pop("pri")
        assert parsed.priority.name == pri
    assert parsed.attrs == known_valid["attrs"]
    assert parsed.complete is known_valid["complete"]
    assert parsed.completion_date == known_valid["completion_date"]
    assert parsed.creation_date == known_valid["creation_date"]
