from pydantic_settings import BaseSettings


class EnvsConfig(BaseSettings):
    LINKEDIN_BASE_URL: str
    LINKEDIN_USERNAME: str
    LINKEDIN_PASSWORD: str

    class Config:
        case_sensitive = False
        env_file = '.env'
        extra = 'ignore'


envs = EnvsConfig()
