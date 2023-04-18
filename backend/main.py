from fastapi import FastAPI

from app.core.init_app import init_middlewares, register_db, register_routers

try:
    from app.settings import settings
except ImportError:
    raise UnicodeDecodeError('Can not import settings. Create settings file from template.config.py')

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.VERSION,
)
init_middlewares(app)
register_db(app)
register_routers(app)
