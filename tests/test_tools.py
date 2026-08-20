def test_tools_module_imports() -> None:
    import app.tools.logs
    import app.tools.registry

    assert app.tools.registry.__doc__
    assert app.tools.logs.__doc__
