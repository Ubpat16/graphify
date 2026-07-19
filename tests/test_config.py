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
