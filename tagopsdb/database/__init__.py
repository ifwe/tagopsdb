import sqlalchemy.exc
import yaml
import yaml.parser

from sqlalchemy import create_engine

from .model import Base
from tagopsdb.database.meta import Session
from tagopsdb.database.model import *
from tagopsdb.exceptions import PermissionsException


def load_db_config():
    """Load configuration for database from system file"""

    data = {}
    db_host = db_name = None

    with open('/etc/tagops/tagopsdb.yml') as conf_file:
        try:
            data = yaml.load(conf_file.read())
        except yaml.parser.ParserError, e:
            raise RuntimeError('YAML parse error: %s' % e)

    # These must exist in configuration file
    try:
        db_host = data['db']['hostname']
        db_name = data['db']['db_name']
    except KeyError as e:
        raise RuntimeError('Missing parameter: %s' % e)

    return db_host, db_name


def create_dbconn_string(db_user, db_password, **kwargs):
    """Create the connection string for the database"""

    protocol = 'mysql+oursql'

    db_dict = dict(protocol=protocol, user=db_user,
                   password=db_password, host=kwargs['hostname'],
                   name=kwargs['db_name'])

    return '%(protocol)s://%(user)s:%(password)s@%(host)s/%(name)s' % db_dict


def init_session(db_user, db_password, db_host, db_name):
    """Initialize database session"""

    dbconn_string = create_dbconn_string(db_user, db_password, **kwargs)
    engine = create_engine(dbconn_string, pool_recycle=3600)

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
