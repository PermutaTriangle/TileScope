"""The cell insertion strategy checks whether a cell is empty or contains a
point"""

from comb_spec_searcher import BatchStrategy
from permuta import Av


def all_cell_insertions(tiling, **kwargs):
    """
    The cell insertion strategy.

    The cell insertion strategy is a batch strategy that considers each active
    cells, excluding positive cells. For each of these cells, the strategy
    considers all patterns (up to some maximum length given by kwargs) and
    returns two tilings; one which requires the pattern in the cell and one
    where the pattern is obstructed.

    TODO:
        - Have a flag to insert into positive cells that contain the maximal
        intersections
    """
    maxreqlen = kwargs.get('maxreqlen')
    if not maxreqlen:
        maxreqlen = 1

    active = tiling.active_cells
    positive = tiling.positive_cells
    bdict = tiling.cell_basis()
    for length in range(1, maxreqlen + 1):
        for cell in (active - positive):
            for patt in Av(bdict[cell][0]).of_length(length):
                yield BatchStrategy(
                    formal_step="Insert {} into cell {}.".format(patt, cell),
                    tilings=[tiling.add_single_cell_obstruction(patt, cell),
                             tiling.add_single_cell_requirement(patt, cell)])
