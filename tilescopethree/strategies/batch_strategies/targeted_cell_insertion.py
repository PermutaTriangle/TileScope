from comb_spec_searcher import Rule
from permuta.misc import UnionFind


def targeted_cell_insertion(tiling, **kwargs):
    """Return combintorial rules formed by inserting """
    factors = factors_of_gridded_perm(tiling)
    if not factors:
        return
    for f in factors:
        yield Rule("Insert {}.".format(repr(f)),
                   [tiling.add_obstruction(f.patt, f.pos),
                    tiling.add_requirement(f.patt, f.pos)],
                   inferable=[True, True],
                   workable=[True, True],
                   ignore_parent=True,
                   constructor='disjoint')


def components(tiling):
    """Return the component of a tiling. Two cells are in the same component if
    they are in the same row or column."""
    n, m = tiling.dimensions

    def cell_to_int(cell):
        return cell[0] * m + cell[1]

    def int_to_cell(i):
        return (i // m, i % m)

    cells = list(tiling.active_cells)
    uf = UnionFind(n * m)
    for i in range(len(cells)):
        for j in range(i+1, len(cells)):
            c1, c2 = cells[i], cells[j]
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
    return component_cells


def factors_of_gridded_perm(tiling):
    """Return factor of gridded permutation if separated from rest of gridded
    permutation, if cells are not on the same row or column."""
    comps = components(tiling)
    if len(comps) <= 1:
        return
    factors = set()
    for ob in tiling.obstructions:
        subperms = [ob.get_gridded_perm_in_cells(c) for c in comps]
        subperms = [p for p in subperms if p]
        if len(subperms) > 1:
            factors.update(subperms)
    return factors
