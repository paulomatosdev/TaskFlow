from flask_migrate import downgrade, upgrade
from sqlalchemy import inspect

from app import create_app
from app.extensions import db


def test_migracoes_criam_e_removem_tabelas():
    """Aplica as migrações num banco vazio, como o `flask db upgrade` faz."""
    app = create_app("testing")
    with app.app_context():
        upgrade()
        tabelas = set(inspect(db.engine).get_table_names())
        assert {"user", "task", "alembic_version"} <= tabelas

        downgrade(revision="base")
        tabelas = set(inspect(db.engine).get_table_names())
        assert "user" not in tabelas
        assert "task" not in tabelas


def test_migracoes_batem_com_os_modelos():
    """Falha se você mudou um modelo e esqueceu de rodar `flask db migrate`."""
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext

    app = create_app("testing")
    with app.app_context():
        upgrade()
        with db.engine.connect() as conn:
            diff = compare_metadata(
                MigrationContext.configure(conn), db.metadata
            )
        assert diff == [], f"Modelos diferentes das migrações: {diff}"
