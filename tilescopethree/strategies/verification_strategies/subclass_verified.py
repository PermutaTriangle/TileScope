"""A strategy for checking if a tiling is contained in a subclass."""

from itertools import chain

from comb_spec_searcher import VerificationRule
from permuta import Av
from permuta.descriptors import Basis


def subclass_verified(tiling, basis, **kwargs):
    """The subclass verified strategy.

    A tiling is subclass verified if it only generates permutations in a
    proper subclass of Av(basis).
    """
    if tiling.dimensions == (1, 1):
        return None
    else:
        maxlen = kwargs.get('maxpattlen', 4)
        patterns = set(perm for perm in chain(*[Av(basis).of_length(i)
                                                for i in range(maxlen + 1)]))
        maxlen += tiling.maximum_length_of_minimum_gridded_perm()
        for i in range(maxlen + 1):
            for g in tiling.objects_of_length(i):
                perm = g.patt
                patterns = set(pattern for pattern in patterns
                               if perm.avoids(pattern))
                if not patterns:
                    return None
        return VerificationRule(formal_step=("The tiling belongs to the "
                                             "subclass obtained by adding"
                                             " the patterns {}."
                                             "".format(Basis(patterns))))
