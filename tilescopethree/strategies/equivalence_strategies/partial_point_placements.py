from itertools import chain

from comb_spec_searcher import EquivalenceStrategy
from tilings import Obstruction, Requirement, Tiling
from permuta import Perm
from permuta.misc import (DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST,
                          DIRS)


def opposite_dir(DIR):
    if DIR == DIR_WEST:
        return DIR_EAST
    if DIR == DIR_EAST:
        return DIR_WEST
    if DIR == DIR_NORTH:
        return DIR_SOUTH
    if DIR == DIR_SOUTH:
        return DIR_NORTH
    return DIR_NONE


def partial_place_point_of_requirement(tiling, req_index, point_index,
                                       force_dir):
    """
    Places the point at point_index in requirement at req_index into tiling on
    its own row or onto its own column depending on force_dir.
    """
    if len(tiling.requirements[req_index]) > 1:
        raise ValueError(
            "Requirement list at {} contains more than 1 requirement.".format(
                req_index))
    # Determine if placing onto own row or column
    row = (force_dir == DIR_NORTH or force_dir == DIR_SOUTH)
    # The requirement
    requirement = tiling.requirements[req_index][0]
    # The cell containing the point
    cell = requirement.pos[point_index]
    # The rest of the requirements
    other_reqs = [tiling.requirements[i]
                  for i in range(len(tiling.requirements))
                  if i != req_index]
    # Placing the forced occurrence of the point in the requirement
    new_req, forced_obstructions = requirement.partial_place_forced_point(
                                                    point_index, force_dir)
    assert len(new_req) == 1
    # New indices of the point.
    point_cell = (cell[0] if row else cell[0] + 1,
                  cell[1] + 1 if row else cell[1])
    # The set of new obstructions, consisting of the forced obstructions, other
    # obstructions where the point placement has been taken into account and
    # the 12, 21 in the cell.
    newobs = forced_obstructions + list(chain.from_iterable(
                    ob.place_point(cell, DIR_NONE, partial=True, row=row)
                    for ob in tiling.obstructions)) + [
            Obstruction.single_cell(Perm((0, 1)), point_cell),
            Obstruction.single_cell(Perm((1, 0)), point_cell)]
    # If a point cell, make sure neighbouring cells are empty by adding the
    # point obstructions.
    if cell in tiling.point_cells:
        if force_dir == DIR_EAST or force_dir == DIR_WEST:
            newobs = (newobs +
                      [Obstruction.single_cell(
                            Perm((0,)), (point_cell[0] + 1, point_cell[1])),
                       Obstruction.single_cell(
                            Perm((0,)), (point_cell[0] - 1, point_cell[1]))])
        elif force_dir == DIR_NORTH or force_dir == DIR_SOUTH:
            newobs = (newobs +
                      [Obstruction.single_cell(
                            Perm((0,)), (point_cell[0], point_cell[1] + 1)),
                       Obstruction.single_cell(
                            Perm((0,)), (point_cell[0], point_cell[1] - 1))])
    # The new requirements, consisting of the requirement with the point
    # placed, other requirements where point placement has been taken into
    # account and the point requirement in the cell.
    newreqs = [list(chain.from_iterable(req.place_point(cell, DIR_NONE,
                                                        partial=True, row=row)
                                        for req in reqs))
               for reqs in other_reqs] + [new_req] + [
                       [Requirement.single_cell(Perm((0,)), point_cell)]]
    return Tiling(obstructions=newobs, requirements=newreqs)


def partial_requirement_placement(tiling, **kwargs):
    """
    Strategy that places a single forced point of a requirement onto it own row
    or onto its own column.

    The partial_requirement_placement strategy considers every requirement list
    of length exactly 1. For each of these requirements, it considers all the
    points of the requirement. The strategy then returns all tilings where the
    point has been partially placed with a force.
    """
    point_cells = tiling.point_cells
    point_only = kwargs.get('point_only')
    for ri, reqs in enumerate(tiling.requirements):
        if len(reqs) > 1:
            continue
        if reqs[0].is_point_perm() in point_cells:
            cell = reqs[0].pos[0]
            directions = []
            if not tiling.only_cell_in_row(cell):
                directions.extend((DIR_NORTH, DIR_SOUTH))
            if not tiling.only_cell_in_col(cell):
                directions.extend((DIR_EAST, DIR_WEST))
        else:
            directions = DIRS
        if point_only and reqs[0].is_point_perm() is None:
            continue
        for i in range(len(reqs[0])):
            for DIR in directions:
                placedtiling = partial_place_point_of_requirement(
                                                        tiling, ri, i, DIR)
                yield EquivalenceStrategy(
                    formal_step=("Partially placing point {} of requirement {}"
                                 " with force {}").format(
                                     (i, reqs[0].patt[i]), repr(reqs[0]), DIR),
                    comb_class=placedtiling)


def partial_point_placement(tiling, **kwargs):
    """
    Strategy that place a single forced point of a point requirement.

    The point placement strategy considers all point requirements in their own
    requirement lists. For each of them, it returns a new tiling where the
    point has been placed with a force.
    """
    yield from partial_requirement_placement(tiling, point_only=True)
