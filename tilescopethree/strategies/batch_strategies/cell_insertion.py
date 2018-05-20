"""The cell insertion strategy checks whether a cell is empty or contains a
point"""

from comb_spec_searcher import Strategy
from permuta import Av, Perm


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
    extra_basis = kwargs.get('extra_basis')
    if extra_basis is None:
        extra_basis = []
    if (not isinstance(extra_basis, list) or
            not all(isinstance(p, Perm) for p in extra_basis)):
        raise TypeError("'extra_basis' flag should be a list of Perm to avoid")

    active = tiling.active_cells
    positive = tiling.positive_cells
    bdict = tiling.cell_basis()
    for cell in (active - positive):
        for length in range(1, maxreqlen + 1):
            for patt in Av(bdict[cell][0] + extra_basis).of_length(length):
                yield Strategy(
                    formal_step="Insert {} into cell {}.".format(patt, cell),
                    comb_classes=[
                            tiling.add_single_cell_obstruction(patt, cell),
                            tiling.add_single_cell_requirement(patt, cell)],
                    ignore_parent=False,
                    inferable=[True for _ in range(2)],
                    workable=[True for _ in range(2)],
                    constructor='disjoint')


def root_requirement_insertion(tiling, **kwargs):
    """The cell insertion strategy performed only on 1 by 1 tilings."""
    if tiling.dimensions != (1, 1) or tiling.requirements != []:
        return
    yield from all_cell_insertions(tiling, **kwargs)


def all_point_insertions(tiling, **kwargs):
    """The cell insertion strategy using only points."""
    yield from all_cell_insertions(tiling, maxreqlen=1, **kwargs)


def all_requirement_extensions(tiling, **kwargs):
    """Insert longer requirements in to cells which contain a requirement"""
    maxreqlen = kwargs.get('maxreqlen')
    if not maxreqlen:
        maxreqlen = 2
    extra_basis = kwargs.get('extra_basis')
    if extra_basis is None:
        extra_basis = []
    if (not isinstance(extra_basis, list) or
            not all(isinstance(p, Perm) for p in extra_basis)):
        raise TypeError("'extra_basis' flag should be a list of Perm to avoid")

    active = tiling.active_cells
    bdict = tiling.cell_basis()
    for cell in active:
        basis = bdict[cell][0]
        reqs = bdict[cell][1]
        if len(reqs) != 1:
            continue
        curr_req = reqs[0]
        for length in range(len(curr_req) + 1, maxreqlen + 1):
            for patt in Av(bdict[cell][0] + extra_basis).of_length(length):
                if curr_req in patt:
                    yield Strategy(
                        formal_step=("Insert {} into cell {}."
                                     "".format(patt, cell)),
                        comb_classes=[
                            tiling.add_single_cell_obstruction(patt, cell),
                            tiling.add_single_cell_requirement(patt, cell)],
                        ignore_parent=False,
                        inferable=[True for _ in range(2)],
                        workable=[True for _ in range(2)],
                        constructor='disjoint')
