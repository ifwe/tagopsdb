import sqlalchemy.orm.exc

from sqlalchemy.sql.expression import func

import tagopsdb.deploy.repo as repo

from tagopsdb.database.meta import Session
from tagopsdb.database.model import Packages
from tagopsdb.exceptions import NotImplementedException, PackageException


def add_package(app_name, version, revision, user):
    """Add the requested version for the package of a given application"""

    app = find_app_by_name(app_name)

    if find_package(app.pkg_name, version, revision):
        raise PackageException('Current version of application "%s" '
                               'already found in Packages table' % app_name)

    pkg = Packages(app.pkg_name, version, revision, func.current_timestamp(),
                   user, app.pkg_type, app.project_type)
    Session.add(pkg)


def delete_package(app_name, version, revision):
    """Delete the requested version for the package of a given application"""

    raise NotImplementedException('This command is not implemented yet')


def find_app_by_name(app_name):
    """Return information for a given application"""

    try:
        app = repo.find_app_location(app_name)
    except sqlalchemy.orm.exc.NoResultFound:
        raise PackageException('Application "%s" not found in '
                               'PackageLocations table' % app_name)

    return app


def find_package(app_name, version, revision):
    """Check for a specific package version"""

    # NOTE: Originally this method also used 'pkg_type' (the 'builder'
    # column in the 'packages' table) to filter; this may need to be
    # re-added at some point.

    app = find_app_by_name(app_name)

    try:
        return (Session.query(Packages)
                       .filter_by(pkg_name=app.pkg_name)
                       .filter_by(version=version)
                       .filter_by(revision=revision)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        return None


def list_packages():
    """Return all available packages in the repository"""

    return (Session.query(Packages)
                   .order_by(Packages.pkg_name, Packages.version,
                             Packages.revision)
                   .all())
