from pydantic_settings import BaseSettings


class EnvsConfig(BaseSettings):
    LINKEDIN_BASE_URL: str
    LINKEDIN_USERNAME: str
    LINKEDIN_PASSWORD: str

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        case_sensitive = False
        env_file = '.env'
        extra = 'ignore'


envs = EnvsConfig()
