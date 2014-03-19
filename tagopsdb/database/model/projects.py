from sqlalchemy import Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import relationship

from .base import Base


class Projects(Base):
    __tablename__ = 'projects'

    id = Column(u'project_id', INTEGER(), primary_key=True)
    name = Column(VARCHAR(length=255), nullable=False, unique=True)

    proj_pkg = relationship('ProjectPackage')

    def __init__(self, name):
        """ """

        self.name = name
