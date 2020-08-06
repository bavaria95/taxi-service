from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    '''
        Class with application congiguration
        We can define values here directly or use env file. By default we use .env
        file, but by calling `get_settings` with env file name we can easily replace
        file from which to read configuration
    '''

    # how many cars we want to have in our world
    num_cars: int = 3

    # float number representation isn't accurate, so we have to introduce
    # margin epsilon of which error we can tolerate and assume it's the same float number
    eps = 10e-6

    class Config:
        env_file = ".env"


@lru_cache()  # caching values because reading .env file from disk is expensive
def get_settings(env_file=None):
    if env_file:
        return Settings(_env_file=env_file)

    return Settings()


settings = get_settings()
