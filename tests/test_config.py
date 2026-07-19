import os

from graphify import config


def test_load_project_environment_loads_dotenv_values(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("OPENAI_API_KEY=from-dotenv\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    assert config.load_project_environment() is True
    assert os.environ["OPENAI_API_KEY"] == "from-dotenv"


def test_load_project_environment_does_not_override_exported_values(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("OPENAI_API_KEY=from-dotenv\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "from-shell")

    config.load_project_environment()

    assert os.environ["OPENAI_API_KEY"] == "from-shell"


def test_install_does_not_parse_project_dotenv(tmp_path, monkeypatch, capsys):
    from graphify.__main__ import main

    (tmp_path / ".env").write_text("not a dotenv assignment\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["graphify", "install", "--project", "codex"])

    main()

    assert "could not parse" not in capsys.readouterr().err


def test_load_project_environment_ignores_invalid_lines_without_noise(
    tmp_path, monkeypatch, caplog
):
    (tmp_path / ".env").write_text(
        "OPENAI_API_KEY=from-dotenv\nnot a dotenv assignment\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    config.load_project_environment()

    assert os.environ["OPENAI_API_KEY"] == "from-dotenv"
    assert "could not parse" not in caplog.text
