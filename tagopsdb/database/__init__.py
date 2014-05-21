# WARNING WARNING WARNING
# This module is _transitional_ and will go away
# once 2.0 is in full usage
# WARNING WARNING WARNING

import yaml
import yaml.parser

from ..model.meta import init


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


def init_session(db_user, db_password, **kwargs):
    """Initialize database session"""

    if 'hostname' not in kwargs or 'db_name' not in kwargs:
        db_host, db_name = load_db_config()
        kwargs.setdefault('hostname', db_host)
        kwargs.setdefault('db_name', db_name)

    init(
        url=dict(
            username=db_user,
            password=db_password,
            host=kwargs['hostname'],
            database=kwargs['db_name'],
        ),
        pool_recycle=3600
    )
