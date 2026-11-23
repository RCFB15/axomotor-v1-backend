from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "axomotor_v1"
    DATABASE_URL: str
    SECRET_KEY: str
    HASHING_ALGORITHM: str = "argon2"
    TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    USE_ALEMBIC: bool = True
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
    ]

    LINKING_TOKEN_EXPIRE_MINUTES: int = 10
    TELEGRAM_BOT_USERNAME: str
    X_BOT_API_KEY: str

    X_MQTT_CONSUMER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
