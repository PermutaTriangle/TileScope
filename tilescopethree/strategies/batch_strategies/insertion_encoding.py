from permuta.misc import DIR_SOUTH
from comb_spec_searcher import BatchStrategy, EquivalenceStrategy
from grids_three import Tiling, Obstruction, Requirement
from permuta import Perm
from tilescopethree.strategies.batch_strategies import cell_insertion
from collections import defaultdict


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

    If 'symmetry' then it will also consider symmetries of tilings at the root.

    If 'top_and_bottom' then will try insertion encoding rules from to and
    bottom.
    """
    if not tiling.requirements:
        if tiling.dimensions == (1, 1):
            if kwargs.get('symmetry'):
                for sym_tiling in [tiling.rotate90(), tiling.rotate180(),
                                   tiling.rotate270()]:
                    yield EquivalenceStrategy("a rotation", sym_tiling)
            yield BatchStrategy(
                formal_step="Insert {} into (0, 0).",
                comb_classes=[
                    tiling.add_single_cell_obstruction(Perm((0, )), (0, 0)),
                    tiling.add_single_cell_requirement(Perm((0, )), (0, 0))])
        return
    if kwargs.get('top_and_bottom'):
        yield EquivalenceStrategy("a rotation", tiling.rotate180())

    rows = defaultdict(list)
    for req in tiling.requirements:
        if len(req) > 1 or len(req[0]) > 1:
            raise ValueError("The insertion encoding can not handle"
                             "requirements that are not points")
        rows[req[0].pos[0][1]].append(req[0].pos[0])

    for row, slots in rows.items():
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

            for other_slots in rows.values():
                for i, j in other_slots:
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
                           requirements +
                           [[Requirement(Perm((0, )), ((x, y + 1),))],
                            [Requirement(Perm((0, )), ((x + 2, y + 1),))]])),
                 Tiling(obstructions=(
                           obstructions +
                           [Obstruction(Perm((0, )), ((x, y + 1),))]),
                        requirements=(
                           requirements +
                           [[Requirement(Perm((0, )), ((x + 2, y + 1),))]])),
                 Tiling(obstructions=(
                           obstructions +
                           [Obstruction(Perm((0, )), ((x + 2, y + 1),))]),
                        requirements=(
                           requirements +
                           [[Requirement(Perm((0, )), ((x, y + 1),))]])),
                 Tiling(obstructions=(
                           obstructions +
                           [Obstruction(Perm((0, )), ((x, y + 1),)),
                            Obstruction(Perm((0, )), ((x + 2, y + 1),))]),
                        requirements=requirements)])

        yield BatchStrategy(formal_step=("Place next maximum into"
                                         " the slots in row {}.".format(row)),
                            comb_classes=strategy)
