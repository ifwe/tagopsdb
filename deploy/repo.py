import sqlalchemy.orm.exc

from tagopsdb.database.meta import Session
from tagopsdb.database.model import PackageLocations
from tagopsdb.exceptions import RepoException


def add_app_location(pkg_type, pkg_name, app_name, path):
    """Add the location of a given application"""

    app = PackageLocations(pkg_type, pkg_name, app_name, path)
    Session.add(app)


def delete_app_location(app_name):
    """Delete the location of a given application"""

    try:
        app = list_app_location(app_name)
    except sqlalchemy.orm.exc.NoResultFound:
        raise RepoException('No application "%s" to remove from '
                            'PackageLocations table' % app_name)

    Session.delete(app)


def list_app_location(app_name):
    """ """

    return (Session.query(PackageLocations)
                   .filter_by(app_name=app_name)
                   .one())


def list_all_app_locations():
    """ """

    return (Session.query(PackageLocations).all())
