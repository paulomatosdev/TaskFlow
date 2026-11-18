from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from flask_migrate import downgrade, upgrade
from sqlalchemy import inspect

from app import create_app
from app.extensions import db


def tabelas():
    return set(inspect(db.engine).get_table_names())


def test_migracoes_criam_e_removem_tabelas():
    with create_app("testing").app_context():
        upgrade()
        assert {"user", "task", "alembic_version"} <= tabelas()
        downgrade(revision="base")
        assert not {"user", "task"} & tabelas()


def test_migracoes_batem_com_os_modelos():  # falha se esquecer o `flask db migrate`
    with create_app("testing").app_context():
        upgrade()
        with db.engine.connect() as conn:
            diff = compare_metadata(MigrationContext.configure(conn), db.metadata)
        assert diff == [], f"Modelos diferentes das migrações: {diff}"
