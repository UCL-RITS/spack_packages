from spack import *

class Wcslib(Package):
    """ FITS World Coordinate Systems """
    homepage = "http://www.atnf.csiro.au/people/mcalabre/WCS/"
    url      = "ftp://ftp.atnf.csiro.au/pub/software/wcslib/wcslib.tar.bz2"

    version('5.16', 'b7bcb6426405cb15e13fb8b217c954ebe869a522')
    parallel = False

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
