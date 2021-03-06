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

from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKeyConstraint


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """

    id = Column(Integer, primary_key=True)


class References(object):
    """A mixin which creates foreign key references to related classes."""

    _to_ref = set()
    _references = _to_ref.add

    @classmethod
    def __declare_first__(cls):
        """declarative hook called within the 'before_configure' mapper
        event.
        """

        for lcl, rmt in cls._to_ref:
            cls._decl_class_registry[lcl]._reference_table(
                    cls._decl_class_registry[rmt].__table__)
        cls._to_ref.clear()

    @classmethod
    def _reference_table(cls, ref_table):
        """Create a foreign key reference from the local class to the given
        remote table.

        Adds column references to the declarative class and adds a
        ForeignKeyConstraint.
        """

        # create pairs of (Foreign key column, primary key column)
        cols = [(Column(), refcol) for refcol in ref_table.primary_key]

        # set "tablename_colname = Foreign key Column" on the local class
        for col, refcol in cols:
            setattr(cls, "%s_%s" % (ref_table.name, refcol.name), col)

        # add a ForeignKeyConstraint([local columns], [remote columns])
        cls.__table__.append_constraint(ForeignKeyConstraint(*zip(*cols)))
