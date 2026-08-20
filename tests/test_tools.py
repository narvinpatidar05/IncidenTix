def test_tools_module_imports() -> None:
    import tools.logs
    import tools.registry

    assert tools.registry.__doc__
    assert tools.logs.__doc__
