from functools import lru_cache
from app.core.config import Settings, LocalSettings

@lru_cache
def get_settings():
    return Settings()

@lru_cache
def get_local_settings():
    return LocalSettings()