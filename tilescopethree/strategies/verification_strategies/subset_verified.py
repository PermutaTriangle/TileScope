"""A strategy for checking if a tiling is a subset of the class."""

from comb_spec_searcher import VerificationRule
from permuta import Perm
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
            return VerificationRule(
                formal_step="The tiling is a subset of the class.")
    elif (all(ob.is_single_cell() for ob in tiling.obstructions) and
          all(all(r.is_single_cell() for r in req)
              for req in tiling.requirements)):
            return VerificationRule(
                formal_step="The tiling is a subset of the class.")

def subset_verified_no_req(tiling, basis, **kwargs):
    """The subset verified strategy.

    A tiling is subset verified if every obstruction and every requirement is
    localized, and every requirement is a point that is placed.
    """
    if kwargs.get("no_factors", False):
        if len(tiling.find_factors()) > 1:
            return
    if tiling.dimensions == (1, 1):
        if one_by_one_verified(tiling, basis, **kwargs):
            return VerificationRule(
                formal_step="The tiling is a subset of the class.")
    elif (all(ob.is_single_cell() for ob in tiling.obstructions) and
          all(all(r.is_single_cell() for r in req)
              for req in tiling.requirements)):
            
            for req in tiling.requirements:
                # No requirement lists allowed
                if len(req) > 1:
                    return
                r = req[0]
                # Only point requirements allowed
                if len(r) > 1:
                    return
                if not(Perm((0,1)) in tiling.cell_basis()[r._pos[0]][0] and Perm((1,0)) in tiling.cell_basis()[r._pos[0]][0]):
                    return
            return VerificationRule(formal_step="The tiling is a subset of the class no req.")
            


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
        return VerificationRule(
                        formal_step="The tiling is a subclass of the class.")
