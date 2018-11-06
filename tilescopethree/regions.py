"""This file contains functions for finding the forwards maps implied by
specific strategies."""
from functools import partial

from grids_three import Tiling
from tilescopethree.strategies.equivalence_strategies.point_placements import place_point_of_requirement
from tilescopethree.strategies.inferral_strategies.row_and_column_separation import row_and_column_separation
from tilescopethree.strategies.equivalence_strategies.fusion import fuse_tiling
from tilescopethree.strategies.batch_strategies.list_requirement_placements import row_placements


def mapping_after_initialise(start_tiling, end_tilings, forward_maps):
    """Return overall forward map implied by the forward maps given by a
    strategy and the inferral that has happened during the initialising."""
    return [{start_cell: frozenset(tiling.forward_map[cell]
                                   for cell in forward_map[mapped_cell])
             for start_cell, forward_map in zip(start_tiling.active_cells,
                                                forward_maps)}]

def parse_formal_step(formal_step):
    """Parse the formal step to get information about the strategy applied,
    plus any keywords needed. This will return a partial function that can be
    applied to give the same combinatorial rule. It will return None if it is a
    verification strategy."""

    def unpacking_generator(start_tiling, strategy, **kwargs):
        return next(strategy(start_tiling, **kwargs))

    if "Reverse of:" in formal_step:
        raise ValueError("Can only handle forward equivalence rules!")
    if "Placing point" in formal_step:
        _, ri, i, DIR, _ = formal_step.split("|")
        return partial(place_point_of_requirement,
                       int(ri), int(i), int(DIR), regions=True)
    elif "Insert " in formal_step:
        _, c1, c2, patt, _ = formal_step.split("|")
        cell = (int(c1), int(c2))
        return partial(cell_insertion, cell, regions=True)
    elif "factors of the tiling." in formal_step:
        return partial(Tiling.find_factors, regions=True)
    elif "Separated rows" in formal_step:
        return partial(row_and_column_separation, regions=True)
    elif "Fuse rows" in formal_step:
        _, row_index, _ = formal_step.split("|")
        return partial(fuse_tiling, row_index=int(row_index),
                       row=True, regions=True)
    elif "Fuse columns" in formal_step:
        _, col_index, _ = formal_step.split("|")
        return partial(fuse_tiling, row_index=int(col_index),
                       row=False, regions=True)
    elif "Placing row" in formal_step or "Placing col" in formal_step:
        row = "row" in formal_step
        _, direction, positive, _ = formal_step.split("|")
        return partial(unpacking_generator, strategy=row_placements,
                       row=row, positive=bool(int(positive)),
                       direction=int(direction), regions=True)
    elif "The tiling is a subset of the class" in formal_step:
        return None
    else:
        raise NotImplementedError("Not tracking regions for: " + formal_step)
