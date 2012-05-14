from sqlalchemy import create_engine

from tagopsdb.database.meta import Base, Session
#from tagopsdb.database.test_db import Testing
from tagopsdb.database.model import *

def init_session():
    #engine = create_engine('sqlite:///testing.db', echo=True)
    engine = create_engine('mysql+oursql://tagopsdb_writer:removed@localhost'
                           '/TagOpsDB2', echo=True)
    Session.configure(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=Session.bind)

def drop_tables():
    Base.metadata.drop_all(bind=Session.bind)

def init_database():
    drop_tables()
    create_tables()
