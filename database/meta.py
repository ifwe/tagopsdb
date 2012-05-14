"""SQLAlchemy Metadata and Session object"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = [ 'Base', 'Session' ]

Session = scoped_session(sessionmaker())
Base = declarative_base()
