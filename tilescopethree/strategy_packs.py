from comb_spec_searcher import StrategyPack
from tilescopethree.strategies import (all_cell_insertions, database_verified,
                                       empty_cell_inferral, factor,
                                       globally_verified, is_empty_strategy,
                                       obstruction_transitivity,
                                       point_placement,
                                       requirement_corroboration,
                                       row_and_column_separation,
                                       subset_verified)

point_placement_only = StrategyPack(
         eq_strats=[point_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified, is_empty_strategy],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [all_cell_insertions],
                       [requirement_corroboration]],
         name="point_placement")
