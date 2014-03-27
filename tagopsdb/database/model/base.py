from sqlalchemy.orm import object_mapper
from sqlalchemy.ext.declarative import declarative_base


class TagOpsDBBase(object):
    """Base class for some common default settings"""

    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', },
    )

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
                    seq_str = ', '.join(map(object.__repr__, val[:10]))
                    v_str = '[' + seq_str + ']'
                else:
                    v_str = repr(val)
            else:
                v_str = repr(getattr(self, attr))

            kv_strs.append('\n%s=%s' % (attr, v_str))

        return '<%(class_name)s (%(table_name)s) %(fields_str)s>' % dict(
            class_name=type(self).__name__,
            table_name=self.__table__.name,
            fields_str=' '.join(kv_strs),
        )

Base = declarative_base(cls=TagOpsDBBase)
