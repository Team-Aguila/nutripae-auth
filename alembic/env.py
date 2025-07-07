import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Añade la raíz del proyecto al path de Python.
# Dado que este archivo está en /app/alembic/ y el WORKDIR es /app,
# Python podrá encontrar el paquete 'src'.
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- ¡¡IMPORTANTE!! ---
# Importa la Base de tus modelos y tu objeto de settings
# Asegúrate de que la ruta de importación sea correcta según tu estructura 'src'
from models.base import Base 
from core.config import settings

# Este es el objeto de configuración de Alembic, que da acceso
# a los valores del archivo .ini en uso.
config = context.config

# Interpreta el archivo de configuración para el logging de Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- ¡¡IMPORTANTE!! ---
# Establece la URL de la base de datos programáticamente desde tu objeto settings.
# Esto es más robusto y asegura que Alembic y tu app usen LA MISMA configuración.
# Sobrescribe el valor 'sqlalchemy.url' del alembic.ini.
if settings.DATABASE_URL:
    sync_database_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    config.set_main_option("sqlalchemy.url", sync_database_url)

# --- ¡¡IMPORTANTE!! ---
# Añade el objeto MetaData de tu modelo aquí para el soporte de 'autogenerate'.
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()