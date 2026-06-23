import os 
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

current_dir = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    DB_USER : str
    DB_PASSWORD : str
    DB_HOST : str
    DB_PORT : int 
    DB_NAME : str

    SECRET_KEY : str
    ALGORITHM : str 
    ACCESS_TOKEN_EXPIRE_MINUTES : int 
    API_KEY : str

    model_config = SettingsConfigDict(env_file=os.path.join(current_dir, ".env"), env_file_encoding="utf-8")

    def async_get_db_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    def get_db_url(self) -> str:
        return (f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")




settings = Settings()

