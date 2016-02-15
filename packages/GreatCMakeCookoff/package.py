from spack import *

class Greatcmakecookoff(Package):
    """A bunch of cmake recipes"""

    homepage = "https://github.com/UCL/GreatCMakeCookOff"
    url      = "https://github.com/UCL/GreatCMakeCookOff/archive/v2.1.1.tar.gz"

    version('2.1.2', "9335cffec655560c1041a307d1f3544a222912fb")
    version('2.1.1', "30b52a58c8c50c4645413dc7903ce71347ff65c2")

    def install(self, spec, prefix):
        from os.path import join
        cmake("-Dtests=OFF", *std_cmake_args)
        make("install")
        # fakes out spack so it installs a module file
        mkdirp(join(prefix, 'bin'))
