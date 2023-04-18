import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEBUG = True

    APPLICATIONS = [
        'users',
        'vacancies',

    ]
    VERSION = '0.1.0'
    APP_TITLE = 'Template Application'
    PROJECT_NAME = 'Template Application'
    APP_DESCRIPTION = 'TG - @AKuzyashin\nhttps://github.com/Kuzyashin'

    SERVER_HOST = 'localhost'

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT = os.path.join(BASE_DIR, "app/logs")
    DB_URL = 'postgres://postgres:postgres@localhost:5432/hh_cabinet'
    DB_CONNECTIONS = {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'db_url': DB_URL,
                'credentials': {
                    'host': 'localhost',
                    'port': '5432',
                    'user': 'postgres',
                    'password': 'postgres',
                    'database': 'hh_cabinet',
                }
            },
        }

    SECRET_KEY = '3488a63e1765035d386f05409663f55c83bfae3b3c61a932744b20ad14244dcf'  # openssl rand -hex 32
    JWT_ALGORITHM = 'HS25'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 day
    APPLICATIONS_MODULE = 'app'

    CORS_ORIGINS = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:5000",
        "http://localhost:3000",
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

settings = Settings()
