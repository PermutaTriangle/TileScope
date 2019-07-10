from comb_spec_searcher import InferralStrategy
from tilings import Obstruction, Tiling
from permuta import Perm


def empty_cell_inferral(tiling, **kwargs):
    """The empty cell inferral strategy.

    The strategy considers each active but non-positive cell and inserts a
    point requirement. If the resulting tiling is empty, then a point
    obstruction can be added into the cell, i.e. the cell is empty."""
    active = set(tiling.active_cells)
    positive = set(tiling.positive_cells)
    empty_cells = []
    for cell in active - positive:
        reqtil = tiling.insert_cell(cell)
        if reqtil.is_empty():
            empty_cells.append(cell)
    newobs = [Obstruction.single_cell(Perm((0,)), cell)
              for cell in empty_cells]
    return InferralStrategy(
        "The cells {} are empty".format(", ".join(map(str, empty_cells))),
        Tiling(obstructions=tiling.obstructions + tuple(newobs),
               requirements=tiling.requirements))


def subobstruction_inferral(tiling, **kwargs):
    """Return tiling created by adding all subobstructions which can be
    added."""
    subobs = set()
    for ob in tiling.obstructions:
        subobs.update(ob.all_subperms())
    newobs = []
    if subobs:
        merged_tiling = tiling.merge(remove_empty=False)
        for ob in sorted(subobs, key=len):
            if can_add_obstruction(ob, merged_tiling):
                newobs.append(ob)
                merged_tiling = Tiling(merged_tiling.obstructions + (ob,),
                                       merged_tiling.requirements,
                                       remove_empty=False)
    if newobs:
        return InferralStrategy("Added the obstructions {}.".format(newobs),
                                Tiling(tiling.obstructions + tuple(newobs),
                                       tiling.requirements))


def can_add_obstruction(obstruction, tiling):
    """Return true if obstruction can be added to tiling."""
    return tiling.add_requirement(obstruction.patt,
                                  obstruction.pos).merge().is_empty()
