from permuta.misc import DIR_SOUTH
from comb_spec_searcher import BatchStrategy
from grids_three import Tiling, Obstruction, Requirement
from permuta import Perm
from tilescopethree.strategies.batch_strategies import cell_insertion


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
        if tiling.dimensions == (1, 1):
            yield BatchStrategy(
                formal_step="Insert {} into (0, 0).",
                tilings=[tiling.add_single_cell_obstruction(Perm((0, )),
                                                            (0, 0)),
                         tiling.add_single_cell_requirement(Perm((0, )),
                                                            (0, 0))])
        return
    slots = []
    for req in tiling.requirements:
        if len(req) > 1 or len(req[0]) > 1:
            raise ValueError("The insertion encoding can not handle"
                             "requirements that are not points")
        slots.append(req[0].pos[0])

    strategy = []
    for slot in slots:
        x, y = slot
        obstructions = []
        for ob in tiling.obstructions:
            obstructions.extend(ob.insertion_encoding(slot))

        obstructions.extend([Obstruction.single_cell(Perm((0, 1)),
                                                     (x + 1, y)),
                             Obstruction.single_cell(Perm((1, 0)),
                                                     (x + 1, y))])
        requirements = [[Requirement(Perm((0, )), ((x + 1, y),))]]

        for i, j in slots:
            if x == i:
                continue
            if i > x:
                i += 2
            if j >= y:
                j += 1
            requirements.append([Requirement(Perm((0, )), ((i, j),))])

        strategy.extend(
            [Tiling(obstructions=obstructions,
                    requirements=(
                        requirements
                        + [[Requirement(Perm((0, )), ((x, y + 1),))],
                           [Requirement(Perm((0, )), ((x + 2, y + 1),))]])),
             Tiling(obstructions=(
                           obstructions
                           + [Obstruction(Perm((0, )), ((x, y + 1),))]),
                    requirements=(
                           requirements
                           + [[Requirement(Perm((0, )), ((x + 2, y + 1),))]])),
             Tiling(obstructions=(
                           obstructions
                           + [Obstruction(Perm((0, )), ((x + 2, y + 1),))]),
                    requirements=(
                           requirements
                           + [[Requirement(Perm((0, )), ((x, y + 1),))]])),
             Tiling(obstructions=(
                           obstructions
                           + [Obstruction(Perm((0, )), ((x, y + 1),)),
                              Obstruction(Perm((0, )), ((x + 2, y + 1),))]),
                    requirements=requirements)])

    yield BatchStrategy(formal_step="Place next maximum into slots",
                        tilings=strategy)
