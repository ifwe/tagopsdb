from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .meta import Base, Column, String


class Project(Base):
    __tablename__ = 'projects'

    id = Column(u'project_id', INTEGER(), primary_key=True)
    name = Column(String(length=255), nullable=False, unique=True)

    applications = relationship(
        'AppDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
        lazy=False,
    )


    package_definitions = relationship(
        'PackageDefinition',
        secondary=lambda: Base.metadata.tables['project_package'],
        passive_deletes=True,
    )

    @property
    def targets(self):
        return self.applications
