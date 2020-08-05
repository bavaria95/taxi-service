from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    '''
        Class with application congiguration
        We can define values here directly or use env file. By default we use .env
        file, but by calling `get_settings` with env file name we can easily replace
        file from which to read configuration
    '''

    num_cars: int = 3

    class Config:
        env_file = ".env"


@lru_cache()  # caching values because reading .env file from disk is expensive
def get_settings(env_file=None):
    if env_file:
        return Settings(_env_file=env_file)

    return Settings()


settings = get_settings()
