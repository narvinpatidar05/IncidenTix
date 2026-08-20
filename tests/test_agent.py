def test_agent_module_imports() -> None:
    import app.agent.agent
    import app.agent.loop
    import app.agent.prompts

    assert app.agent.agent.__doc__
    assert app.agent.loop.__doc__
    assert app.agent.prompts.__doc__
