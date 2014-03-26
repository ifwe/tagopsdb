from elixir import using_options, belongs_to, has_and_belongs_to_many
from .base import Base


class NagServicesContactGroups(Base):
    using_options(tablename='nag_services_contact_groups')

    belongs_to(
        'service',
        of_kind='NagServices',
        colname='service_id',
        primary_key=True,
        ondelete='cascade',
    )

    belongs_to(
        'contact_group',
        of_kind='NagContactGroups',
        colname='contact_group_id',
        primary_key=True,
        ondelete='cascade',
    )
