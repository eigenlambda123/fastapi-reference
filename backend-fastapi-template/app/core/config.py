from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import BaseModel, Field

class EmailConfig(BaseModel):
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str = "Hackathon Boilerplate"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True

class Settings(BaseSettings):
    # ------------------------------------------------------------
    # APP CONFIG
    # ------------------------------------------------------------
    APP_NAME: str = "FastAPI App"
    ENV: str = "development"  # "development" | "production"
    SECRET_KEY: str = "changeme"

    # ------------------------------------------------------------
    # DATABASE CONFIG
    # ------------------------------------------------------------
    USE_POSTGRES: bool = False  # Toggle between SQLite and PostgreSQL

    # SQLite (default)
    SQLITE_PATH: str = "./app.db"

    # PostgreSQL (optional)
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: Optional[str] = "localhost"
    POSTGRES_PORT: Optional[int] = 5432

    # ------------------------------------------------------------
    # EMAIL CONFIG (flattened env vars)
    # ------------------------------------------------------------
    mail_username: str = Field(..., env="MAIL_USERNAME")
    mail_password: str = Field(..., env="MAIL_PASSWORD")
    mail_from: str = Field(..., env="MAIL_FROM")
    mail_port: int = Field(..., env="MAIL_PORT")
    mail_server: str = Field(..., env="MAIL_SERVER")
    mail_from_name: str = Field("Hackathon Boilerplate", env="MAIL_FROM_NAME")
    mail_starttls: bool = Field(True, env="MAIL_STARTTLS")
    mail_ssl_tls: bool = Field(False, env="MAIL_SSL_TLS")
    use_credentials: bool = Field(True, env="USE_CREDENTIALS")
    validate_certs: bool = Field(True, env="VALIDATE_CERTS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


    # ------------------------------------------------------------
    # AI CONFIG
    # ------------------------------------------------------------
    COHERE_API_KEY: str = Field(..., env="COHERE_API_KEY")

    @property
    def DB_URL(self) -> str:
        """
        Return the active database URL based on the selected mode.
        """
        if self.USE_POSTGRES:
            return (
                f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        return f"sqlite:///{self.SQLITE_PATH}"

    @property
    def email(self) -> EmailConfig:
        return EmailConfig(
            mail_username=self.mail_username,
            mail_password=self.mail_password,
            mail_from=self.mail_from,
            mail_port=self.mail_port,
            mail_server=self.mail_server,
            mail_from_name=self.mail_from_name,
            mail_starttls=self.mail_starttls,
            mail_ssl_tls=self.mail_ssl_tls,
            use_credentials=self.use_credentials,
            validate_certs=self.validate_certs,
        )


# Singleton settings instance
settings = Settings()
