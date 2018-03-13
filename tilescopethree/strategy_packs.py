from comb_spec_searcher import StrategyPack
from tilescopethree.strategies import (all_cell_insertions,
                                       factor,
                                       globally_verified, point_placement,
                                       requirement_corroboration,
                                       row_and_column_separation,
                                       subset_verified)

point_placement = StrategyPack(
         eq_strats=[point_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[row_and_column_separation],
         other_strats=[[factor], [all_cell_insertions],
                       [requirement_corroboration]],
         name="point_placement")
