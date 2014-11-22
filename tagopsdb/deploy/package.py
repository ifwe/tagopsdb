import sqlalchemy.orm.exc

from sqlalchemy.sql.expression import func

import tagopsdb.deploy.repo as repo

from tagopsdb import Session
from tagopsdb.model import (
    PackageDefinition, Package, ProjectPackage
)
from tagopsdb.exceptions import PackageException


def add_package(app_name, version, revision, user):
    """Add the requested version for the package of a given application"""

    pkg_def = find_package_definition(app_name)

    if find_package(app_name, version, revision):
        raise PackageException('Current version of application "%s" '
                               'already found in Package table' % app_name)

    pkg = Package(
        pkg_def_id=pkg_def.id,
        pkg_name=app_name,
        version=version,
        revision=revision,
        status='pending',
        created=func.current_timestamp(),
        creator=user,
        builder=pkg_def.build_type,
        project_type='application'
    )
    Session.add(pkg)


def delete_package(app_name, version, revision):
    """Delete the requested version for the package of a given application"""

    raise NotImplementedError('This command is not implemented yet')


def find_package(app_name, version, revision):
    """Check for a specific package version"""

    # NOTE: Originally this method also used 'pkg_type' (the 'builder'
    # column in the 'packages' table) to filter; this may need to be
    # re-added at some point.

    pkg_def = find_package_definition(app_name)

    if pkg_def is None:
        return None

    try:
        return (Session.query(Package)
                       .filter_by(pkg_name=pkg_def.pkg_name)
                       .filter_by(version=version)
                       .filter_by(revision=revision)
                       .one())
    except sqlalchemy.orm.exc.NoResultFound:
        return None


def find_package_definition(app_name):
    """Find package definition for a given package"""

    try:
        # Note: can there be multiple package definitions
        # with the same pkg_name?
        pkg_def = (Session.query(PackageDefinition)
                          .filter_by(pkg_name=app_name)
                          .first())
    except sqlalchemy.orm.exc.NoResultFound:
        raise PackageException('Entry for application "%s" not found in '
                               'PackageDefinition table' % app_name)

    return pkg_def


def list_packages(app_names):
    """Return all available packages in the repository"""

    if app_names is None:
        return None

    return (Session.query(Package)
                   .join(PackageDefinition)
                   .filter(PackageDefinition.pkg_name == Package.pkg_name)
                   .filter(PackageDefinition.pkg_name.in_(app_names))
                   .order_by(Package.pkg_name, Package.version,
                             Package.revision)
                   .all())
