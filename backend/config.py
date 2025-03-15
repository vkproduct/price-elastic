import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT конфигурация
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Лимиты тарифных планов
    PLAN_LIMITS = {
        'free': {
            'sku_limit': 5,
            'data_rows_limit': 1000,
            'analysis_limit': 5,
            'storage_days': 30
        },
        'standard': {
            'sku_limit': 100,
            'data_rows_limit': 10000,
            'analysis_limit': 50,
            'storage_days': 180
        },
        'business': {
            'sku_limit': 1000,
            'data_rows_limit': 100000,
            'analysis_limit': 200,
            'storage_days': 365
        },
        'enterprise': {
            'sku_limit': 0,  # Неограниченно
            'data_rows_limit': 0,  # Неограниченно
            'analysis_limit': 0,  # Неограниченно
            'storage_days': 0  # Неограниченно
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test.db'

class ProductionConfig(Config):
    DEBUG = False
    
    # В продакшн окружении должны быть заданы переменные окружения
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}