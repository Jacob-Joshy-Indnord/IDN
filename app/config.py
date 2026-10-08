from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration, overridable via environment variables."""

    model_config = SettingsConfigDict(env_prefix="IDN_")

    jwt_secret_key: str = "dev-secret-change-me-to-a-32-byte-or-longer-random-value"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15


settings = Settings()
