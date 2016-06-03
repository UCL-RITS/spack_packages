from spack import depends_on, extends, version
from spack import Package


class PyCasacore(Package):
    """ Python bindings for casacore """
    homepage = "https://github.com/casacore/python-casacore"
    url      = "https://github.com/casacore/python-casacore/archive/v2.1.2.tar.gz"

    version('2.1.2', 'cc5873babd7f04c9e587ec00618537e07e5773f8')

    extends("python")
    depends_on("casacore +python")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

