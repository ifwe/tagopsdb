import sqlalchemy

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper, scoped_session, sessionmaker

from .schema import References


def init(**config):
    """"""

    url = config.pop('url', {})
    url.setdefault('drivername', 'mysql+oursql')
    url.setdefault('database', 'TagOpsDB')

    engine = sqlalchemy.create_engine(URL(**url), **config)

    Session.configure(bind=engine)


class TagOpsDB(References):
    """Base class for some common default settings"""

    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def __repr__(self):
        mapper = object_mapper(self)
        keyvals = [(key, getattr(self, key))
                   for key in mapper.columns.keys()]

        return '<%(class_name)s (%(table_name)s) %(keyvals_string)s>' % dict(
            class_name = type(self).__name__,
            table_name = self.__table__.name,
            keyvals_string =
                ' '.join('%s=%r'% (key, val) for (key, val) in keyvals),
        )


Session = scoped_session(sessionmaker())

Base = declarative_base(cls=TagOpsDB)

# Constraint naming convention
#Base.metadata.naming_convention = {
#    "ix": 'ix_%(table_name)s_%(column_0_name)s',
#    "uq": "uq_%(table_name)s_%(column_0_name)s",
#    "ck": "ck_%(table_name)s_%(constraint_name)s",
#    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#    "pk": "pk_%(table_name)s",
#}
