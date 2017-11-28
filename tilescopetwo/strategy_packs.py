from tilescopetwo.strategies import *
from comb_spec_searcher import StrategyPack
from functools import partial
from permuta import Perm

# WARNING: To use full subobstruction inferral need strategy
# 'subobstruction_inferral_rec' but it is a lot slower. The function
# 'subobstruction_inferral' is a subset of the work.

################################################################################
###################### STRATEGY PACKS FOR RUN 15/11/2017 #######################
################################################################################

forced_patterns_3 = StrategyPack(
        eq_strats=[],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[partial(components, unions=True)],
                      [partial(all_requirement_insertions, maxreqlen=3),
                       all_cell_insertions, forced_binary_pattern]],
        name="forced_patterns_3")

forced_patterns_with_row_column_placements = StrategyPack(
        eq_strats=[],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[partial(components, unions=True)],
                      [partial(all_requirement_insertions, maxreqlen=3),
                       all_cell_insertions, row_placements, col_placements,
                       forced_binary_pattern]],
        name="forced_patterns_with_row_column_placements")

row_column_placements = StrategyPack(
        eq_strats=[],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[components],
                      [all_cell_insertions, partial(row_placements, all_positive_in_row=False),  partial(col_placements, all_positive_in_row=False)]],
        name="row_column_placements")

point_sep_and_iso = StrategyPack(
        eq_strats=[point_separation],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[partial(components, unions=True, workable=False)],
                      [all_cell_insertions, point_isolations]],
        name="point_sep_and_iso")

forced_patterns_4 = StrategyPack(
        eq_strats=[],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[partial(components, unions=True)],
                      [partial(all_requirement_insertions, maxreqlen=4),
                       all_cell_insertions,
                       forced_binary_pattern]],
        name="forced_patterns_4")

################################################################################
################################################################################
###################### STRATEGY PACKS FOR RUN 21/11/2017 #######################
################################################################################

root_requirement_placements = StrategyPack(
        eq_strats=[partial(row_placements, equivalence_only=True)],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[components],
                      [partial(root_requirement_insertions, maxreqlen=4),
                       partial(forced_binary_pattern, forcelen=2)],
                      [all_cell_insertions, row_placements,  col_placements]],
        name="root_requirement_placements")

point_placement = StrategyPack(
         eq_strats=[all_point_placements],
         ver_strats=[subset_verified, database_verified, globally_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[components], [all_cell_insertions]],
         name="point_placement")

all_strategies = StrategyPack(
        eq_strats=[all_point_placements, point_separation,
                   partial(row_placements, equivalence_only=True),
                   partial(col_placements, equivalence_only=True),
                   partial(point_isolations, equivalence_only=True)],
         ver_strats=[subset_verified, database_verified, globally_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[partial(components, unions=True)],
                       [partial(root_requirement_insertions, maxreqlen=4),
                        partial(all_requirement_insertions, maxreqlen=4),
                        partial(forced_binary_pattern, forcelen=2)],
                       [all_cell_insertions,
                        partial(row_placements, ignore_equivalence=True),
                        partial(col_placements, ignore_equivalence=True),
                        partial(point_isolations, ignore_equivalence=True)]],
        name="all_strategies")

################################################################################
################################################################################

forced_patterns_2_basic = StrategyPack(
        eq_strats=[],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[components],
                      [partial(all_requirement_insertions, maxreqlen=2),
                       all_cell_insertions, forced_binary_pattern]],
        name="forced_patterns_2_basic")

point_sep_equiv_iso = StrategyPack(
        eq_strats=[point_separation,
                   partial(point_isolations, equivalence_only=True)],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, subobstruction_inferral_rec,
                    row_and_column_separation],
        other_strats=[[partial(components, unions=True, workable=False)],
                      [all_cell_insertions,
                       partial(point_isolations, ignore_equivalence=True)]],
        name="point_sep_equiv_iso")

row_column_eqv_placements = StrategyPack(
        eq_strats=[partial(row_placements, equivalence_only=True),
                   partial(col_placements, equivalence_only=True)],
        ver_strats=[subset_verified, database_verified, globally_verified],
        inf_strats=[empty_cell_inferral, row_and_column_separation],
        other_strats=[[components],
                      [all_cell_insertions,
                       partial(row_placements, ignore_equivalence=True),
                       partial(col_placements, ignore_equivalence=True)]],
        name="row_column_placements")


point_placement_one_cell_inferral = StrategyPack(
         eq_strats=[all_point_placements],
         ver_strats=[subset_verified],
         inf_strats=[empty_cell_inferral],
         other_strats=[[components], [all_cell_insertions]],
         name="point_placement")

point_placement_no_infer = StrategyPack(
         eq_strats=[all_point_placements],
         ver_strats=[subset_verified],
         inf_strats=[empty_cell_inferral],
         other_strats=[[components], [all_cell_insertions]],
         name="point_placement_no_infer")

row_placements_only = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[components],[all_cell_insertions, row_placements]],
         name="row_placements")

col_placements_only = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[components], [all_cell_insertions, col_placements]],
         name="col_placements")

row_and_column_placements = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[components],
                       [all_cell_insertions, row_placements, col_placements]],
         name="row_and_column_placements")

row_and_column_placements_and_database = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, database_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[components],
                       [all_cell_insertions, row_placements, col_placements]],
         name="row_and_column_placements_and_database")

point_separation_and_row_col_placements = StrategyPack(
         eq_strats=[point_separation],
         ver_strats=[subset_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[components],
                       [all_cell_insertions,
                        partial(row_placements, all_positive_in_row=False),
                        partial(col_placements, all_positive_in_col=False)]],
         name="row_and_column_placements")

binary_force_only = StrategyPack(
    eq_strats=[forced_binary_pattern],
    ver_strats=[subset_verified],
    inf_strats=[empty_cell_inferral, row_and_column_separation],
    other_strats=[[partial(components, unions=True)],
                  [all_cell_insertions],
                  [partial(all_requirement_insertions, maxreqlength=4)],
                  ],
    name="binary_force w/ row-col separation and cell insertions")

point_separation_and_isolation = StrategyPack(
         eq_strats=[point_separation],
         ver_strats=[subset_verified],
         inf_strats=[empty_cell_inferral, row_and_column_separation],
         other_strats=[[partial(components, workable=False, unions=True)],
                       [all_cell_insertions, point_isolations]],
         name="point_separation_and_isolation")
