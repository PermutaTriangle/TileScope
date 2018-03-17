from comb_spec_searcher import InferralStrategy
from grids_three import Obstruction, Tiling
from permuta import Perm


def empty_cell_inferral(tiling, **kwargs):
    """The empty cell inferral strategy.

    The strategy considers each active but non-positive cell and inserts a
    point requirement. If the resulting tiling is empty, then a point
    obstruction can be added into the cell, i.e. the cell is empty."""
    if tiling.is_empty():
        return Tiling(obstructions=[Obstruction.empty_perm()])
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


def empty_cell_inferral_old(tiling, **kwargs):
    """The old empty cell inferral strategy.

    The strategy checks for each active non-positive cell whether a point
    obstruction can be added into the cell and returns a new tiling with the
    new obstructions.
    """
    positive_cells = list(tiling.positive_cells)

    adding = []
    empty_cells = []
    empty_ob = Obstruction.empty_perm()
    if can_add_obstruction(tiling, empty_ob, positive_cells):
        adding.append(empty_ob)
    else:
        for cell in tiling.possibly_empty:
            ob = Obstruction.single_cell(Perm((0,)), cell)
            if can_add_obstruction(tiling, ob, positive_cells):
                adding.append(ob)
                empty_cells.append(cell)
    if adding:
        new_tiling = Tiling(obstructions=tiling.obstructions + tuple(adding),
                            requirements=tiling.requirements)

        return InferralStrategy("The cells {} are empty".format(empty_cells),
                                new_tiling)


def can_add_obstruction(tiling, obstruction, positive_cells):
    """Checks whether an obstruction can be added to a tiling.

    The check is done by considering all superobstructions of the given
    obstruction using the positive cells. If each of these obstructions are
    'covered' by the obstructions already present in the tiling, then the given
    obstruction can be added to the tiling.
    """
    for i, cell in enumerate(positive_cells):
        if obstruction.occupies(cell):
            continue
        obs = list(obstruction.insert_point(cell))
        if all(any(o in ob for o in tiling.obstructions) for ob in obs):
            return True
        return all(can_add_obstruction(tiling, ob, positive_cells[i+1:])
                   for ob in obs)
    return any(o in obstruction for o in tiling.obstructions)
