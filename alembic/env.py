from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from geoalchemy2 import alembic_helpers

from alembic import context

from app.core.config import settings
from app.db.base import Base
from app.models import buildings, organizations, activities  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

config.set_main_option("sqlalchemy.url", f"{settings.DATABASE_URL}?async_fallback=True")


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        # Загружаем имена таблиц из файла
        with open(settings.GEOALCHEMY_TABLES_FILE, "r") as file:
            ignored_tables = [line.strip().strip('"') for line in file.readlines()]

        # Игнорируем таблицы, если они есть в списке geoalchemy_tables
        if name in ignored_tables:
            return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # S.M. 2025-01-09 - to avoid errors with GeoAlchemy2
        include_object=include_object,  # exclude geoalchemy_tables from migration
        render_item=alembic_helpers.render_item,  # add geoalchemy imports to migration file
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # S.M. 2025-01-09 - to avoid errors with GeoAlchemy2
            include_object=include_object,  # exclude geoalchemy_tables from migration
            render_item=alembic_helpers.render_item,  # add geoalchemy imports to migration file
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
