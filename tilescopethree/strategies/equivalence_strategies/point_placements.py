from grids_three import Obstruction, Requirement, Tiling
from permuta import Perm
from permuta.misc import DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST
from itertools import chain


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
    # The gridded permutations corresponding to the forced occurrence of the
    # requirement and the rest of the requirement
    inserted_gp = requirement.place_point(
        cell, opposite_dir(force_dir))
    forced_obstructions = [Obstruction(gp.patt, gp.pos) for gp in inserted_gp
                           if len(gp) == len(requirement)]
    new_req = [gp for gp in inserted_gp if len(gp) < len(requirement)]
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
    pass


def point_placement(tiling, **kwargs):
    """
    Strategy that place a single forced point of a point requirement.

    The point placement strategy considers all point requirements in their own
    requirement lists. For each of them, it returns a new tiling where the
    point has been placed with a force.
    """
    yield from requirement_placement(tiling, point_only=True)
