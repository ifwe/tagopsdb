from sqlalchemy import Column, ForeignKey, VARCHAR, DATE
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(u'AssetID', INTEGER(), primary_key=True)
    host_id = Column(u'HostID', INTEGER(),
                     ForeignKey('hosts.HostID', ondelete='cascade'),
                     nullable=False)
    date_received = Column(u'dateReceived', DATE())
    description = Column(VARCHAR(length=20))
    oem_serial = Column(u'oemSerial', VARCHAR(length=30), unique=True)
    service_tag = Column(u'serviceTag', VARCHAR(length=20))
    tagged_serial = Column(u'taggedSerial', VARCHAR(length=20))
    invoice_number = Column(u'invoiceNumber', VARCHAR(length=20))
    location_site = Column(u'locationSite', VARCHAR(length=20))
    location_owner = Column(u'locationOwner', VARCHAR(length=20))
    cost_per_item = Column(u'costPerItem', VARCHAR(length=20))
    date_of_invoice = Column(u'dateOfInvoice', DATE())
    warranty_start = Column(u'warrantyStart', DATE())
    warranty_end = Column(u'warrantyEnd', DATE())
    warranty_level = Column(u'warrantyLevel', VARCHAR(length=20))
    warranty_id = Column(u'warrantyID', VARCHAR(length=20))
    vendor_contact = Column(u'vendorContact', VARCHAR(length=20))

    host = relationship('Hosts', uselist=False)

    def __init__(self, host_id, date_received, description, oem_serial,
                 service_tag, tagged_serial, invoice_number, location_site,
                 location_owner, cost_per_item, date_of_invoice,
                 warranty_start, warranty_end, warranty_level, warranty_id,
                 vendor_contact):
        """ """

        self.host_id = host_id
        self.date_received = date_received
        self.description = description
        self.oem_serial = oem_serial
        self.service_tag = service_tag
        self.tagged_serial = tagged_serial
        self.invoice_number = invoice_number
        self.location_site = location_site
        self.location_owner = location_owner
        self.cost_per_item = cost_per_item
        self.date_of_invoice = date_of_invoice
        self.warranty_start = warranty_start
        self.warranty_end = warranty_end
        self.warranty_level = warranty_level
        self.warranty_id = warranty_id
        self.vendor_contact = vendor_contact
