import datetime
import string

from hypothesis import given
from hypothesis import strategies as st

import penelopise


# According to the spec, a project or context contains any non-whitespace
# character.  This is a bit broad for a generation strategy, so we'll limit it
# to something more reasonable.
safe_text = st.text(
    alphabet=st.characters(min_codepoint=33, max_codepoint=126).filter(
        lambda c: c not in "+@:"
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
    creation_date = (
        draw(
            st.dates(
                min_value=datetime.date(1970, 1, 1),
                max_value=datetime.date(2038, 1, 18),
            )
        ).strftime("%F ")
        if has_creation_date
        else ""
    )
    completion_date = (
        draw(
            st.dates(
                min_value=datetime.date(1970, 1, 1),
                max_value=datetime.date(2038, 1, 18),
            )
        ).strftime("%F ")
        if is_complete
        else ""
    )

    words = draw(st.lists(safe_text))
    projects = draw(st.lists(safe_text.map(lambda s: "+" + s)))
    contexts = draw(st.lists(safe_text.map(lambda s: "@" + s)))
    kv_pairs = draw(st.dictionaries(safe_text, safe_text)).items()

    description_parts = (
        words + projects + contexts + [f"{k}:{v}" for k, v in kv_pairs]
    )
    draw(st.randoms()).shuffle(description_parts)
    description = " ".join(description_parts)

    # Construct the final entry
    entry = ""
    if is_complete:
        entry += completion_marker
        entry += completion_date
        if has_creation_date:
            entry += creation_date
    else:
        if has_priority:
            entry += priority
        if has_creation_date:
            entry += creation_date

    entry += description

    return entry


@given(todo_entries())
def test_fuzz_parse(text):
    penelopise.Entry(text)
