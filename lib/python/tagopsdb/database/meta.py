"""SQLAlchemy Metadata and Session objects and session context manager"""

import contextlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


__all__ = [ 'Base', 'Session', 'isolated_transaction' ]

Session = scoped_session(sessionmaker())
Base = declarative_base()


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
