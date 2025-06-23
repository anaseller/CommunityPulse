from typing import Any, Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    # DEFAULT
    APP_NAME: str = "CommunityPulse"
    DEBUG: bool = False
    API_VERSION: str = "v1"
    SECRET_KEY: SecretStr

    # DB
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: SecretStr
    MYSQL_DATABASE: str
    MYSQL_POOL_SIZE: int = 5
    MYSQL_POOL_TIMEOUT: int = 30

    # PROJ SETTINGS
    CORS_ORIGINS: list[str] = Field(default_factory=list)
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env.development",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> str:
        url_template = "mysql+pymysql://{user}:{password}@{host}{port}/{db}"

        return url_template.format(
            user=self.MYSQL_USER,
            # password=self.MYSQL_PASSWORD, # *******
            password=self.MYSQL_PASSWORD.get_secret_value(), # real_password
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            db=self.MYSQL_DATABASE,
        )

    def get_flask_config(self) -> Dict[str, Any]:
        return {
            "SECRET_KEY": self.SECRET_KEY.get_secret_value(),
            "DEBUG": self.DEBUG,
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_POOL_SIZE": self.MYSQL_POOL_SIZE,
            "SQLALCHEMY_POOL_TIMEOUT": self.MYSQL_POOL_TIMEOUT,
            "SQLALCHEMY_ECHO_POOL": True,
        }


settings = Settings()