from spack import *

class Wcslib(Package):
    """ FITS World Coordinate Systems """
    homepage = "http://www.atnf.csiro.au/people/mcalabre/WCS/"
    url      = "ftp://ftp.atnf.csiro.au/pub/software/wcslib/wcslib.tar.bz2"

    version('5.15', '053894e777fdf1ee3a9987362f2cd74d8a913381')
    parallel = False

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
