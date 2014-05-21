from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Project(Base):
    __tablename__ = 'projects'

    id = Column(u'project_id', INTEGER(), primary_key=True)
    name = Column(String(length=255), nullable=False, unique=True)
    proj_pkg = relationship('ProjectPackage')
