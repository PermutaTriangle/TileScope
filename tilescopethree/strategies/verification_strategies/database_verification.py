"""A strategy for checking if a tiling is a subset of the class."""
from base64 import b64decode, b64encode
from comb_spec_searcher import VerificationStrategy
from grids_three import Tiling, Obstruction, Requirement
from permuta import Perm


database = set()
filenames = ["012_depth_4_database.txt"]
for filename in filenames:
    f = open(filename, 'r')
    for line in f:
       compression = b64decode(line.encode())
       tiling = Tiling.decompress(compression)
       database.add(tiling)

def database_verified(tiling, **kwargs):
    if tiling in database:
       return VerificationStrategy("Already in database!")
