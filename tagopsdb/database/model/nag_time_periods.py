from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from .base import Base


class NagTimePeriods(Base):
    __tablename__ = 'nag_time_periods'

    id = Column(INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=32), nullable=False, unique=True)
    alias = Column(VARCHAR(length=80))
    sunday = Column(VARCHAR(length=32))
    monday = Column(VARCHAR(length=32))
    tuesday = Column(VARCHAR(length=32))
    wednesday = Column(VARCHAR(length=32))
    thursday = Column(VARCHAR(length=32))
    friday = Column(VARCHAR(length=32))
    saturday = Column(VARCHAR(length=32))
