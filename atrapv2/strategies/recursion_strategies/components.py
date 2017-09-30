"""A recursive strategy using the definition of components."""


from grids import Tiling
from permuta.misc import UnionFind
from itertools import combinations
from atrap.tools import cells_of_occurrences

from comb_spec_searcher import DecompositionStrategy


def components(tiling, basis, basis_partitioning=None, **kwargs):
    """
    Yield strategy found by taking components of a tiling.

    Two cells are in the same component if there exists an occurrence using both cells.
    """
    cell_to_int = {}

    for cell, _ in tiling:
        # TODO: use integer mapping
        cell_to_int[cell] = len(cell_to_int)

    components_set = UnionFind(len(cell_to_int))

    occurrences_of_basis_elements = cells_of_occurrences(tiling, basis, basis_partitioning=basis_partitioning)
    for cells_of_occurrence in occurrences_of_basis_elements:
        for cell1, cell2 in combinations(cells_of_occurrence, 2):
            components_set.unite(cell_to_int[cell1], cell_to_int[cell2])

    all_components = {}
    for cell, _ in tiling:
        i = components_set.find(cell_to_int[cell])
        if i in all_components:
            all_components[i].append(cell)
        else:
            all_components[i] = [cell]
    cells_of_new_tilings = list(all_components.values())

    if len(cells_of_new_tilings) == 1:
        return
    strategy = []
    for new_cells in cells_of_new_tilings:
        new_tiling_dict = {}
        for cell in new_cells:
            new_tiling_dict[cell] = tiling[cell]
        strategy.append(Tiling(new_tiling_dict))

    if len(strategy) <= 1:
        return

    yield DecompositionStrategy("The components of the tiling", strategy, [t._back_map for t in strategy])
# Consider the union of components?
