from sqlalchemy import Column, Table, VARCHAR

from .base import Base


Locks = locks = Table(
    u'locks',
    Base.metadata,
    Column(u'val', VARCHAR(length=64), nullable=False, unique=True),
    Column(u'host', VARCHAR(length=32), nullable=False),
    mysql_engine='InnoDB', mysql_charset='utf8',
)
