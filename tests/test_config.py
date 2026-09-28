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


def test_load_project_environment_falls_back_to_graphify_dotenv(tmp_path, monkeypatch):
    graphify_root = tmp_path / "graphify"
    graphify_root.mkdir()
    (graphify_root / ".env").write_text("OPENAI_API_KEY=from-graphify\n", encoding="utf-8")
    monkeypatch.setattr(config, "_GRAPHIFY_ROOT", graphify_root)
    (tmp_path / "project").mkdir()
    monkeypatch.chdir(tmp_path / "project")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    assert config.load_project_environment() is True
    assert os.environ["OPENAI_API_KEY"] == "from-graphify"


def test_project_dotenv_takes_precedence_over_graphify_fallback(tmp_path, monkeypatch):
    graphify_root = tmp_path / "graphify"
    project = tmp_path / "project"
    graphify_root.mkdir()
    project.mkdir()
    (graphify_root / ".env").write_text("OPENAI_API_KEY=from-graphify\n", encoding="utf-8")
    (project / ".env").write_text("OPENAI_API_KEY=from-project\n", encoding="utf-8")
    monkeypatch.setattr(config, "_GRAPHIFY_ROOT", graphify_root)
    monkeypatch.chdir(project)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    config.load_project_environment()
    assert os.environ["OPENAI_API_KEY"] == "from-project"


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
