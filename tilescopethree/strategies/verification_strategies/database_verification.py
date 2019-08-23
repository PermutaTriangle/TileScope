"""A strategy for checking if a tiling is a subset of the class."""
import os
from base64 import b64decode, b64encode

from logzero import logger

from comb_spec_searcher import VerificationRule
from tilings import Tiling

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
        return VerificationRule("Already in database!")
