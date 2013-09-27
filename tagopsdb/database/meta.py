"""SQLAlchemy Metadata and Session objects and session context manager"""

import contextlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper, scoped_session, sessionmaker

__all__ = [ 'Base', 'Session', 'isolated_transaction' ]


class TagOpsDB(object):
    """Base class for some common default settings"""

    __table_args__ = (
        { 'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8', },
    )

    def __repr__(self):
        mapper = object_mapper(self)
        keyvals = [(key, getattr(self, key))
                   for key in mapper.columns.keys()]

        return '<%(class_name)s (%(table_name)s) %(keyvals_string)s>' % dict(
            class_name = type(self).__name__,
            table_name = self.__table__.name,
            keyvals_string = \
                ' '.join('%s=%r'% (key, val) for (key, val) in keyvals),
        )


Session = scoped_session(sessionmaker())
Base = declarative_base(cls=TagOpsDB)


@contextlib.contextmanager
def isolated_transaction(NewSession=None):
    """Manage a new transaction (session) within an existing session"""

    needed_session = True
    existing = Session.registry()

    if NewSession is None:
        NewSession = Session.session_factory()
    else:
        needed_session = False

    Session.registry.set(NewSession)

    try:
        yield
    finally:
        Session.registry.set(existing)

        if needed_session:
            NewSession.close()
