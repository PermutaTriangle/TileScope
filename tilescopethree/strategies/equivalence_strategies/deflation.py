"""The deflation strategy."""
from permuta import Perm
from grids_three import Obstruction, Tiling
from comb_spec_searcher import Strategy

def deflation(tiling, **kwargs):
    """Yield all deflation strategies.
    TODO: Think about how this works with requirements."""
    if tiling.requirements:
        return
    bases = tiling.cell_basis()
    for cell in tiling.possibly_empty:
        cell_basis = bases[cell][0]
        if sum_closed(cell_basis): 
            if can_deflate(tiling, cell, True):
                yield Strategy("Sum deflate cell {}.".format(cell),
                            [deflated_tiling(tiling, cell, sum_decomp=True)],
                             inferable=[True], workable=[True], 
                             possibly_empty=[False], ignore_parent=False, 
                             constructor="other")
        if skew_closed(cell_basis):
            if can_deflate(tiling, cell, False):
                yield Strategy("Skew deflate cell {}.".format(cell),
                            [deflated_tiling(tiling, cell, sum_decomp=False)],
                            inferable=[True], workable=[True], 
                            possibly_empty=[False], ignore_parent=False, 
                            constructor="other")

def sum_closed(basis):
    return all(not p.is_sum_decomposable() for p in basis)

def skew_closed(basis):
    return all(not p.is_skew_decomposable() for p in basis)

def can_deflate(tiling, cell, sum_decomp):
    alone_in_row = tiling.only_cell_in_row(cell)
    alone_in_col = tiling.only_cell_in_col(cell)

    if alone_in_row and alone_in_col:
        return False
    
    deflate_patt = Obstruction.single_cell(Perm((1, 0)) if sum_decomp
                                           else Perm((0, 1)), cell)

    # we must be sure that no cell in a row or column can interleave 
    # with any reinflated components, so collect cells that do not.
    cells_not_interleaving = set([cell])
    
    for ob in tiling.obstructions:
        if ob == deflate_patt:
            print("1")
            return False
        if ob.is_single_cell() or not ob.occupies(cell):
            continue
        number_points_in_cell = sum(1 for c in ob.pos if c == cell)
        if number_points_in_cell == 1:
            if len(ob) == 2:
                # not interleaving with cell as separating if 
                # in same row or column
                other_cell = [c for c in ob.pos if c != cell][0]
                cells_not_interleaving.add(other_cell)
        elif number_points_in_cell == 2:
            if len(ob) != 3:
                print(2)
                return False
            patt_in_cell = ob.get_gridded_perm_in_cells((cell, ))
            if patt_in_cell != deflate_patt:
                # you can interleave with components
                print(3)
                return False
            # we need the other cell to be in between the intended deflate 
            # patt in either the row or column
            other_cell = [c for c in ob.pos if c != cell][0]
            if (point_in_between(ob, True, cell, other_cell) or 
                point_in_between(ob, False, cell, other_cell)):
                # this cell does not interleave with inflated components
                cells_not_interleaving.add(other_cell)
            else:
                print(4)
                return False
        elif number_points_in_cell >= 3:
            # you can interleave with components
            print(5)
            return False
    # check that do not interleave with any cells in row or column.
    if (cells_not_interleaving >= tiling.cells_in_row(cell[1]) and
            cells_not_interleaving >= tiling.cells_in_col(cell[0])):
        print(cell)
        print(tiling.to_old_tiling())
        print(repr(tiling))
        print()
    print(6)
    return (cells_not_interleaving >= tiling.cells_in_row(cell[1]) and
            cells_not_interleaving >= tiling.cells_in_col(cell[0]))
            



# def can_deflate(tiling, cell, sum_decomp):
#     """Return True if can deflate cell, else False."""
#     row = tiling.only_cell_in_col(cell)
#     col = tiling.only_cell_in_row(cell)
#     if not row and not col:
#         return False
#     deflating = set()
#     sumpatt = Obstruction.single_cell(Perm((1, 0)) if sum_decomp
#                                       else Perm((0, 1)), cell)
#     for ob in tiling.obstructions:
#         if ob == sumpatt:
#             return False
#         if ob.is_single_cell() or not ob.occupies(cell):
#             continue
#         if len(ob) == 2:
#             other_cell = [c for c in ob.pos if c != cell][0]
#             deflating.add(other_cell)
#             continue
#         n = sum(1 for c in ob.pos if c == cell)
#         if n == 1:
#             continue
#         if n > 2 or len(ob) > 3:
#             if sum(1 for c in ob.pos if c != cell) != 1:
#                 return False
#         other_cell = [c for c in ob.pos if c != cell][0]
#         if ((row and other_cell[1] != cell[1]) or
#                 (col and other_cell[0] != cell[0])):
#             return False
#         if ob.patt.is_decreasing() or ob.patt.is_increasing():
#             continue
#         patt_in_cell = Perm.to_standard([x for x, y in zip(ob.patt, ob.pos)
#                                          if y == cell])
#         if ((sum_decomp and patt_in_cell == Perm((1, 0))) or
#                 (not sum_decomp and patt_in_cell == Perm((0, 1)))):
#             if point_in_between(ob, row, cell, other_cell):
#                 deflating.add(other_cell)
#     return ((not col or deflating >= set(tiling.cells_in_col(cell[0]))) 
#             and (not row or deflating >= set(tiling.cells_in_row(cell[1]))))

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
