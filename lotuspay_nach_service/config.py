from pydantic import BaseSettings


class Settings(BaseSettings):
    perdix_base_url:str



class Config:
        env_file = "/.env"
        env_file_encoding = 'utf-8'