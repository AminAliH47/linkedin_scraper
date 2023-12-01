from config import envs


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
