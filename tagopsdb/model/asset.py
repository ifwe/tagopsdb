from elixir import Field
from elixir import Integer, String, Date
from elixir import using_options, belongs_to

from .base import Base


class Asset(Base):
    using_options(tablename='asset')

    id = Field(Integer, colname='AssetID', primary_key=True)
    date_received = Field(Date, colname='dateReceived')
    description = Field(String(length=20))
    oem_serial = Field(String(length=30), colname='oemSerial', unique=True)
    service_tag = Field(String(length=20), colname='serviceTag')
    tagged_serial = Field(String(length=20), colname='taggedSerial')
    invoice_number = Field(String(length=20), colname='invoiceNumber')
    location_site = Field(String(length=20), colname='locationSite')
    location_owner = Field(String(length=20), colname='locationOwner')
    cost_per_item = Field(String(length=20), colname='costPerItem')
    date_of_invoice = Field(Date, colname='dateOfInvoice')
    warranty_start = Field(Date, colname='warrantyStart')
    warranty_end = Field(Date, colname='warrantyEnd')
    warranty_level = Field(String(length=20), colname='warrantyLevel')
    warranty_id = Field(String(length=20), colname='warrantyID')
    vendor_contact = Field(String(length=20), colname='vendorContact')

    belongs_to('host', of_kind='Host', colname='HostID', required=True)
