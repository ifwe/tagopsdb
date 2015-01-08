@GrabResolver('https://artifactory.tagged.com/artifactory/libs-release-local/')
@Grab('com.tagged.build:jenkins-dsl-common:[0.1.0,)')
@Grab('com.tagged.build:tagged-fpm-scriptlet:0.0.4')

import com.tagged.build.scm.*
import com.tagged.build.common.*

def project = new PythonFPMMatrixProject(
    jobFactory,
    [
        scm: new StashSCM(project: "tagopsdb", name: "tagopsdb"),
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
            pylint(999, 999, 999, "reports/pylint.log")
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
