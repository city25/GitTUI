def test_import_file_menu():
    """Smoke test: ensure `File` class in file menu can be imported and has a callable `main`."""
    from cli.command.file.file import File

    f = File()
    assert callable(getattr(f, "main", None))
