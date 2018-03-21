from permuta.misc import DIR_SOUTH
from comb_spec_searcher import Strategy
from grids_three import Tiling, Obstruction, Requirement
from permuta import Perm

def insertion_encoding(tiling, **kwargs):
    """
    Insert a new maximum as in the insertion encoding.

    The insertion encoding strategy is a batch strategy which takes in a 1 x n
    tiling where it is assumed that all cells contains a point requirement. It
    considers where the lowest entry is of a gridded permutation is on this
    tiling and places it into its cell. It will place this as one of four
    options, in correspondence with the letters in the insertion encoding:
        - f: it is the only point in the cell
        - l: it is the leftmost point in the cell, and there will be a point
             appearing to the right of it in this cell
        - r: it is the rightmost point in the cell, and there will be a point
             appearing to the left of it in this cell
        - m: it is in the middle and there will be a point appearing to the
             right and left of it in this cell.
    """
    if not tiling.requirements:
        return
    slots = []
    for req in tiling.requirements:
        if len(req) > 1 or len(req[0]) > 1:
            raise ValueError("The insertion encoding can not handle requirements that are not points")
        slots.append(req[0].pos[0])

    strategy = []
    for slot in slots:
        x, y = slot
        obstructions = []
        for ob in tiling.obstructions:
            obstructions.extend(ob.place_point((x, y - 10), DIR_SOUTH))
        obstructions.extend([Obstruction.single_cell(Perm((0, 1)), (x + 1, y + 1)),
                             Obstruction.single_cell(Perm((1, 0)), (x + 1, y + 1))])
        requirements = [[Requirement(Perm((0, )), ((x + 1, y + 1),))]]
        for i, j in slots:
            if x == i:
                continue
            if i > x:
                i += 2
            requirements.append([Requirement(Perm((0, )), ((i, j + 2),))])

        strategy.extend(
        [Tiling(obstructions=obstructions,
                requirements=(requirements
                       + [[Requirement(Perm((0, )), ((x, y + 2),))],
                          [Requirement(Perm((0, )), ((x + 2, y + 2),))]])),
         Tiling(obstructions=(obstructions
                       + [Obstruction(Perm((0, )), ((x, y + 2),))]),
                requirements=(requirements
                       + [[Requirement(Perm((0, )), ((x + 2, y + 2),))]])),
         Tiling(obstructions=(obstructions
                       + [Obstruction(Perm((0, )), ((x + 2, y + 2),))]),
                requirements=(requirements
                       + [[Requirement(Perm((0, )), ((x, y + 2),))]])),
         Tiling(obstructions=(obstructions
                       + [Obstruction(Perm((0, )), ((x, y + 2),)),
                          Obstruction(Perm((0, )), ((x + 2, y + 2),))]),
               requirements=requirements)])
               
    yield Strategy(formal_step="Place next maximum into slots",
                   objects=strategy,
                   workable=[True for _ in strategy])
