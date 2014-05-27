from elixir import EntityBase, EntityMeta
from elixir import using_table_options, using_options_defaults
from sqlalchemy.orm import object_mapper


class TagOpsDBBase(EntityBase):
    """Base class for some common default settings"""
    __metaclass__ = EntityMeta

    using_options_defaults(
        table_options=dict(mysql_engine='InnoDB', mysql_charset='utf8')
    )

    @classmethod
    def all(cls, *args, **kwargs):
        q = cls.query
        if 'limit' in kwargs:
            q = q.limit(kwargs.pop('limit'))

        return q.all(*args, **kwargs)

    @classmethod
    def first(cls, *args, **kwargs):
        return cls.query.first(*args, **kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.query.filter_by(*args, **kwargs)

    def __repr__(self):
        mapper = object_mapper(self)
        all_attrs = mapper.attrs.keys()
        rel_attrs = mapper.relationships.keys()

        kv_strs = []

        for attr in sorted(all_attrs):
            if attr in rel_attrs:
                val = getattr(self, attr)
                if isinstance(val, TagOpsDBBase):
                    v_str = object.__repr__(getattr(self, attr))
                elif isinstance(val, list):
                    seq_str = 'List of %d %s' % (len(val), attr)
                    v_str = '[' + seq_str + ']'
                else:
                    v_str = repr(val)
            else:
                v_str = repr(getattr(self, attr))

            kv_strs.append('%s=%s' % (attr, v_str))

        return '<%(class_name)s (%(table_name)s) %(fields_str)s>' % dict(
            class_name=type(self).__name__,
            table_name=self.table.name,
            fields_str=' '.join(kv_strs),
        )

Base = TagOpsDBBase
