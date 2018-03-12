from comb_spec_searcher import VerificationStrategy


def globally_verified(tiling, **kwargs):
    """The globally verified strategy.

    A tiling is globally verified if every requirement and obstruction is
    non-interleaving.
    """
    if not tiling.dimensions == (1, 1):
        if all(not ob.is_interleaving() for ob in tiling.obstructions):
            if all(all(not r.is_interleaving() for r in req)
                   for req in tiling.requirements):
                return VerificationStrategy(formal_step="Globally verified.")
