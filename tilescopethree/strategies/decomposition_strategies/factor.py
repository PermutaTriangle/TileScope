from comb_spec_searcher import Strategy
from itertools import chain
from grids_three import Tiling
from grids_three.misc import union_reduce
from permuta.misc import UnionFind
from permuta.misc.ordered_set_partitions import ordered_set_partitions_list


def factor(tiling, **kwargs):
    """
    The factor strategy that decomposes a tiling into its connected factors.

    The factors are the connected components of the graph of the tiling, where
    vertices are the cells. Two vertices are connected if there exists a
    obstruction or requirement occupying both cells. Two cells are also
    connected if they share the same row or column unless the interleaving or
    point_interleaving keyword arguments are set to True.
    When point interleavings are allowed, two cells in the same row or column
    are not connected. When general interleavings are allowed, two cells in the
    same row or column are not connected.
    """
    interleaving = kwargs.get("interleaving", False)
    point_interleaving = kwargs.get("point_interleaving", False)
    n, m = tiling.dimensions

    def cell_to_int(cell):
        return cell[0] * m + cell[1]

    def int_to_cell(i):
        return (i // m, i % m)

    cells = list(tiling.active_cells)
    uf = UnionFind(n * m)

    # Unite by obstructions
    for ob in tiling.obstructions:
        for i in range(len(ob.pos)):
            for j in range(i+1, len(ob.pos)):
                uf.unite(cell_to_int(ob.pos[i]), cell_to_int(ob.pos[j]))

    # Unite by requirements
    for req_list in tiling.requirements:
        req_cells = list(union_reduce(req.pos for req in req_list))
        for i in range(len(req_cells)):
            for j in range(i + 1, len(req_cells)):
                uf.unite(cell_to_int(req_cells[i]), cell_to_int(req_cells[j]))

    # If interleaving not allowed, unite by row/col
    if not interleaving:
        for i in range(len(cells)):
            for j in range(i+1, len(cells)):
                c1, c2 = cells[i], cells[j]
                if (point_interleaving and
                        (c1 in tiling.point_cells or
                         c2 in tiling.point_cells)):
                    continue
                if c1[0] == c2[0] or c1[1] == c2[1]:
                    uf.unite(cell_to_int(c1), cell_to_int(c2))

    # Collect the connected components of the cells
    all_components = {}
    for cell in cells:
        i = uf.find(cell_to_int(cell))
        if i in all_components:
            all_components[i].append(cell)
        else:
            all_components[i] = [cell]
    component_cells = list(set(cells) for cells in all_components.values())

    # If the tiling is a single connected component
    if len(component_cells) <= 1:
        return

    # Collect the factors of the tiling
    factors = []
    strategy = []  # the vanilla factors
    for cell_component in component_cells:
        obstructions = [ob for ob in tiling.obstructions
                        if ob.pos[0] in cell_component]
        requirements = [req for req in tiling.requirements
                        if req[0].pos[0] in cell_component]

        if obstructions or requirements:
            factors.append((obstructions, requirements))
            strategy.append(Tiling(obstructions=obstructions,
                                   requirements=requirements))

    if kwargs.get("workable", True):
        work = [True for _ in strategy]
    else:
        work = [False for _ in strategy]

    yield Strategy("The factors of the tiling.", strategy, workable=work,
                   back_maps=[t.back_map for t in strategy])

    if kwargs.get("unions", False):
        for partition in ordered_set_partitions_list(factors):
            strategy = []
            for part in partition:
                obstructions, requirements = zip(*part)
                strategy.append(Tiling(obstructions=chain(*obstructions),
                                       requirements=chain(*requirements)))
            yield Strategy("The union of factors of the tiling",
                           strategy,
                           workable=[False for _ in strategy],
                           back_maps=[t.back_map for t in strategy])
