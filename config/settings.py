from config import envs
from datetime import timedelta

JWT_AUTHENTICATION = {
    'ACCESS_TOKEN_EXPIRE_MINUTES': timedelta(minutes=10),
    'REFRESH_TOKEN_EXPIRE_MINUTES': timedelta(days=7),
    'ALGORITHM': 'HS256',
    'SECRET_KEY': envs.SECRET_KEY,
}

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': envs.POSTGRES_HOST,
                'port': envs.POSTGRES_PORT,
                'user': envs.POSTGRES_USER,
                'password': envs.POSTGRES_PASSWORD,
                'database': envs.POSTGRES_DB,
            }
        },
    },
    'apps': {
        'auth': {
            'models': [
                'auth.models',
            ],
            'default_connection': 'default',
        },
        'scraper': {
            'models': [
                'scraper.models'
            ],
            'default_connection': 'default',
        },
        'people': {
            'models': [],
            'default_connection': 'default',
        },
        'models': {
            'models': [
                'aerich.models',
                'people.models',
            ],
            'default_connection': 'default',
        },
    }
}

ALLOW_ORIGINS = ['*']
