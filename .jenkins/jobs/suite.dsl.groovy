@GrabResolver('https://artifactory.tagged.com/artifactory/libs-release-local/')
@Grab('com.tagged.build:jenkins-dsl-common:0.1.14')

import com.tagged.build.common.*

def project = new PythonFPMMatrixProject(
    jobFactory,
    [
        githubOwner: 'siteops',
        githubProject: 'tagopsdb',
        hipchatRoom: '/dev/null',
        notifyEmail: 'siteops@tagged.com',
        interpreters:['python26', 'python27'],
    ]
)

// Report pylint warnings and go 'unstable' when over the threshold
def pylint = project.downstreamJob {
    name 'pylint'
    label 'python26 && centos6'
    steps { shell '.jenkins/scripts/pylint.sh' }

    publishers {
        warnings([], ['Pyflakes': 'reports/pyflakes.log'])
        violations {
            pylint(207, 208, 207, "reports/pylint.log")
        }
    }
}

// Run python unit tests and record results
def pyunit = project.downstreamJob {
    name 'pyunit'
    label 'python26 && centos6'
    steps { shell '.jenkins/scripts/pyunit.sh' }
    publishers {
        archiveJunit "reports/pyunit.xml"
        cobertura('coverage.xml')
    }
}

// Build RPMs
def build = project.pythonFPMMatrixJob {
    name 'build'
    logRotator(-1, 50)

    environmentVariables([
        'FPM_PYPREFIX_PREFIX': 'TAG',
        'FPM_EXTRAS': '--no-python-downcase-name',
    ])

    triggers {
        githubPush()
    }

    steps {
        publishers {
            archiveArtifacts('*.rpm')
        }
    }
}

def gauntlet = project.gauntlet([
    ['Gauntlet', [pylint, pyunit]],
    ['Build', [build]],
])

def (tagopsdb, branches) = project.branchBuilders(gauntlet.name)
