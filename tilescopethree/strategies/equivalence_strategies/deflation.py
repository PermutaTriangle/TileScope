"""The deflation strategy."""
from permuta import Perm
from grids_three import Obstruction, Tiling
from comb_spec_searcher import Strategy

def deflation(tiling, **kwargs):
    """Yield all deflation strategies.
    TODO: Think about how this works with requirements."""
    if tiling.requirements:
        return
    for cell in tiling.possibly_empty:
        if can_deflate(tiling, cell, True):
            yield Strategy("Sum deflate cell {}.".format(cell),
                           [deflated_tiling(tiling, cell, sum_decomp=True)],
                           inferable=[True], workable=[True],
                           ignore_parent=True, constructor="other")
        if can_deflate(tiling, cell, False):
            yield Strategy("Skew deflate cell {}.".format(cell),
                           [deflated_tiling(tiling, cell, sum_decomp=False)],
                           inferable=[True], workable=[True],
                           ignore_parent=True, constructor="other")

def can_deflate(tiling, cell, sum_decomp):
    """Return True if can deflate cell, else False."""
    row = tiling.only_cell_in_col(cell)
    col = tiling.only_cell_in_row(cell)
    if not row and not col:
        return False
    deflating = False
    sumpatt = Obstruction.single_cell(Perm((1, 0)) if sum_decomp
                                      else Perm((0, 1)), cell)
    for ob in tiling.obstructions:
        if ob == sumpatt:
            return False
        if ob.is_single_cell() or len(ob) <= 2 or not ob.occupies(cell):
            continue
        n = sum(1 for c in ob.pos if c == cell)
        if n == 1:
            continue
        if n != 2 or len(ob) > 3:
            if sum(1 for c in ob.pos if c != cell) != 1:
                return False
        other_cell = [c for c in ob.pos if c != cell][0]
        if ((row and other_cell[1] != cell[1]) or
                (not row and other_cell[0] != cell[0])):
            return False
        if ob.patt.is_decreasing() or ob.patt.is_increasing():
            continue
        patt_in_cell = Perm.to_standard([x for x, y in zip(ob.patt, ob.pos)
                                         if y == cell])
        if ((sum_decomp and patt_in_cell == Perm((1, 0))) or
                (not sum_decomp and patt_in_cell == Perm((0, 1)))):
            if point_in_between(ob, row, cell, other_cell):
                return True
    return deflating

def point_in_between(ob, row, cell, other_cell):
    """Return true if point in other cell is in between point in cell.
    Assumes a length 3 pattern, and to be told if row or column."""
    if row:
        left = other_cell[0] < cell[0]
        if left:
            return ob.patt[0] == 1
        else:
            return ob.patt[2] == 1
    below = other_cell[1] < cell[1]
    if below:
        return ob.patt[1] == 0
    else:
        return ob.patt[1] == 2


def deflated_tiling(tiling, cell, sum_decomp=True):
    """Return tiling where cell is deflated."""
    if sum_decomp:
        extra = Obstruction.single_cell(Perm((1, 0)), cell)
    else:
        extra = Obstruction.single_cell(Perm((0, 1)), cell)
    return Tiling(requirements=tiling.requirements,
                  obstructions=tiling.obstructions + (extra, ))
