from comb_spec_searcher import VerificationStrategy
from .subset_verified import subset_verified


def globally_verified(tiling, **kwargs):
    """The globally verified strategy.

    A tiling is globally verified if every requirement and obstruction is
    non-interleaving.
    """
    if not tiling.dimensions == (1, 1):
        if all(not ob.is_interleaving() for ob in tiling.obstructions):
            if (all(all(not r.is_interleaving() for r in req)
                    for req in tiling.requirements) and
                    not possible_tautology(tiling)):
                return VerificationStrategy(formal_step="Globally verified.")
    else:
        return subset_verified(tiling, **kwargs)


def possible_tautology(tiling):
    """Return True if possibly equivalent to a 1x1 tiling through empty cell
    inferral. (It just checks if two cells are non-empty - nothing exciting)"""
    if len(tiling.positive_cells) > 1:
        return False
    cells = set()
    for gp in tiling.gridded_perms():
        cells.update(gp.pos)
        if len(cells) > 1:
            return False
    return True

def elementary_verified(tiling, **kwargs):
    """A tiling is elementary verified if it is globally verified and has no
    interleaving cells."""
    if tiling.fully_isolated():
        if tiling.dimensions == (1, 1):
            return subset_verified(tiling, **kwargs)
        return globally_verified(tiling, **kwargs)
