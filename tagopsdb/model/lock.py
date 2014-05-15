from sqlalchemy import Table

from .meta import Base, Column, String


lock = Table(u'locks', Base.metadata,
    Column(u'val', String(length=64), nullable=False, unique=True),
    Column(u'host', String(length=32), nullable=False),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
