"""A strategy for checking if a tiling is a subset of the class."""

from comb_spec_searcher import VerificationStrategy
from permuta.descriptors import Basis
from permuta.permutils import all_symmetry_sets


def subset_verified(tiling, basis, **kwargs):
    """The subset verified strategy.

    A tiling is subset verified if every obstruction and every requirement is
    localized.
    """
    if kwargs.get("no_factors", False):
        if len(tiling.find_factors()) > 1:
            return
    if tiling.dimensions == (1, 1):
        if one_by_one_verified(tiling, basis, **kwargs):
            return VerificationStrategy(
                formal_step="The tiling is a subset of the class.")
    elif (all(ob.is_single_cell() for ob in tiling.obstructions) and
          all(all(r.is_single_cell() for r in req)
              for req in tiling.requirements)):
            return VerificationStrategy(
                formal_step="The tiling is a subset of the class.")


def one_by_one_verified(tiling, basis, **kwargs):
    """Return true if tiling is a subset of the Av(basis)."""
    if basis is None or tiling.dimensions != (1, 1):
        return False
    rootbasis = [ob.patt for ob in tiling.obstructions]
    if kwargs.get('symmetry'):
        all_patts = [Basis(sym_set)
                     for sym_set in all_symmetry_sets(rootbasis)]
    else:
        all_patts = [Basis(rootbasis)]
    if any(basis == patts for patts in all_patts):
        return False
    return True


def one_by_one_verification(tiling, basis, **kwargs):
    """Return a verification if one-by-one verified."""
    if one_by_one_verified(tiling, basis, **kwargs):
        return VerificationStrategy(
                        formal_step="The tiling is a subclass of the class.")
