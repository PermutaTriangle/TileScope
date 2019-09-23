from comb_spec_searcher import EquivalenceRule
from permuta.misc import DIR_WEST
from tilings.algorithms import RequirementPlacement


def point_isolations(tiling, **kwargs):
    req_placement = RequirementPlacement(tiling)
    for cell in tiling.point_cells:
        if not tiling.only_cell_in_row_and_col():
            isolated_tiling = req_placement.place_point_in_cell(cell, DIR_WEST)
            yield EquivalenceRule("Isolate point at cell {}.".format(cell),
                                isolated_tiling)