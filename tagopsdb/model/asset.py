from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import DATE, INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(u'AssetID', INTEGER(), primary_key=True)
    host_id = Column(
        u'HostID',
        INTEGER(),
        ForeignKey('hosts.HostID', ondelete='cascade'),
        nullable=False
    )
    date_received = Column(u'dateReceived', DATE())
    description = Column(String(length=20))
    oem_serial = Column(u'oemSerial', String(length=30), unique=True)
    service_tag = Column(u'serviceTag', String(length=20))
    tagged_serial = Column(u'taggedSerial', String(length=20))
    invoice_number = Column(u'invoiceNumber', String(length=20))
    location_site = Column(u'locationSite', String(length=20))
    location_owner = Column(u'locationOwner', String(length=20))
    cost_per_item = Column(u'costPerItem', String(length=20))
    date_of_invoice = Column(u'dateOfInvoice', DATE())
    warranty_start = Column(u'warrantyStart', DATE())
    warranty_end = Column(u'warrantyEnd', DATE())
    warranty_level = Column(u'warrantyLevel', String(length=20))
    warranty_id = Column(u'warrantyID', String(length=20))
    vendor_contact = Column(u'vendorContact', String(length=20))
    host = relationship('Host', uselist=False)
