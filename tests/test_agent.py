def test_agent_module_imports() -> None:
    import agent.agent
    import agent.loop
    import agent.prompts

    assert agent.agent.__doc__
    assert agent.loop.__doc__
    assert agent.prompts.__doc__
