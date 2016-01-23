from spack import *

class Ctemplate(Package):
    """Template language for C++"""

    homepage = "https://github.com/olafvdspek/ctemplate"
    url      = "https://github.com/OlafvdSpek/ctemplate/archive/ctemplate-2.3.tar.gz"

    version('2.3', 'be6ba46bf64287887f9b806719a851af50f79acd')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
