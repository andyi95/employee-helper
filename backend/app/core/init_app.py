import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from app.settings import settings
from vacancies.routes import router as vacancy_router


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'] if settings.DEBUG else settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=['*'] if settings.DEBUG else settings.CORS_ALLOW_METHODS,
        allow_headers=['*'] if settings.DEBUG else settings.CORS_ALLOW_HEADERS,
    )

def get_app_list():
    app_list = [f'{app}.models' for app in settings.APPLICATIONS]
    return app_list

def get_tortoise_config() -> dict:
    app_list = get_app_list()
    app_list.append('aerich.models')
    config = {
        'connections': settings.DB_CONNECTIONS,
        'apps': {
            'models': {
                'models': [*app_list, 'aerich.models'],
                'default_connection': 'default',
            }
        }
    }
    return config

TORTOISE_ORM = get_tortoise_config()

def register_db(app: FastAPI, db_url: str = None):
    db_url = db_url or settings.DB_URL
    app_list = get_app_list()
    register_tortoise(
        app,
        db_url=db_url,
        modules={'models': app_list},
        generate_schemas=True,
        add_exception_handlers=True,
    )

def register_routers(app: FastAPI):
    app.include_router(vacancy_router, prefix='/api/vacancies')

Tortoise.init_models(get_app_list(), 'models')