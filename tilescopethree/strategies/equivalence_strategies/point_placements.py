from itertools import chain

from comb_spec_searcher import Rule
from permuta import Perm
from permuta.misc import (DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST,
                          DIRS)
from tilings import Obstruction, Requirement, Tiling


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


def place_point_of_requirement(tiling, req_index, point_index, force_dir):
    """
    Places the point at point_index in requirement at req_index into tiling.
    """
    if len(tiling.requirements[req_index]) > 1:
        raise ValueError(
            "Requirement list at {} contains more than 1 requirement.".format(
                req_index))
    # The requirement
    requirement = tiling.requirements[req_index][0]
    # The cell containing the point
    cell = requirement.pos[point_index]
    # The rest of the requirements
    other_reqs = [tiling.requirements[i]
                  for i in range(len(tiling.requirements))
                  if i != req_index]
    # Placing the forced occurrence of the point in the requirement
    new_req, forced_obstructions = requirement.place_forced_point(
        point_index, force_dir)
    assert len(new_req) == 1
    # New indices of the point
    point_cell = (cell[0] + 1, cell[1] + 1)

    # The set of new obstructions, consisting of the forced obstructions, other
    # obstructions where the point placement has been taken into account and
    # the 12, 21 in the cell.
    newobs = forced_obstructions + list(chain.from_iterable(
        ob.place_point(cell, DIR_NONE) for ob in tiling.obstructions)) + [
            Obstruction.single_cell(Perm((0, 1)), point_cell),
            Obstruction.single_cell(Perm((1, 0)), point_cell)]
    # The new requirements, consisting of the requirement with the point
    # placed, other requirements where point placement has been taken into
    # account and the point requirement in the cell.
    newreqs = [list(chain.from_iterable(req.place_point(cell, DIR_NONE)
                                        for req in reqs))
               for reqs in other_reqs] + [new_req] + [
                       [Requirement.single_cell(Perm((0,)), point_cell)]]
    return Tiling(obstructions=newobs, requirements=newreqs)


def requirement_placement(tiling, **kwargs):
    """
    Strategy that places a single forced point of a requirement.

    The requirement_placement strategy considers every requirement list of
    length exactly 1. For each of these requirements, it considers all the
    points of the requirement. The strategy then returns all tilings where the
    point has been placed with a force.
    """
    point_cells = tiling.point_cells
    point_only = kwargs.get('point_only')
    ignore_parent = kwargs.get('ignore_parent', False)
    for ri, reqs in enumerate(tiling.requirements):
        if len(reqs) > 1:
            continue
        if reqs[0].is_point_perm() in point_cells and
        tiling.only_cell_in_row_and_col(reqs[0].is_point_perm()):
            continue
        if point_only and reqs[0].is_point_perm() is None:
            continue
        for i in range(len(reqs[0])):
            for DIR in DIRS:
                placedtiling = place_point_of_requirement(tiling, ri, i, DIR)
                yield Rule(
                    formal_step=("Placing point {} of requirement {} "
                                 "with force {}").format(
                                    (i, reqs[0].patt[i]), str(reqs[0]), DIR),
                    comb_classes=[placedtiling],
                    ignore_parent=ignore_parent,
                    inferable=[True],
                    possibly_empty=[True],
                    workable=[True],
                    constructor='equiv')


def point_placement(tiling, **kwargs):
    """
    Strategy that place a single forced point of a point requirement.

    The point placement strategy considers all point requirements in their own
    requirement lists. For each of them, it returns a new tiling where the
    point has been placed with a force.
    """
    yield from requirement_placement(tiling, point_only=True)
