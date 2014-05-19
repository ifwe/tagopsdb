#
# Copyright (C) 2012 Tagged, Inc.
#
# All rights reserved

"""Custom exceptions for TagOpsDB library"""


class RepoException(Exception):
    """Base exception for manipulating repositories"""


class PackageException(Exception):
    """Base exception for manipulating packages"""


class DeployException(Exception):
    """Base exception for manipulating deployments"""


# WARNING WARNING WARNING
# The below exceptions are _transitional_ and will go away
# once 2.0 is in full usage
# WARNING WARNING WARNING
class PermissionsException(Exception):
    """Exception for handling permission errors"""


class NotImplementedException(Exception):
    """Exception for an unimplemented method"""
