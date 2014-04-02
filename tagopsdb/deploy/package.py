import sqlalchemy.orm.exc

from sqlalchemy.sql.expression import func

import tagopsdb.deploy.repo as repo

import elixir

from tagopsdb.model import (
    PackageDefinition, PackageLocation, Package, ProjectPackage
)
from tagopsdb.exceptions import PackageException


def add_package(app_name, version, revision, user):
    """Add the requested version for the package of a given application"""

    pkg_loc = repo.find_app_location(app_name)
    project = repo.find_project(app_name)
    pkg_def = find_package_definition(project.id)

    if find_package(app_name, version, revision):
        raise PackageException('Current version of application "%s" '
                               'already found in Package table' % app_name)

    pkg = Package(pkg_def.id, pkg_loc.name, version, revision, 'pending',
                  func.current_timestamp(), user, pkg_loc.pkg_type,
                  pkg_loc.project_type)
    elixir.session.add(pkg)


def delete_package(app_name, version, revision):
    """Delete the requested version for the package of a given application"""

    raise NotImplementedError('This command is not implemented yet')


def find_package(app_name, version, revision):
    """Check for a specific package version"""

    # NOTE: Originally this method also used 'pkg_type' (the 'builder'
    # column in the 'packages' table) to filter; this may need to be
    # re-added at some point.

    pkg_loc = repo.find_app_location(app_name)

    try:
        return (elixir.session.query(Package)
                       .filter_by(name=pkg_loc.name)
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
        pkg_def = (elixir.session.query(PackageDefinition)
                          .join(ProjectPackage)
                          .filter(ProjectPackage.project_id == project_id)
                          .first())
    except sqlalchemy.orm.exc.NoResultFound:
        raise PackageException('Entry for project ID "%s" not found in '
                               'ProjectPackage table' % project_id)

    return pkg_def


def list_packages(app_names):
    """Return all available packages in the repository"""

    list_query = elixir.session.query(Package)

    if app_names is not None:
        list_query = \
            (list_query.join(PackageLocation,
                             PackageLocation.name == Package.name)
                       .filter(PackageLocation.app_name.in_(app_names)))

    return (list_query.order_by(Package.name, Package.version,
                                Package.revision)
                      .all())
