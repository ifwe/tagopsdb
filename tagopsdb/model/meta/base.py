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

import sqlalchemy

from collections import OrderedDict as odict

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper, scoped_session, sessionmaker

import tagopsdb.exceptions

from .schema import References


def init(**config):
    if initialized(**config) and not config.get('force'):
        return

    attrs = _module_attrs(config.pop('module', None))

    attrs['_initialized'] = True

    url = config.pop('url', {})
    url.setdefault('drivername', 'mysql+pymysql')
    url.setdefault('database', 'TagOpsDB')
    url.setdefault('query', {'charset': 'utf8'})
    do_create = config.pop('create', False)

    if do_create:
        create_url = url.copy()
        db_name = create_url.pop('database')
        engine = sqlalchemy.create_engine(URL(**create_url), **config)
        engine.execute('CREATE DATABASE IF NOT EXISTS %s' % db_name)

    engine = sqlalchemy.create_engine(
        URL(**url), **config
    )
    attrs['Base'].metadata.bind = engine

    if do_create:
        attrs['Base'].metadata.create_all(engine)

    attrs['Base'].Session = attrs['Session'] = scoped_session(sessionmaker())
    attrs['Session'].configure(bind=engine)


def destroy(module=None):
    if initialized(module=module):
        attrs = _module_attrs(module)
        attrs['Session'].close()
        attrs['Session'].remove()
        attrs['Base'].Session = attrs['Session'] = None

        attrs['_initialized'] = False

    if attrs['Base'].metadata.bind is not None:
        attrs['Base'].metadata.bind.execute('DROP DATABASE IF EXISTS %s' % attrs['Base'].metadata.bind.url.database)
        attrs['Base'].metadata.bind.dispose()
        attrs['Base'].metadata.bind = None


class TagOpsDB(References):
    """Base class for some common default settings"""

    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'},
    )

    def to_dict(self):
        mapper = object_mapper(self)
        return odict(
            (key, getattr(self, key))
            for key in mapper.columns.keys()
        )

    def __repr__(self):
        return '<%(class_name)s (%(table_name)s) %(keyvals_string)s>' % dict(
            class_name = type(self).__name__,
            table_name = self.__table__.name,
            keyvals_string =
                ' '.join('%s=%r'% (key, val)
                    for (key, val) in self.to_dict().iteritems()),
        )

    def __eq__(self, other):
        if not callable(getattr(other, 'to_dict', None)):
            return False

        return self.to_dict().__eq__(other.to_dict())

    def delete(self, *args, **kwargs):
        return self.Session.delete(self, *args, **kwargs)

    def refresh(self):
        return self.Session.refresh(self)

    @classmethod
    def query(cls):
        return cls.Session.query(cls)

    @classmethod
    def get_by(cls, **kwds):
        try:
            return cls.query().filter_by(**kwds).one()
        except sqlalchemy.orm.exc.MultipleResultsFound as e:
            raise tagopsdb.exceptions.MultipleInstancesException(e)
        except sqlalchemy.orm.exc.NoResultFound as e:
            return None

    get = get_by

    @staticmethod
    def group_by(query, kwds):
        group_by_arg = kwds.pop('group_by', None)
        if group_by_arg is not None:
            query = query.group_by(group_by_arg)

        return query

    @staticmethod
    def limit(query, kwds):
        limit_arg = kwds.pop('limit', None)
        if limit_arg is not None:
            query = query.limit(limit_arg)

        return query

    @staticmethod
    def order_by(query, kwds):
        order_by_arg = kwds.pop('order_by', None)
        if order_by_arg is not None:
            desc_arg = kwds.pop('desc', None)
            if desc_arg is not None:
                query = query.order_by(sqlalchemy.desc(order_by_arg))
            else:
                query = query.order_by(order_by_arg)

        return query

    @staticmethod
    def find_filter(kwds):
        kwds.pop('limit', None)
        kwds.pop('order_by', None)
        kwds.pop('desc', None)

        return kwds

    @classmethod
    def find(cls, **kwds):
        filter_kwds = cls.find_filter(kwds.copy())

        q = cls.query()
        q = q.filter_by(**filter_kwds)
        q = cls.group_by(q, kwds)
        q = cls.order_by(q, kwds)
        q = cls.limit(q, kwds)

        try:
            return q.all()
        except sqlalchemy.orm.exc.NoResultFound as e:
            return []

    @classmethod
    def all(cls, *args, **kwargs):
        q = cls.query()
        q = cls.order_by(q, kwargs)
        q = cls.limit(q, kwargs)

        return q.all(*args, **kwargs)

    @classmethod
    def update_or_create(cls, data, surrogate=True):
        pk_props = [x for x in cls.__table__.columns if x.primary_key]

        pk_vals = [data.get(p.key, None) for p in pk_props]
        # if any pk are missing or None
        if any(x is None for x in pk_vals):
            if surrogate:
                record = cls()
            else:
                raise Exception("Cannot create non surrogate without pk")
        else:
            record = cls.query().get(tuple(pk_vals))
            if record is None:
                if not surrogate:
                    record = cls()
                else:
                    raise Exception("Cannot create surrogate with pk")

        record.from_dict(data)
        Session.add(record)
        return record

    @classmethod
    def first(cls, *args, **kwargs):
        return cls.query().first(*args, **kwargs)

    def from_dict(self, data):
        """
        Update a mapped class with data from a JSON-style nested dict/list
        structure.
        """
        # surrogate can be guessed from autoincrement/sequence but I guess
        # that's not 100% reliable, so we'll need an override

        mapper = sqlalchemy.orm.object_mapper(self)

        for key, value in data.iteritems():
            if isinstance(value, dict):
                dbvalue = getattr(self, key)
                rel_class = mapper.get_property(key).mapper.class_
                pk_props = rel_class._descriptor.primary_key_properties

                # If the data doesn't contain any pk, and the relationship
                # already has a value, update that record.
                if not [1 for p in pk_props if p.key in data] and \
                   dbvalue is not None:
                    dbvalue.from_dict(value)
                else:
                    record = rel_class.update_or_create(value)
                    setattr(self, key, record)
            elif isinstance(value, list) and \
                 value and isinstance(value[0], dict):

                rel_class = mapper.get_property(key).mapper.class_
                new_attr_value = []
                for row in value:
                    if not isinstance(row, dict):
                        raise Exception(
                                'Cannot send mixed (dict/non dict) data '
                                'to list relationships in from_dict data.')
                    record = rel_class.update_or_create(row)
                    new_attr_value.append(record)
                setattr(self, key, new_attr_value)
            else:
                setattr(self, key, value)


Base = declarative_base(cls=TagOpsDB)
class HasDummy(object): dummy = '__dummy__'

Session = None
_initialized = False


def initialized(module=None, **_kwds):
    'Whether or not init() has been called'

    attrs = _module_attrs(module)
    return attrs.get('Session', None) is not None and attrs.get('_initialized', False)


def _module_attrs(module):
    if module is None:
        return globals()
    else:
        return vars(module)


# Constraint naming convention
#Base.metadata.naming_convention = {
#    "ix": 'ix_%(table_name)s_%(column_0_name)s',
#    "uq": "uq_%(table_name)s_%(column_0_name)s",
#    "ck": "ck_%(table_name)s_%(constraint_name)s",
#    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#    "pk": "pk_%(table_name)s",
#}
