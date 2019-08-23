"""A strategy for checking if a tiling only has obstructions of length at most two."""

from comb_spec_searcher import VerificationRule

def verify_short_obstructions(tiling, **kwargs):
    """
    A tiling is verified if it only has obstructions of length at most two.
    """
    if tiling.dimensions == (1, 1):
        return None
    else:
        if all(len(obs)<3 for obs in tiling.obstructions):
            return VerificationRule(formal_step=("The tiling only has obstructions of length at most two."))
