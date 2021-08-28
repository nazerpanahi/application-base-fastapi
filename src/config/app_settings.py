import os
import sys
from typing import List

from pydantic import BaseSettings

gettrace = getattr(sys, 'gettrace', None)

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SRC_DIR)


class Settings(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, '.env')
        env_file_encoding = 'utf-8'

    DEBUG: bool = True
    REGISTERED_APPLICATIONS: List[str] = [
        'api',
        'app_management'
    ]
    CORS_ORIGINS: List[str] = None


settings = Settings()

if isinstance(settings.DEBUG, str):
    settings.DEBUG = settings.DEBUG == 'True'

if settings.DEBUG or gettrace():
    pass
