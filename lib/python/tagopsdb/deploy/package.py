import sqlalchemy.orm.exc

from sqlalchemy.sql.expression import func

import tagopsdb.deploy.repo as repo

from tagopsdb.database.meta import Session
from tagopsdb.database.model import Packages
from tagopsdb.exceptions import NotImplementedException, PackageException


def add_package(app_name, version, revision, user):
    """Add the requested version for the package of a given application"""

    try:
        app = repo.list_app_location(app_name)
    except sqlalchemy.orm.exc.NoResultFound:
        raise PackageException('Application "%s" not found in '
                               'PackageLocations table' % app_name)

    if find_package(app.pkg_name, version, revision, app.pkg_type):
        raise PackageException('Current version of application "%s" '
                               'already found in Packages table' % app_name)

    pkg = Packages(app.pkg_name, version, revision, func.current_timestamp(),
                   user, app.pkg_type)
    Session.add(pkg)


def delete_package(app_name, version, revision):
    """Delete the requested version for the package of a given application"""

    raise NotImplementedException('This command is not implemented yet')


def find_package(pkg_name, version, revision, pkg_type):
    """Check for a specific package version"""

    try:
        (Session.query(Packages)
                .filter_by(pkg_name=pkg_name)
                .filter_by(version=version)
                .filter_by(revision=revision)
                .filter_by(builder=pkg_type)
                .one())
    except sqlalchemy.orm.exc.NoResultFound:
        return False
    else:
        return True


def list_packages():
    """ """

    return (Session.query(Packages)
                   .order_by(Packages.pkg_name, Packages.version,
                             Packages.revision)
                   .all())
