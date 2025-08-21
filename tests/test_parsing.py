import datetime

import penelopise


def test_complete():
    """Exercise all the attributes from an input string."""
    text = "x (A) 2016-05-20 2016-04-30 measure space for +chapelShelving @chapel due:2016-05-30"
    e = penelopise.Entry(text)
    assert repr(e) == f"{e.__class__.__qualname__}({text!r})"
    assert e.text == text
    assert e.complete is True
    assert e.completion_date == datetime.date(2016, 5, 20)
    assert e.priority == penelopise.Priority.A
    assert e.contexts == [penelopise.Context("chapel")]
    assert e.projects == [penelopise.Project("chapelShelving")]
    assert e.attrs == {"due": datetime.date(2016, 5, 30)}


def test_file_input(tmp_path):
    """Test basic file parsing."""
    p = tmp_path / "todo.txt"
    p.write_text(
        "x Rule @Ithaca\n"
        "Devise machine to unravel +shroud @bed\n"
        "Cut +penelopise release\n"
    )
    entries = penelopise.Entries.parse_file(p)
    assert len(entries) == 3
