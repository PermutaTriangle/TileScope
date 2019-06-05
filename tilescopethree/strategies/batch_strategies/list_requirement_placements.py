from itertools import chain

from comb_spec_searcher import Rule
from permuta import Perm
from permuta.misc import DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST
from tilings import Obstruction, Requirement, Tiling


def requirement_list_placement(tiling, **kwargs):
    """Places all requirements on the tiling in every direction."""
    for req in tiling.requirements:
        for direction in [DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST]:
            tilings = place_requirement_list(tiling, req, direction)
            if tilings is None:
                continue
            yield Rule(
                        formal_step=("Place requirement {} in direction {}."
                                     "".format(req, direction)),
                        comb_classes=tilings,
                        ignore_parent=False,
                        possibly_empty=[True for _ in tilings],
                        inferable=[True for _ in tilings],
                        workable=[True for _ in tilings],
                        constructor='disjoint')


def row_placements(tiling, row=True, positive=True, **kwargs):
    """Places the points in a row (or col if row=False) in the given
    direction."""
    if row:
        x = tiling.dimensions[1]
        y = tiling.dimensions[0]
        only_cell_in_col = tiling.only_cell_in_col
        directions = [DIR_NORTH, DIR_SOUTH]
    else:
        x = tiling.dimensions[0]
        y = tiling.dimensions[1]
        only_cell_in_col = tiling.only_cell_in_row
        directions = [DIR_EAST, DIR_WEST]
    direction = kwargs.get('direction')
    if direction is not None:
        if row:
            if direction == DIR_NORTH:
                directions = [DIR_NORTH]
            elif direction == DIR_SOUTH:
                directions = [DIR_SOUTH]
            else:
                raise ValueError("Can't place rows in direction.")
        else:
            if direction == DIR_EAST:
                directions = [DIR_EAST]
            elif direction == DIR_WEST:
                directions = [DIR_WEST]
            else:
                raise ValueError("Can't place cols in direction.")
    for i in range(x):
        place = True
        cells_in_row = []
        for j in range(y):
            cell = (j, i) if row else (i, j)
            if positive and cell not in tiling.positive_cells:
                place = False
                break
            cells_in_row.append(cell)
        if place:
            if (len(cells_in_row) != 1 or
                not cells_in_row[0] in tiling.point_cells or
                    not only_cell_in_col(cells_in_row[0])):
                req_list = tuple(Requirement(Perm((0,)), (cell,))
                                 for cell in cells_in_row)
                if not positive:
                    """Adding the empty row case."""
                    empty_row_tiling = Tiling(tiling.obstructions +
                                              tuple(Obstruction(Perm((0,)),
                                                                (cell,))
                                                    for cell in cells_in_row),
                                              tiling.requirements)
                for direction in directions:
                    tilings = place_requirement_list(tiling, req_list,
                                                     direction)
                    if not positive:
                        tilings = [empty_row_tiling] + tilings
                    yield Rule(
                        formal_step=("Placing {} {} in direction {}."
                                     "".format("row" if row else "col",
                                               i, direction)),
                        comb_classes=tilings,
                        ignore_parent=False,
                        possibly_empty=[True for _ in tilings],
                        inferable=[True for _ in tilings],
                        workable=[True for _ in tilings],
                        constructor='disjoint')


def col_placements(tiling, **kwargs):
    yield from row_placements(tiling, row=False, **kwargs)


def place_requirement_list(tiling, req_list, direction):
    """Return the list of tilings obtained by placing the direction-most point
    of a requirement list. This represents a batch strategy, where the
    direction-most point of each requirement in the list is placed."""
    # Compute the points furthest in the given direction.
    min_points = minimum_points(req_list, direction)
    if len([c for _, c in min_points]) != len(set([c for _, c in min_points])):
        # Can't handle list requirements with more than req farthest in the
        # direction in same cell.
        return None
    # For each tiling, compute the tiling where this point is placed furthest
    # in that direction.
    res = []
    for (idx, cell), req in zip(min_points, req_list):
        # Placing the forced occurrence of the point in the requirement
        new_req, forced_obstructions = req.place_forced_point(idx, direction)
        assert len(new_req) == 1
        # Add the forced obstruction to ensure no other requirement has a point
        # further in that direction.
        forced_obstructions = (forced_obstructions +
                               list(chain.from_iterable(
                                     r.other_req_forced_point(cell, direction)
                                    for r in req_list if r != req)))
        # New indices of the point
        point_cell = (cell[0] + 1, cell[1] + 1)
        # The set of new obstructions, consisting of the forced obstructions,
        # other obstructions where the point placement has been taken into
        # account and the 12, 21 in the cell.
        newobs = forced_obstructions + list(chain.from_iterable(
            ob.place_point(cell, DIR_NONE) for ob in tiling.obstructions)) + [
                Obstruction.single_cell(Perm((0, 1)), point_cell),
                Obstruction.single_cell(Perm((1, 0)), point_cell)]
        # The rest of the requirements
        other_reqs = [reqs for reqs in tiling.requirements if reqs != req_list]
        # The new requirements, consisting of the requirement with the point
        # placed, other requirements where point placement has been taken into
        # account and the point requirement in the cell.
        newreqs = [list(chain.from_iterable(r.place_point(cell, DIR_NONE)
                                            for r in reqs))
                   for reqs in other_reqs] + [new_req] + [
                        [Requirement.single_cell(Perm((0,)), point_cell)]]
        res.append(Tiling(newobs, newreqs))
    return res


def minimum_points(req_list, direction):
    """Return a list of tuple containing the index and cell of the point in the
     requirement furthest to the geiven direction."""
    res = []
    if direction == DIR_WEST:
        res = [(0, req.pos[0]) for req in req_list]
    elif direction == DIR_EAST:
        res = [(len(req) - 1, req.pos[-1]) for req in req_list]
    elif direction == DIR_SOUTH:
        for req in req_list:
            mindex = req.patt.index(0)
            res.append((mindex, req.pos[mindex]))
    elif direction == DIR_NORTH:
        for req in req_list:
            maxdex = req.patt.index(0)
            res.append((maxdex, req.pos[maxdex]))
    else:
        raise ValueError("Must choose north, south, east or west.")

    return res
