# Copyright 2016 Ifwe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# WARNING WARNING WARNING
# This module is _transitional_ and will go away
# once 2.0 is in full usage
# WARNING WARNING WARNING

import yaml
import yaml.parser

from ..model import init


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
    )
