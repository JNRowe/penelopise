import penelopise


def test_noop_identical():
    """Text changes should invalidate computed properties.

    This abuses ``Entry`` in a bad way, but it is a quick way to see that we’re
    avoiding expensive nad unnecessary invalidation of properties.
    """
    e = penelopise.Entry("example")
    e.contexts = True  # type: ignore
    e.text = e.text
    assert e.contexts is True


def test_properties_invalidate_on_change():
    """Text changes should invalidate computed properties."""
    e = penelopise.Entry("example with @context")
    assert e.contexts == ["context"]
    e.text = "dropped context"
    assert not e.contexts
