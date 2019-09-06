from itertools import chain

from comb_spec_searcher import Rule
from tilings.algorithms import (Factor, FactorWithInterleaving,
                                FactorWithMonotoneInterleaving)


def general_factor(tiling, factor_class, constructor, **kwargs):
    factor = factor_class(tiling)
    if factor.factorable():
        if kwargs.get("workable", True):
            workable = [True for _ in strategy]
        else:
            workable = [False for _ in strategy]
        yield Rule("The factors of the tiling.",
                   factor.factors(),
                   inferable=[False for _ in strategy],
                   workable=work,
                   possibly_empty=[False for _ in strategy],
                   ignore_parent=kwargs.get("workable", True),
                   constructor=constructor)


def factor(tiling, **kwargs):
    return general_factor(tiling, Factor, 'cartesian')


def factor_with_monotone_interleaving(tiling, **kwargs):
    return general_factor(tiling, FactorWithMonotoneInterleaving, 'other')


def factor_with_interleaving(tiling, **kwargs):
    return general_factor(tiling, FactorWithInterleaving, 'other')

# -----------------------------------------------------------------
#       The old stuff
# -----------------------------------------------------------------



def factor_old(tiling, **kwargs):
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
                                   requirements=requirements,
                                   minimize=False))

    if kwargs.get("workable", True):
        work = [True for _ in strategy]
    else:
        work = [False for _ in strategy]

    new_algo_factor = Factor(tiling).factors()
    if (len(new_algo_factor) != len(strategy) or set(new_algo_factor) !=
        set(strategy)):
        print(tiling)
        print(tiling.__repr__())

    yield Rule("The factors of the tiling.", strategy,
               inferable=[False for _ in strategy], workable=work,
               possibly_empty=[False for _ in strategy],
               ignore_parent=kwargs.get("workable", True),
               constructor='cartesian')

    if kwargs.get("unions", False):
        for partition in partition_list(factors):
            strategy = []
            for part in partition:
                obstructions, requirements = zip(*part)
                strategy.append(Tiling(obstructions=chain(*obstructions),
                                       requirements=chain(*requirements),
                                       minimize=False))
            yield Rule("The union of factors of the tiling",
                       strategy,
                       possibly_empty=[False for _ in strategy],
                       inferable=[False for _ in strategy],
                       workable=[False for _ in strategy],
                       constructor='cartesian')


# The code below is magical and comes from
# https://codereview.stackexchange.com/questions/1526/finding-all-k-subset-partitions


def partition_list(lst):
    for i in range(2, len(lst)):
        for part in algorithm_u(lst, i):
            yield part


def algorithm_u(ns, m):
    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)
