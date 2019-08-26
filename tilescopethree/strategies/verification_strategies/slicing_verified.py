from permuta import Perm
from comb_spec_searcher import VerificationRule
from .subset_verified import subset_verified
from .globally_verified import possible_tautology


def slicing_verified(tiling, **kwargs):
    """The globally verified strategy.

    A tiling is slicing verified if every requirement and obstruction that
    crosses slices is 'simple'. Requirments and obstructions within slices
    do not affect this strategy
    """

    def deflation_type(gp):
        patt = gp._patt
        poss = gp._pos
        if patt == Perm((0,2,1)) or patt == Perm((1,2,0)):
            if poss[0][1] == poss[2][1] and poss[1][1] > poss[0][1]:
                return True
        if patt == Perm((1,0,2)) or patt == Perm((2,0,1)):
            if poss[0][1] == poss[2][1] and poss[1][1] < poss[0][1]:
                return True

    if not tiling.dimensions == (1, 1):
        if all(ob.is_single_row() or len(ob) <= 2 or deflation_type(ob) for ob in tiling.obstructions):
            if (all(all((r.is_single_row() or len(r) <= 2) for r in req)
                    for req in tiling.requirements) and
                    not possible_tautology(tiling)):
                return VerificationRule(formal_step="Slicing verified.")
    else:
        return subset_verified(tiling, **kwargs)