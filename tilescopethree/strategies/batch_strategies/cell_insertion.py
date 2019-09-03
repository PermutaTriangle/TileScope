"""The cell insertion strategy checks whether a cell is empty or contains a
point"""

from itertools import chain

from comb_spec_searcher import Rule
from permuta import Av, Perm
from tilings import Obstruction, Requirement, Tiling


def all_cell_insertions(tiling, **kwargs):
    """
    The cell insertion strategy.

    The cell insertion strategy is a batch strategy that considers each active
    cells, excluding positive cells. For each of these cells, the strategy
    considers all patterns (up to some maximum length given by maxreqlen, and
    some maximum number given by maxreqnum) and returns two tilings; one which
    requires the pattern in the cell and one where the pattern is obstructed.

    TODO:
        - Have a flag to insert into positive cells that contain the maximal
        intersections
    """
    maxreqlen = kwargs.get('maxreqlen')
    if not maxreqlen:
        maxreqlen = 1
    ignore_parent = kwargs.get('ignore_parent', False)
    extra_basis = kwargs.get('extra_basis')
    if extra_basis is None:
        extra_basis = []
    if (not isinstance(extra_basis, list) or
            not all(isinstance(p, Perm) for p in extra_basis)):
        raise TypeError("'extra_basis' flag should be a list of Perm to avoid")
    maxreqnum = kwargs.get('maxreqnum')
    if not maxreqnum:
        maxreqnum = 1

    active = tiling.active_cells
    bdict = tiling.cell_basis()
    for cell in active:
        if len(bdict[cell][1]) >= maxreqnum:
            continue
        for length in range(1, maxreqlen + 1):
            for patt in Av(bdict[cell][0] + extra_basis).of_length(length):
                if not any(patt in perm for perm in bdict[cell][1]):
                    if (tiling.dimensions != (1, 1) or
                            all(patt > perm for perm in bdict[cell][1])):
                        yield Rule(
                            formal_step=("Insert {} into cell {}.|{}|{}|{}|"
                                         "".format(patt, cell, cell[0],
                                                   cell[1],
                                                   "".join(str(i)
                                                           for i in patt))),
                            comb_classes=cell_insertion(tiling, patt, cell),
                            ignore_parent=ignore_parent,
                            inferable=[True for _ in range(2)],
                            possibly_empty=[True for _ in range(2)],
                            workable=[True for _ in range(2)],
                            constructor='disjoint')

def cell_insertion(tiling, patt, cell, regions=False):
    """Return a tuple, the first avoids pattern in the cell, and the second
    contains it."""
    if regions:
        return ([tiling.add_single_cell_obstruction(patt, cell),
                 tiling.add_single_cell_requirement(patt, cell)],
                [{c: frozenset([c]) for c in tiling.active_cells},
                 {c: frozenset([c]) for c in tiling.active_cells}])
    else:
        return [tiling.add_single_cell_obstruction(patt, cell),
                tiling.add_single_cell_requirement(patt, cell)]



def cell_insertion(tiling, patt, cell, regions=False):
    """Return a tuple, the first avoids pattern in the cell, and the second
    contains it."""
    if regions:
        return ([tiling.add_single_cell_obstruction(patt, cell),
                 tiling.add_single_cell_requirement(patt, cell)],
                [{c: frozenset([c]) for c in tiling.active_cells},
                 {c: frozenset([c]) for c in tiling.active_cells}])
    else:
        return [tiling.add_single_cell_obstruction(patt, cell),
                tiling.add_single_cell_requirement(patt, cell)]


def root_requirement_insertion(tiling, **kwargs):
    """The cell insertion strategy performed only on 1 by 1 tilings."""
    if tiling.dimensions != (1, 1):
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
                    yield Rule(
                        formal_step=("Insert {} into cell {}."
                                     "".format(patt, cell)),
                        comb_classes=[
                            tiling.add_single_cell_obstruction(patt, cell),
                            tiling.add_single_cell_requirement(patt, cell)],
                        ignore_parent=False,
                        possibly_empty=[any(len(r) > 1
                                            for r in tiling.requirements),
                                        True],
                        inferable=[True for _ in range(2)],
                        workable=[True for _ in range(2)],
                        constructor='disjoint')


def all_row_insertions(tiling, **kwargs):
    """Insert a list requirement into every possibly empty row."""
    positive_cells = tiling.positive_cells
    for row in range(tiling.dimensions[1]):
        row_cells = tiling.cells_in_row(row)
        if any(c in positive_cells for c in row_cells):
            continue
        yield Rule(
                    formal_step="Either row {} is empty or not.".format(row),
                    comb_classes=row_insertion_helper(tiling, row, row_cells),
                    ignore_parent=False,
                    inferable=[True for _ in range(2)],
                    possibly_empty=[True,
                                    True],
                    workable=[True for _ in range(2)],
                    constructor='disjoint')


def row_insertion_helper(tiling, row, row_cells, regions=False):
    if row_cells is None:
        row_cells = tiling.cells_in_row(row)
    row_req = tuple(Requirement.single_cell(Perm((0, )), c)
                    for c in row_cells)
    row_obs = tuple(Obstruction.single_cell(Perm((0, )), c)
                    for c in row_cells)
    if regions:
        return ([Tiling(tiling.obstructions + row_obs, tiling.requirements),
                Tiling(tiling.obstructions, tiling.requirements + (row_req,))],
                [{c: frozenset([c]) for c in tiling.active_cells},
                 {c: frozenset([c]) for c in tiling.active_cells}])
    else:
        return [Tiling(tiling.obstructions + row_obs, tiling.requirements),
                Tiling(tiling.obstructions, tiling.requirements + (row_req,))]


def all_col_insertions(tiling, **kwargs):
    """Insert a list requirement into every possibly empty column."""
    positive_cells = tiling.positive_cells
    for col in range(tiling.dimensions[0]):
        col_cells = tiling.cells_in_col(col)
        if any(c in positive_cells for c in col_cells):
            continue
        yield Rule(
                    formal_step="Either col {} is empty or not.".format(col),
                    comb_classes=col_insertion_helper(tiling, col, col_cells),
                    ignore_parent=False,
                    inferable=[True for _ in range(2)],
                    possibly_empty=[True,
                                    True],
                    workable=[True for _ in range(2)],
                    constructor='disjoint')


def col_insertion_helper(tiling, col, col_cells, regions=False):
    if col_cells is None:
        col_cells = tiling.cells_in_col(col)
    col_req = tuple(Requirement.single_cell(Perm((0, )), c)
                    for c in col_cells)
    col_obs = tuple(Obstruction.single_cell(Perm((0, )), c)
                    for c in col_cells)
    if regions:
        return ([Tiling(tiling.obstructions + col_obs,
                        tiling.requirements),
                 Tiling(tiling.obstructions,
                        tiling.requirements + (col_req,))],
                [{c: frozenset([c]) for c in tiling.active_cells},
                 {c: frozenset([c]) for c in tiling.active_cells}])
    else:
        return [Tiling(tiling.obstructions + col_obs,
                       tiling.requirements),
                Tiling(tiling.obstructions,
                       tiling.requirements + (col_req,))]


def all_requirement_insertions(tiling, **kwargs):
    """Insert all possible requirements the obstruction allow."""
    if kwargs.get("no_reqs", True) and tiling.requirements:
        return
    maxlen = kwargs.get("maxlen", 2)
    ignore_parent = kwargs.get("ignore_parent", False)
    obs_tiling = Tiling(tiling.obstructions,
                        remove_empty=False, derive_empty=False,
                        minimize=False, sorted_input=True)
    for length in range(1, maxlen + 1):
        for gp in obs_tiling.gridded_perms_of_length(length):
            if len(gp.factors()) == 1:
                av = Tiling((tiling.obstructions +
                            (Obstruction(gp.patt, gp.pos),)),
                            tiling.requirements)
                co = Tiling(tiling.obstructions,
                            (tiling.requirements) +
                            ((Requirement(gp.patt, gp.pos),),))
                yield Rule(formal_step="Insert {}.".format(str(gp)),
                           comb_classes=[av, co],
                           ignore_parent=ignore_parent,
                           inferable=[True for _ in range(2)],
                           possibly_empty=[True for _ in range(2)],
                           workable=[True for _ in range(2)],
                           constructor='disjoint')


def all_factor_insertions(tiling, **kwargs):
    ignore_parent = kwargs.get("ignore_parent", False)
    for gp in sorted(set(chain(tiling.obstructions, *tiling.requirements))):
        factors = gp.factors()
        if len(factors) != 1:
            for gp in factors:
                av = Tiling((tiling.obstructions +
                            (Obstruction(gp.patt, gp.pos),)),
                            tiling.requirements)
                co = Tiling(tiling.obstructions,
                            (tiling.requirements) +
                            ((Requirement(gp.patt, gp.pos),),))
                yield Rule(formal_step="Insert {}.".format(str(gp)),
                           comb_classes=[av, co],
                           ignore_parent=ignore_parent,
                           inferable=[True for _ in range(2)],
                           possibly_empty=[True for _ in range(2)],
                           workable=[True for _ in range(2)],
                           constructor='disjoint')
