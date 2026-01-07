"""
Konfigurace pro Joker API
Centralizované nastavení pro různá prostředí
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Základní konfigurace"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    DEBUG = False
    TESTING = False

    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))

    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # Rate Limiting
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per minute')
    REDIS_URL = os.getenv('REDIS_URL', 'memory://')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = 'logs'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 10

    # Jokes
    JOKES_DIR = 'jokes'
    SUPPORTED_LANGUAGES = ['cz', 'sk', 'en-gb', 'en-us']
    SUPPORTED_CATEGORIES = ['normal', 'explicit']

    # Auto-Update
    AUTO_UPDATE_ENABLED = os.getenv('AUTO_UPDATE_ENABLED', 'true').lower() == 'true'
    UPDATE_CHECK_INTERVAL = int(os.getenv('UPDATE_CHECK_INTERVAL', 172800))  # 48 hodin
    GIT_BRANCH = os.getenv('GIT_BRANCH', 'main')


class DevelopmentConfig(Config):
    """Konfigurace pro vývoj"""
    DEBUG = True
    RATE_LIMIT = '1000 per minute'  # Vyšší limit pro development


class ProductionConfig(Config):
    """Konfigurace pro produkci"""
    DEBUG = False
    # V produkci je dobré mít nižší limity
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per minute')


class TestingConfig(Config):
    """Konfigurace pro testování"""
    TESTING = True
    RATE_LIMIT = '10000 per minute'  # Bez omezení pro testy


# Slovník konfigurací
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}


def get_config(env=None):
    """Získá konfiguraci podle prostředí"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'production')
    return config.get(env, config['default'])
