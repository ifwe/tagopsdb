from elixir import using_options, belongs_to
from .base import Base


class NagServicesContacts(Base):
    using_options(tablename='nag_services_contacts')
    belongs_to(
        'service',
        of_kind='NagServices',
        colname='service_id',
        primary_key=True
    )
    belongs_to(
        'contact',
        of_kind='NagContacts',
        colname='contact_id',
        primary_key=True
    )
