from tilescopethree.strategies.batch_strategies.point_placements import \
    place_point_of_requirement
from permuta.misc import DIR_WEST
from comb_spec_searcher import EquivalenceStrategy


def point_isolations(tiling, **kwargs):
    point_cells = tiling.point_cells
    for ri, reqs in enumerate(tiling.requirements):
        if len(reqs) > 1:
            continue
        cell = reqs[0].is_point_perm()
        if cell is None or cell not in point_cells:
            continue
        yield EquivalenceStrategy(
            formal_step=("Isolating point at {} into its own row and "
                         "column").format(cell),
            # Direction does not matter
            comb_class=place_point_of_requirement(tiling, ri, 0, DIR_WEST))
