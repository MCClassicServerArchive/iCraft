#
# The Python Imaging Library
# $Id$
#
# HDF5 stub adapter
#
# Copyright (c) 2000-2003 by Fredrik Lundh
#
# See the README file for information on usage and redistribution.
#

from reqs.pil import Image, ImageFile

_handler = None

##
# Install application-specific HDF5 image handler.
#
# @param handler Handler object.

def register_handler(handler):
    global _handler
    _handler = handler

# --------------------------------------------------------------------
# Image adapter

def _accept(prefix):
    return prefix[:8] == "\x89HDF\r\n\x1a\n"

class HDF5StubImageFile(ImageFile.StubImageFile):

    format = "HDF5"
    format_description = "HDF5"

    def _open(self):

        offset = self.fp.tell()

        if not _accept(self.fp.read(8)):
            raise SyntaxError("Not an HDF file")

        self.fp.seek(offset)

        # make something up
        self.mode = "F"
        self.size = 1, 1

        loader = self._load()
        if loader:
            loader.open(self)

    def _load(self):
        return _handler


def _save(im, fp, filename):
    if _handler is None or not hasattr("_handler", "save"):
        raise IOError("HDF5 save handler not installed")
    _handler.save(im, fp, filename)


# --------------------------------------------------------------------
# Registry

Image.register_open(HDF5StubImageFile.format, HDF5StubImageFile, _accept)
Image.register_save(HDF5StubImageFile.format, _save)

Image.register_extension(HDF5StubImageFile.format, ".h5")
Image.register_extension(HDF5StubImageFile.format, ".hdf")
