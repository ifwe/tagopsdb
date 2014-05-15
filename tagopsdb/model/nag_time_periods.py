from .meta import Base, Column, String, SurrogatePK


class NagTimePeriod(SurrogatePK, Base):
    __tablename__ = 'nag_time_periods'

    name = Column(String(length=32), nullable=False, unique=True)
    alias = Column(String(length=80))
    sunday = Column(String(length=32))
    monday = Column(String(length=32))
    tuesday = Column(String(length=32))
    wednesday = Column(String(length=32))
    thursday = Column(String(length=32))
    friday = Column(String(length=32))
    saturday = Column(String(length=32))
