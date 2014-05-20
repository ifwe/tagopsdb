import sqlalchemy
import elixir
from sqlalchemy.engine.url import URL


def init(**config):
    url = config.pop('url', {})
    url.setdefault('drivername', 'mysql+oursql')
    url.setdefault('database', 'TagOpsDB')
    do_create = config.pop('create', False)

    if do_create:
        create_url = url.copy()
        db_name = create_url.pop('database')
        engine = sqlalchemy.create_engine(URL(**create_url), **config)
        engine.execute('CREATE DATABASE IF NOT EXISTS %s' % db_name)

    elixir.metadata.bind = sqlalchemy.create_engine(
        URL(**url), **config
    )

    elixir.setup_all(create_tables=do_create)


def destroy():
    elixir.cleanup_all(drop_tables=True)
    engine = elixir.metadata.bind
    engine.execute('DROP DATABASE IF EXISTS %s' % engine.url.database)

from .model import *
