from elixir import using_options, belongs_to
from .base import Base


class NagContactGroupsMembers(Base):
    using_options(tablename='nag_contact_groups_members')
    belongs_to(
        'contact',
        of_kind='NagContacts',
        colname='contact_id',
        primary_key=True
    )
    belongs_to(
        'contact_group',
        of_kind='NagContactGroups',
        colname='contact_group_id',
        primary_key=True
    )
