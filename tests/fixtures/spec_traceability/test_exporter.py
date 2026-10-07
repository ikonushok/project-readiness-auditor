from exporter import normalize


def test_normalization():
    assert normalize(["  Ada   Lovelace ", " ", "Bob", "Bob"]) == ["Ada Lovelace", "Bob", "Bob"]
