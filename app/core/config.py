from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Organization Management API"
    API_V1_STR: str = "/api"

    # Database
    MASTER_DATABASE_URL: str = "postgresql://user:password@db:5432/mydb"

    # JWT
    SECRET_KEY: str = "ATi-3pbz68m_VmuJn1pzfVjLYyjhrXKBSUva3JLyogvx2gEvBjlSk3XpnLIN8x0Df8hMk0g51SvUz8nbHl4IDQ"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Organization Database Config
    ORG_DB_HOST: str = "db"
    ORG_DB_PORT: int = 5432
    ORG_DB_USER: str = "user"
    ORG_DB_PASSWORD: str = "password"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
