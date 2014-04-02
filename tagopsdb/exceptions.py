#
# Copyright (C) 2012 Tagged, Inc.
#
# All rights reserved

"""Custom exceptions for TagOpsDB library"""


class RepoException(Exception):
    """Base exception for manipulating repositories"""


class PackageException(Exception):
    """Base exception for manipulating pacakages"""


class DeployException(Exception):
    """Base exception for manipulating deployments"""
