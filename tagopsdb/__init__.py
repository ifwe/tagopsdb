import sqlalchemy
import elixir
from sqlalchemy.engine.url import URL


def init(**config):
    url = config.pop('url', {})
    url.setdefault('drivername', 'mysql+oursql')
    url.setdefault('database', 'TagOpsDB')

    elixir.metadata.bind = sqlalchemy.create_engine(
        URL(**url), **config
    )

    elixir.setup_all()

from .model import *
