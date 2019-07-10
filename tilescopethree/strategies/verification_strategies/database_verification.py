"""A strategy for checking if a tiling is a subset of the class."""
from base64 import b64decode, b64encode
from comb_spec_searcher import VerificationStrategy
from logzero import logger
from tilings import Tiling

import os


dir_path = os.path.dirname(os.path.realpath(__file__))
filenames = ["012_depth_5_database_twisted.txt"]
database = set()


def database_verified(tiling, **kwargs):
    if not database and filenames:
        for filename in filenames:
            logger.info("Importing database from '{}'.".format(filename),
                        extra=kwargs['logger'])
            f = open(dir_path + "/" + filename, 'r')
            for line in f.readlines():
                compression = b64decode(line.encode())
                dbtiling = Tiling.decompress(compression)
                database.add(dbtiling)
            f.close()
    if tiling in database:
        return VerificationStrategy("Already in database!")
