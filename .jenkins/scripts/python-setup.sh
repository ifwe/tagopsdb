#!/bin/bash
#
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

set -e

if [[ -z "$WORKSPACE" ]] ; then
    scripts=$(dirname "${BASH_SOURCE-$0}")
    scripts=$(cd "$scripts">/dev/null; pwd)
    WORKSPACE=$(cd "$scripts/../.." >/dev/null; pwd)
    export WORKSPACE
fi

export SITEOPS_VIRTUALENV=$WORKSPACE/jenkins-venv
export PYTHONPATH=$PYTHONPATH:.

if [ -n "$VIRTUAL_ENV" ] ; then
    # shellcheck source=/dev/null
    source "$VIRTUAL_ENV"/bin/activate
    deactivate
fi

if python2.7 --version &>/dev/null ; then
    PYTHON=python2.7
    VENV=virtualenv-2.7
else
    PYTHON=python
    VENV=virtualenv
fi

if ! [[ -d "$SITEOPS_VIRTUALENV" && -f "$SITEOPS_VIRTUALENV/bin/activate" ]] ; then
    if ! command -v "$VENV" ; then
        wget http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.1.tar.gz
        tar -xzf virtualenv-1.9.1.tar.gz
        rm virtualenv-1.9.1.tar.gz
        pushd virtualenv-1.9.1
        "$PYTHON" virtualenv.py "$SITEOPS_VIRTUALENV"
        popd
    else
        "$VENV" "$SITEOPS_VIRTUALENV"
    fi

    if [ -d virtualenv-1.9.1 ] ; then
        rm -rf virtualenv-1.9.1
    fi
fi

export PATH=$PATH:$SITEOPS_VIRTUALENV/bin
# shellcheck source=/dev/null
source "$SITEOPS_VIRTUALENV/bin/activate"

if [ -f requirements.txt ]; then
   pip install -r requirements.txt --allow-all-external --allow-unverified progressbar
fi

if [ -f requirements-dev.txt ]; then
   pip install -r requirements-dev.txt --allow-all-external --allow-unverified progressbar
fi

rm -rf reports

if [ ! -d reports ]; then
  mkdir reports
fi
