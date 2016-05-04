from spack import *


class Belos(Package):
    """
    The Trilinos Project is an effort to develop algorithms and enabling technologies within an object-oriented
    software framework for the solution of large-scale, complex multi-physics engineering and scientific problems.
    A unique design feature of Trilinos is its focus on packages.
    """
    homepage = "https://trilinos.org/"
    url = "http://trilinos.csbsju.edu/download/files/trilinos-12.2.1-Source.tar.gz"

    version('12.4.2', '7c830f7f0f68b8ad324690603baf404e')
    version('12.2.1', '6161926ea247863c690e927687f83be9')
    version('12.0.1', 'bd99741d047471e127b8296b2ec08017')
    version('11.14.3', '2f4f83f8333e4233c57d0f01c4b57426')
    version('11.14.2', 'a43590cf896c677890d75bfe75bc6254')
    version('11.14.1', '40febc57f76668be8b6a77b7607bb67f')

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
                        '-DTPL_ENABLE_BLAS:BOOL=%s' + ('ON' if blas else 'OFF'),
                        '-DTPL_ENABLE_LAPACK:BOOL=%s' + ('ON' if spec.satisfies('+lapack') else 'OFF'),
                        '-DTrilinos_ENABLE_CXX11=' + ('ON' if spec.satisfies('+cpp11') else 'OFF')
                        ])
        if spec.satisfies('+blas'):
            options.append('-DBLAS_LIBRARY_DIRS:PATH=%s' % spec['blas'].prefix)
        if spec.satisfies('+lapack'):
            options.append('-DLAPACK_LIBRARY_DIRS:PATH=%s' % spec['lapack'].prefix)
        if spec.satisfies('+mpi'):
            options.append('-DMPI_BIN_DIR:FILEPATH=%s' % dirname(environ['CC']))

        with working_dir('spack-build', create=True):
           cmake('..', *options)
           make()
           make('install')
