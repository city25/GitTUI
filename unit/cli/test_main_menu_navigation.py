def test_import_main_menu_navigation():
    """Smoke test: ensure `MainMenuNavigation` can be imported and instantiated."""
    from cli.command.main_menu_navigation import MainMenuNavigation

    m = MainMenuNavigation()
    assert hasattr(m, "main")
