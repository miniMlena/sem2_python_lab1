import pytest

def test_cli_instruct(capsys):
    '''Тестируем команду instruct'''
    from src.cli import cli
    with pytest.raises(SystemExit):
        cli(["instruct"])
    captured = capsys.readouterr()
    assert "1) instruct" in captured.out
    assert "2) sources" in captured.out
    assert "3) read" in captured.out

def test_cli_sources(capsys):
    '''Тестируем команду sources'''
    from src.cli import cli
    with pytest.raises(SystemExit):
        cli(["sources"])
    captured = capsys.readouterr()
    assert "stdin" in captured.out
    assert "jsonl-file" in captured.out
