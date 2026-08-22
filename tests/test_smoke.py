"""Smoke tests for package importability."""


def test_incidentix_imports() -> None:
    import incidentix

    assert incidentix.__name__ == "incidentix"
