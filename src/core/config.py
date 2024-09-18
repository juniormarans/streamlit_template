import secrets

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

__all__ = ["settings"]


class Settings(BaseSettings):
    API_URL_PREFIX: str | None = Field(
        None, description="Prefixo da URL da API"
    )
    API_URL: str | None = Field(
        None, description="Prefixo da URL da API"
    )
    SECRET_KEY: str | None = Field(
        description="Chave secreta para criptografia",
    )
    RESET_PASSWORD_TOKEN_EXPIRATION_MINUTES: int | None = Field(
        20, description="Validade do token de redefinição de senha em minutos"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = Field(
        86400, description="Validade do token de acesso em minutos"
    )
    REGISTER_TOKEN_EXPIRE_MINUTES: int | None = Field(
        20, description="Validade do token de registro em minutos"
    )

    PROJECT_VERSION: str | None = Field("1.0", description="Versão do projeto")
    PROJECT_NAME: str | None = Field(None, description="Nome do projeto")
    SQLALCHEMY_DATABASE_URI: str | None = Field(
        None, description="URI do banco de dados SQLAlchemy"
    )
    SMTP_TLS: bool | None = Field(None, description="Utilizar TLS para SMTP")
    SMTP_PORT: int | None = Field(None, description="Porta para conexão SMTP")
    SMTP_HOST: str | None = Field(None, description="Host para conexão SMTP")
    SMTP_PASSWORD: str | None = Field(
        None, description="Senha para conexão SMTP"
    )

    EMAILS_FROM_EMAIL: str | None = Field(
        None, description="E-mail do remetente"
    )
    EMAILS_FROM_NAME: str | None = Field(None, description="Nome do remetente")
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int | None = Field(
        48, description="Validade do token de redefinição de e-mail em horas"
    )
    DEBUG: bool = Field(description="Modo de depuração")

    FIRST_SUPERUSER: str | None = Field(
        None, description="Nome de usuário do primeiro superusuário"
    )
    FIRST_SUPERUSER_PASSWORD: str | None = Field(
        None, description="Senha do primeiro superusuário"
    )

    TEMPLATES_DIR: str | None = Field(
        None, description="Diretório de templates"
    )
    BACKEND_CORS_ORIGINS: str | None = Field(
        None, description="Origens permitidas pelo CORS"
    )
    STATIC_DIR: str | None = Field(
        None, description="Diretório de arquivos estáticos"
    )
    UPLOAD_DIR: str | None = Field(None, description="Diretório de upload")
    VALID_FILE_TYPE: str | None = Field(
        None, description="Tipos de arquivos válidos"
    )

    model_config = ConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
