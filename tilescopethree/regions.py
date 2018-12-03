"""This file contains functions for finding the forwards maps implied by
specific strategies."""
from functools import partial

from permuta import Perm
from grids_three import GriddedPerm, Tiling
from tilescopethree.strategies.equivalence_strategies.point_placements import place_point_of_requirement
from tilescopethree.strategies.inferral_strategies.row_and_column_separation import row_and_column_separation
from tilescopethree.strategies.equivalence_strategies.fusion import fuse_tiling
from tilescopethree.strategies.batch_strategies.list_requirement_placements import row_placements
from tilescopethree.strategies.batch_strategies.cell_insertion import cell_insertion
from tilescopethree.strategies.batch_strategies.cell_insertion import col_insertion_helper, row_insertion_helper
from tilescopethree.strategies.batch_strategies.requirement_corroboration import gp_insertion
from tilescopethree.strategies.equivalence_strategies.fusion_with_interleaving import fuse_tiling as fancy_fuse_tiling


def mapping_after_initialise(start_tiling, end_tilings, forward_maps):
    """Return overall forward map implied by the forward maps given by a
    strategy and the inferral that has happened during the initialising."""
    # print(start_tiling)
    # for t in end_tilings:
    #     print(t)
    #     print(t.forward_map)
    # for m in forward_maps:
    #     print(m)
    for tiling in end_tilings:
        if tiling.is_empty():
            tiling.forward_map = {}
    # for tiling, forward_map in zip(end_tilings, forward_maps):
    #     print(tiling)
    #     print(forward_map)
    #     for start_cell in start_tiling.active_cells:
    #         print(start_cell)
    #         for cell in forward_map[start_cell]:
    #             print(cell, (cell in tiling.forward_map and
    #                   tiling.forward_map[cell] in tiling.active_cells))
    return [{start_cell: frozenset(tiling.forward_map[cell]
                                   for cell in forward_map[start_cell]
                                   if (cell in tiling.forward_map and
                                       tiling.forward_map[cell] in
                                       tiling.active_cells))
             for start_cell in start_tiling.active_cells}
            for tiling, forward_map in zip(end_tilings, forward_maps)]

def parse_formal_step(formal_step):
    """Parse the formal step to get information about the strategy applied,
    plus any keywords needed. This will return a partial function that can be
    applied to give the same combinatorial rule. It will return None if it is a
    verification strategy."""

    def unpacking_generator(start_tiling, strategy, **kwargs):
        return next(strategy(start_tiling, **kwargs))

    def apply_post_map(start_tiling, strategy, **kwargs):
        # print(start_tiling)
        # print(strategy)
        # print(kwargs)
        end_tilings, forward_maps = strategy(start_tiling, **kwargs)
        # for t in end_tilings:
        #     print(t)
        #     print(t.forward_map)
        # for m in forward_maps:
        #     print(m)
        return end_tilings, mapping_after_initialise(start_tiling, end_tilings,
                                                     forward_maps)

    if "Reverse of:" in formal_step:
        if "reverse" in formal_step:
            return partial(Tiling.reverse, regions=True)
        raise ValueError("Can only handle forward equivalence rules!")
    if "Placing point" in formal_step:
        _, ri, i, DIR, _ = formal_step.split("|")
        return partial(place_point_of_requirement,
                       req_index=int(ri), point_index=int(i),
                       force_dir=int(DIR), regions=True)
    elif "Insert " in formal_step:
        _, c1, c2, patt, _ = formal_step.split("|")
        patt = Perm.from_string(patt)
        cell = (int(c1), int(c2))
        return partial(apply_post_map, strategy=cell_insertion, patt=patt,
                       cell=cell, regions=True)
    elif "factors of the tiling." in formal_step:
        return partial(Tiling.find_factors, regions=True)
    elif "Separated rows" in formal_step:
        return partial(row_and_column_separation, regions=True)
    elif "Fuse rows" in formal_step:
        _, row_index, _ = formal_step.split("|")
        if "fancily" in formal_step:
            fusion = fancy_fuse_tiling
        else:
            fusion = fuse_tiling
        return partial(fusion, row_index=int(row_index),
                       row=True, regions=True)
    elif "Fuse columns" in formal_step:
        _, col_index, _ = formal_step.split("|")
        if "fancily" in formal_step:
            fusion = fancy_fuse_tiling
        else:
            fusion = fuse_tiling
        return partial(fusion, row_index=int(col_index),
                       row=False, regions=True)
    elif "Either row " in formal_step:
        row = int(formal_step.split(' ')[2])
        return partial(apply_post_map, strategy=row_insertion_helper,
                                       row=row,
                                       row_cells=None,
                                       regions=True)
    elif "Either col " in formal_step:
        col = int(formal_step.split(' ')[2])
        return partial(apply_post_map, strategy=col_insertion_helper,
                                       col=col,
                                       col_cells=None,
                                       regions=True)
    elif "Placing row" in formal_step or "Placing col" in formal_step:
        row = "row" in formal_step
        _, idx, direction, positive, _ = formal_step.split("|")
        return partial(apply_post_map,
                       strategy=partial(unpacking_generator,
                                        strategy=row_placements,
                                        row=row, positive=bool(int(positive)),
                                        index=int(idx),
                                        direction=int(direction),
                                        regions=True))
    elif "The tiling is a subset of the class" in formal_step:
        return None
    elif "Inserting " in formal_step:
        front, _, _ = formal_step.split('~')
        _, patt, pos, _ = formal_step.split("|")
        position = []
        for cell in pos.split("/"):
            x, y = cell.split(",")
            position.append((int(x), int(y)))
        gp = GriddedPerm(Perm.to_standard(patt), position)
        return partial(apply_post_map,
                       strategy=gp_insertion, gp=gp, regions=True)
    elif "Greedily placing points" in formal_step:
        return partial(apply_post_map,
                       strategy=greedy_griddings,
                       formal_step=formal_step)
    else:
        raise NotImplementedError("Not tracking regions for: " + formal_step)

def greedy_griddings(tiling, formal_step):
    from grid_class import GridClass
    if "reversed" in formal_step:
        rev_til = tiling.reverse()
        g = GridClass(rev_til.obstructions)
        maps = [{(1, 0): frozenset([(0, 0)]),
                 (0, 0): frozenset()},
                {(0, 0): frozenset([(0, 0)]),
                 (0, 0): frozenset([(1, 0), (2, 0)])}]
    else:
        g = GridClass(tiling.obstructions)
        maps = [{(0, 0): frozenset([(0, 0)]),
                 (1, 0): frozenset()},
                {(0, 0): frozenset([(0, 0)]),
                 (1, 0): frozenset([(1, 0), (2, 0)])}]
    strat = g.disambiguate()

    return strat, maps


def get_fuse_region(start_tiling, formal_step):
    """Return the cells in the row or columns before fusion. Returns a tuple,
    the first is the first row, the second is the second row. When fused the
    second row merge with the first."""
    _, ri, _ = formal_step.split("|")
    ri = int(ri)
    row = "row" in formal_step
    return (frozenset([c for c in start_tiling.active_cells
                       if (((row and c[1] == ri) or
                           (not row and c[0] == ri)))]),
            frozenset([c for c in start_tiling.active_cells
                       if (((row and c[1] == ri + 1) or
                           (not row and c[0] == ri + 1)))]))
