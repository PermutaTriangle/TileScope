"""A strategy for checking if a tiling is a subset of the class."""

from comb_spec_searcher import VerificationStrategy
from permuta.descriptors import Basis
from permuta import Av
from copy import copy
from grids_three import Tiling

# TODO Memoize the patterns
def subclass_verified(tiling, basis, **kwargs):
    """The subclass verified strategy.

    A tiling is subclass verified if it only generates permutations in a
    proper subclass of Av(basis).
    """

    if tiling.dimensions == (1, 1):
        return None

    else:
        patterns = set(perm for perm in Av(basis).of_length(3)) | set(perm for perm in Av(basis).of_length(4)) # <------------------------ hardcoded!
        for i in range(tiling.maximum_length_of_minimum_gridded_perm()+4+1): # <------------------------ hardcoded!
            for g in tiling.objects_of_length(i):
                p = g.patt
                patterns = set(pattern for pattern in patterns if p.avoids(pattern))
                if not patterns:
                    return None

        return VerificationStrategy(
            formal_step="The tiling belongs to the subclass obtained by adding the patterns {}".format(Basis(patterns))
        )
