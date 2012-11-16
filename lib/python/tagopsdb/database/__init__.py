import sqlalchemy.exc
import yaml

from sqlalchemy import create_engine

from tagopsdb.database.meta import Base, Session
#from tagopsdb.database.test_db import Testing
from tagopsdb.database.model import *
from tagopsdb.exceptions import PermissionsException


def create_dbconn_string(db_user, db_password):
    """Create the connection string for the database"""

    with open('/etc/tagops/tagopsdb.yml') as conf_file:
        try:
            data = yaml.load(conf_file.read())
        except yaml.parser.ParserError, e:
            raise RuntimeError('YAML parse error: %s' % e)

    db_host = data['db']['hostname']
    db_name = data['db']['db_name']

    return 'mysql+oursql://%s:%s@%s/%s' % (db_user, db_password,
                                           db_host, db_name)


def init_session(db_user, db_password, echo=False):
    #engine = create_engine('sqlite:///testing.db', echo=True)
    dbconn_string = create_dbconn_string(db_user, db_password)
    engine = create_engine(dbconn_string, echo=echo)

    # Ensure connection information is valid
    try:
        engine.execute('select 1').scalar()
    except sqlalchemy.exc.DBAPIError, e:
        raise PermissionsException(e)

    Session.configure(bind=engine)


def create_tables():
    Base.metadata.create_all(bind=Session.bind)


def drop_tables():
    Base.metadata.drop_all(bind=Session.bind)


def init_database():
    drop_tables()
    create_tables()
