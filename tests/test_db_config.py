import importlib


def test_uses_sqlite_when_mysql_env_is_missing(monkeypatch):
    monkeypatch.delenv('DB_USER', raising=False)
    monkeypatch.delenv('DB_PASSWORD', raising=False)
    monkeypatch.delenv('DB_HOST', raising=False)
    monkeypatch.delenv('DB_PORT', raising=False)
    monkeypatch.delenv('DB_NAME', raising=False)

    import app.config as config_module
    importlib.reload(config_module)

    assert config_module.Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///')
