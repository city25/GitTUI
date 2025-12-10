import pytest


@pytest.mark.skip(reason="interactive flow; run manually or mock prompts")
def test_new_repository_interactive_flow():
    """Integration placeholder for new repository interactive flow.

    This test is intentionally skipped in automated runs. Replace with
    a mocked interactive flow using `monkeypatch` when enabling CI tests.
    """
    # Import should succeed; we don't execute interactive prompts here.
    from cli.command.file.file_module import new_repository

    assert new_repository is not None
