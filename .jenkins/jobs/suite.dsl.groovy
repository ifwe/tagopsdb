// Copyright 2016 Ifwe Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import com.tagged.build.scm.*
import com.tagged.build.common.*

def project = new Project(
    jobFactory,
    [
        scm: new StashSCM(project: "tagopsdb", name: "tagopsdb"),
        notifyEmail: 'siteops@tagged.com',
    ]
)

// TODO: convert these test jobs to docker and centos 7.

// Report pylint warnings and go 'unstable' when over the threshold
def pylint = project.downstreamJob {
    name 'pylint'
    label 'python27 && centos6'
    steps { shell '.jenkins/scripts/pylint.sh' }

    publishers {
        warnings([], ['Pyflakes': 'reports/pyflakes.log'])
        violations {
            pylint(999, 999, 999, "reports/pylint.log")
        }
    }
}

// Run python unit tests and record results
def pyunit = project.downstreamJob {
    name 'pyunit'
    label 'python27 && centos6'
    steps { shell '.jenkins/scripts/pyunit.sh' }
    publishers {
        archiveJunit "reports/pyunit.xml"
        cobertura('coverage.xml')
    }
}

// Build RPMs
def build = project.downstreamJob {
    name 'build'
    label 'docker'

    configure { j ->
        resetScmTriggers(j)
    }

    triggers {
        scm('H/5 * * * *')
    }

    steps {
        shell 'docker_build/run.sh -- --iteration "$BUILD_NUMBER"'
        publishers {
            archiveArtifacts('docker_build/pkgs/*.rpm')
        }
    }
}

def gauntlet = project.gauntlet([
    ['Gauntlet', [pylint, pyunit]],
    ['Build', [build]],
])

def (tagopsdb, branches) = project.branchBuilders(gauntlet.name)
