import sqlalchemy.orm.exc

from sqlalchemy.sql.expression import func

import tagopsdb.deploy.repo as repo

from tagopsdb.database.meta import Session
from tagopsdb.database.model import PackageDefinition, PackageLocations, \
                                    Packages, ProjectPackage
from tagopsdb.exceptions import PackageException


def add_package(app_name, version, revision, user):
    """Add the requested version for the package of a given application"""

    app = find_app_by_name(app_name)
    project = repo.find_project(app_name)
    pkg_def = find_package_definition(project.id)

    if find_package(app_name, version, revision):
        raise PackageException('Current version of application "%s" '
                               'already found in Packages table' % app_name)

    pkg = Packages(pkg_def.id, app.pkg_name, version, revision, 'pending',
                   func.current_timestamp(), user, app.pkg_type,
                   app.project_type)
    Session.add(pkg)


def delete_package(app_name, version, revision):
    """Delete the requested version for the package of a given application"""

    raise NotImplementedError('This command is not implemented yet')


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


def find_package_definition(project_id):
    """Find package definition for a given package

       Note that in this transitional state, we are actually checking
       against the project and that there will be only one entry in
       the ProjectPackage table for a given project.  THIS WILL CHANGE.
    """

    try:
        pkg_def = (Session.query(PackageDefinition)
                          .join(ProjectPackage)
                          .filter(ProjectPackage.project_id==project_id)
                          .first())
    except sqlalchemy.orm.exc.NoResultFound:
        raise PackageException('Entry for project ID "%s" not found in '
                               'ProjectPackages table' % project_id)

    return pkg_def


def list_packages(app_names):
    """Return all available packages in the repository"""

    list_query = Session.query(Packages)

    if app_names is not None:
        list_query = \
            (list_query.join(PackageLocations,
                             PackageLocations.pkg_name==Packages.pkg_name)
                       .filter(PackageLocations.app_name.in_(app_names)))

    return (list_query.order_by(Packages.pkg_name, Packages.version,
                                Packages.revision)
                      .all())
