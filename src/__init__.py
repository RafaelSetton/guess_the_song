from src.api import API
from os import path, getcwd

api = API()

CACHE_ENABLED = True
CACHE_DIR = path.join(getcwd(), "cache")

__all__ = ['api', 'CACHE_ENABLED', 'CACHE_DIR']