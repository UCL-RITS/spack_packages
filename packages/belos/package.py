from spack import *


class Belos(Package):
    """
    The Trilinos Project is an effort to develop algorithms and enabling technologies within an object-oriented
    software framework for the solution of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """
    homepage = "https://trilinos.org/"

    version(
        '12.6.3',
        '801bb24b175f52608cc1bccebb1523b6dd827839',
        url="https://github.com/trilinos/Trilinos/archive/trilinos-release-12-6-3.tar.gz"
    )

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds a debug version of the libraries')
    variant('mpi', default=True, description='Build with mpi')
    variant('openmp', default=True, description='Build with mpi')
    variant('cpp11', default=True, description='Enable C++11')
    variant('tpetra', default=True, description='Enable with Tpetra')
    variant('epetra', default=False, description='Enable with Epetra')
    variant('blas', default=True, description='Add blas dependency')
    variant('lapack', default=True, description='Add Lapack (and blas) dependency')

    depends_on('blas', when='+blas')
    depends_on('lapack', when='+lapack')
    depends_on('mpi', when="+mpi")

    def patch(self):
        filter_file(
            r"  \{ ([A-Z]*_F77.*), &lda(.*) }",
            "  {\n"
            "    int const llda = std::max(lda, 1);\n"
            "    \\1, &llda\\2\n"
            "  }",
            "packages/teuchos/numerics/src/Teuchos_BLAS.cpp"
        );
        filter_file(
            r"    ([A-Z]*_F77.*), &ldb",
            "    int const lldb = std::max(ldb, 1);\n"
            "    \\1, &lldb",
            "packages/teuchos/numerics/src/Teuchos_BLAS.cpp"
        );
        filter_file(
            r"    ([A-Z]*_F77.*), &ldc",
            "    int const lldc = std::max(ldc, 1);\n"
            "    \\1, &lldc",
            "packages/teuchos/numerics/src/Teuchos_BLAS.cpp"
        );

    def install(self, spec, prefix):
        from os import environ
        from os.path import dirname

        if spec.satisfies("%clang+openmp"):
            raise RuntimeError("Clang does not support OpenMP")
        if spec.satisfies("~epetra ~tpetra"):
            raise RuntimeError("Need one of Epetra or Tpetra")

        options = [u for u in std_cmake_args]

        blas = spec.satisfies('+blas') or spec.satisfies('+lapack')
        options.extend(['-DTrilinos_ENABLE_TESTS:BOOL=OFF',
                        '-DTrilinos_ENABLE_EXAMPLES:BOOL=OFF',
                        '-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
                        '-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if '+shared' in spec else 'OFF'),
                        '-DTPL_ENABLE_MPI:BOOL=' + ('ON' if spec.satisfies('+mpi') else 'OFF'),
                        '-DTrilinos_ENABLE_OpenMP:STRING=' + ('ON' if spec.satisfies('+openmp') else 'OFF'),
                        '-DTrilinos_ENABLE_Epetra:BOOL=' + ('ON' if spec.satisfies('+epetra') else 'OFF'),
                        '-DTrilinos_ENABLE_Tpetra:BOOL=' + ('ON' if spec.satisfies('+tpetra') else 'OFF'),
                        '-DTrilinos_ENABLE_Belos:BOOL=ON',
                        '-DTPL_ENABLE_BLAS:BOOL=%s' % ('ON' if blas else 'OFF'),
                        '-DTPL_ENABLE_LAPACK:BOOL=%s' % ('ON' if spec.satisfies('+lapack') else 'OFF'),
                        '-DTrilinos_ENABLE_CXX11=%s' % ('ON' if spec.satisfies('+cpp11') else 'OFF'),
                        '-DTrilinos_ENABLE_Fortran=OFF'
                        ])
        if spec.satisfies('+blas'):
            blas = spec['blas'].blas_libs
            options.append('-DBLAS_LIBRARY_NAMES=%s' % ';'.join(blas.names))
            options.append('-DBLAS_LIBRARY_DIRS=%s' % ';'.join(blas.directories))
        if spec.satisfies('+lapack'):
            lapack = spec['lapack'].lapack_libs
            options.append('-DLAPACK_LIBRARY_NAMES=%s' % ';'.join(lapack.names))
            options.append('-DLAPACK_LIBRARY_DIRS=%s' % ';'.join(lapack.directories))
        if spec.satisfies('+mpi'):
            mpi_bin = spec['mpi'].prefix.bin
            options.append('-DMPI_BIN_DIR:FILEPATH=%s' % mpi_bin)

        with working_dir('spack-build', create=True):
           cmake('..', *options)
           make()
           make('install')
