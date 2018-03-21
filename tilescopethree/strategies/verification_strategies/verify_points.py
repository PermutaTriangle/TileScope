"""A strategy for checking if a tiling is a point."""

from comb_spec_searcher import VerificationStrategy


def verify_points(tiling, basis, **kwargs):
    """The verify points strategy.

    A tiling is verified only if it is a point.
    """
    if (tiling.dimensions == (1, 1)
            and len(tiling.obstructions) == 2
            and all(len(ob) == 2 for ob in tiling.obstructions)
            and len(tiling.requirements) == 1
            and len(tiling.requirements[0]) == 1
            and len(tiling.requirements[0][0]) == 1):
        return VerificationStrategy(
                    formal_step="I understand points, no really, I do.")
