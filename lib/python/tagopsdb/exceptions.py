#
# Copyright (C) 2012 Tagged, Inc.
#
# All rights reserved

"""Custom exceptions for TagOpsDB library"""


# General exceptions
class NotImplementedException(Exception):
    """Exception for an unimplemented method"""

    pass


# Repository exceptions
class RepoException(Exception):
    """Base exception for repository handling, use specific handlers below"""

    pass


class HudsonException(RepoException):
    """Exception for Hudson repository"""

    pass


class JenkinsException(RepoException):
    """Exception for Jenkins repository"""

    pass


class TagConfigException(RepoException):
    """Exception for tagconfig repository"""

    pass


# Package exceptions
class PackageException(exception):
    """Base exception for package handling, use more specific handlers when
    available
    """

    pass


# Deployment exceptions
