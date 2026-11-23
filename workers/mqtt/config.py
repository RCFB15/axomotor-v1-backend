from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MQTT_CONSUMER_HOST: str = "localhost"
    MQTT_CONSUMER_USER: str = "consumer"
    MQTT_CONSUMER_PASSWORD: str
    X_MQTT_CONSUMER_HOST: str
    X_MQTT_CONSUMER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
