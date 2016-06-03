from spack import *

class Casacore(Package):
    """ Suite of c++ libraries for radio astronomy data processing """

    homepage = "https://github.com/casacore/casacore"
    url      = "https://github.com/casacore/casacore/archive/v2.1.0.tar.gz"

    version('2.1.0', '1e66c9aacac4820fc126a7a5082e3904564a388d')
    variant("debug", default=False, description="Compile in debug mode")
    variant("python", default=False, description="Needed to compile python-casacore")
    variant("fftw", default=False, description="Use FFTW rather than FFTpack")

    depends_on("cfitsio")
    depends_on("wcslib")
    depends_on("python", when="+python")
    depends_on("boost +python", when="+python")
    depends_on("bison")
    depends_on("flex")
    depends_on("fftw@3:", when="+fftw")
    depends_on("py-numpy", when="+python")
    # depends_on("lapack")
    # depends_on("blas")

    def install(self, spec, prefix):
        from os import environ
        options = [u for u in std_cmake_args]

        build_type = 'Debug' if '+debug' in spec else 'Release'
        options.append('-DCMAKE_BUILD_TYPE:STRING=%s' % build_type)

        with_python, with_python3 = False, False
        if '+python' in spec:
            with_python = spec.dependencies['python'].version < ver("3.0.0")
            with_python3 = spec.dependencies['python'].version >= ver("3.0.0")
        options.append('-DBUILD_PYTHON=%s' % ('ON' if with_python else 'OFF'))
        options.append('-DBUILD_PYTHON3=%s' % ('ON' if with_python3 else 'OFF'))

        options.append('-DUSE_FFTW3=%s' % ('ON' if '+fftw' in spec else 'OFF'))
        options.append('-DMODULE=all')

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")
