from comb_spec_searcher import StrategyPack
from functools import partial
from tilescopethree.strategies import (all_cell_insertions, database_verified,
                                       empty_cell_inferral, factor,
                                       globally_verified, is_empty_strategy,
                                       obstruction_transitivity,
                                       point_placement, verify_points,
                                       requirement_corroboration,
                                       row_and_column_separation,
                                       subset_verified, insertion_encoding)

point_placement_only = StrategyPack(
         eq_strats=[point_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified, is_empty_strategy],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [all_cell_insertions],
                       [requirement_corroboration]],
         name="point_placement")

regular_insertion_encoding = StrategyPack(
        eq_strats=[],
        ver_strats=[subset_verified],
        inf_strats=[],
        other_strats=[[factor], [all_cell_insertions], [insertion_encoding]],
        name="regular_insertion_encoding"
)
