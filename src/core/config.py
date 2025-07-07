from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV_STATE: str
    APP_NAME: str
    
    # Variables de entorno para la base de datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str = "localhost" # Default to localhost for local development
    DB_HOST_PORT: int = 5432

    # URL de la base de datos (construida a partir de las variables anteriores)
    DATABASE_URL: str | None = None

    @field_validator("DATABASE_URL", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: str | None, values) -> any:
        if isinstance(v, str):
            return v
        
        data = values.data
        return f"postgresql+psycopg2://{data.get('POSTGRES_USER')}:{data.get('POSTGRES_PASSWORD')}@{data.get('DB_HOST')}:{data.get('DB_HOST_PORT')}/{data.get('POSTGRES_DB')}"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ADMIN_USER_EMAIL: str 
    ADMIN_USER_PASSWORD: str

    BASE_USER_EMAIL: str 
    BASE_USER_PASSWORD: str

    API_PREFIX_STR: str = "/api/v1"

    OTLP_GRPC_ENDPOINT: str

    model_config = SettingsConfigDict(
        env_file=f".env",
        extra="ignore"
    )

# Instancia global de la configuración
settings = Settings()