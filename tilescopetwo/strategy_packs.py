from tilescopetwo.strategies import *
from comb_spec_searcher import StrategyPack

point_placement_with_subobstruction_inferral = StrategyPack(
         eq_strats=[all_point_placements],
         ver_strats=[subset_verified],
         inf_strats=[subobstruction_inferral_rec],
         other_strats=[[components], [all_cell_insertions]],
         name="point_placement_with_subobstruction_inferral")

point_placement_one_cell_inferral = StrategyPack(
         eq_strats=[all_point_placements],
         ver_strats=[subset_verified],
         inf_strats=[subobstruction_inferral],
         other_strats=[[components], [all_cell_insertions]],
         name="point_placement_one_cell_inferral")

point_placement_no_infer = StrategyPack(
         eq_strats=[all_point_placements],
         ver_strats=[subset_verified],
         inf_strats=[],
         other_strats=[[components], [all_cell_insertions]],
         name="point_placement_no_infer")

row_placements = StrategyPack(eq_strats=[],
                              ver_strats=[subset_verified],
                              inf_strats=[],
                              other_strats=[[components],[all_cell_insertions, row_placements]],
                              name="row_placements")
