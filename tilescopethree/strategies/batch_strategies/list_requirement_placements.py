from comb_spec_searcher import Strategy 
from permuta.misc import DIR_EAST, DIR_NORTH, DIR_SOUTH, DIR_WEST, DIR_NONE

from grids_three import Obstruction, Requirement, Tiling

from itertools import chain
from permuta import Perm


def requirement_placement(tiling, **kwargs):
    for req in tiling.requirements:
        for direction in [DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST]:
            tilings = place_requirement_list(tiling, req, direction)
            yield Strategy(
                        formal_step=("Place requirement {} in direction {}."
                                     "".format(req, direction)),
                        comb_classes=tilings,
                        ignore_parent=False,
                        possibly_empty=[True for _ in tilings],
                        inferable=[True for _ in tilings],
                        workable=[True for _ in tilings],
                        constructor='disjoint')
            

def place_requirement_list(tiling, req_list, direction):
    """Return the list of tilings obtained by placing the direction-most point 
    of a requirement list. This represents a batch strategy, where the 
    direction-most point of each requirement in the list is placed."""
    # Compute the points furthest in the given direction.
    min_points = minimum_points(req_list, direction)
    if len([c for _, c in min_points]) != len(set([c for _, c in min_points])):
        raise NotImplementedError(("Can't handle list requirements with more" 
                                   "than req farthest in the direction in same"
                                   " cell."))
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
