from spack import *

class Ccfits(Package):
    """CCfits is an object oriented interface to the cfitsio library"""

    homepage = "http://heasarc.gsfc.nasa.gov/fitsio/ccfits"
    url      = "http://heasarc.gsfc.nasa.gov/fitsio/ccfits/CCfits-2.4.tar.gz"

    version('2.4', '3de2a6379bc1024300befae95cfdf33645a7b64a')
    depends_on("cfitsio")

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
