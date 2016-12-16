from spack import *

class Scalapack(Package):
    """library of high-performance linear algebra routines for HPC"""

    homepage = "http://www.netlib.org/scalapack/"
    url      = "http://www.netlib.org/scalapack/scalapack-2.0.2.tgz"

    version('2.0.2', 'ff9532120c2cffa79aef5e4c2f38777c6a1f3e6a')

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    variant("debug", default=False, description="Installs with debug options")

    def libs_options(self, spec):
        raise NotImplementedError("Linking to this kind of blas has not been implemented")

    @when('^openblas')
    def libs_options(self, spec):
        return ["-DBLAS_LIBRARIES=%s" % self.spec['openblas'].blas_libs,
                "-DLAPACK_LIBRARIES=%s" % self.spec['openblas'].lapack_libs]

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        options.extend(self.libs_options(spec))
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make("all")
            make("install")
