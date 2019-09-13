from tilings.algorithms import ObstructionTransitivity


def obstruction_transitivity(tiling, **kwargs):
    """The obstruction transitivity strategy.

    The obstruction transitivity considers all length 2 obstructions with both
    points in the same row or some column. By considering these length 2
    obstructions in similar manner as the row and column separation, as
    inequality relations. When the the obstructions use a positive cell,
    transitivity applies, i.e. if a < b < c and b is positive, then a < c.
    """
    obs_trans = ObstructionTransitivity(tiling)
    return obs_trans.rule()
