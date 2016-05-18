# Copyright 2016 Ifwe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Copyright (C) 2012 Tagged, Inc.
#
# All rights reserved

"""Custom exceptions for TagOpsDB library"""


class RepoException(Exception):
    """Base exception for manipulating repositories"""
    pass


class PackageException(Exception):
    """Base exception for manipulating packages"""
    pass


class DeployException(Exception):
    """Base exception for manipulating deployments"""
    pass


class MultipleInstancesException(Exception):
    """Exception to catch multiple results when there should be one"""
    pass


# WARNING WARNING WARNING
# The below exceptions are _transitional_ and will go away
# once 2.0 is in full usage
# WARNING WARNING WARNING
class PermissionsException(Exception):
    """Exception for handling permission errors"""
    pass


class NotImplementedException(Exception):
    """Exception for an unimplemented method"""
    pass
