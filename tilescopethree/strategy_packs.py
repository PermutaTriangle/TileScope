from comb_spec_searcher import StrategyPack
from functools import partial
from tilescopethree.strategies import (all_cell_insertions, database_verified,
                                       empty_cell_inferral, factor,
                                       globally_verified,
                                       obstruction_transitivity,
                                       point_placement, verify_points,
                                       requirement_corroboration,
                                       row_and_column_separation,
                                       subset_verified, insertion_encoding)

point_placement_only = StrategyPack(
         eq_strats=[point_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [all_cell_insertions],
                       [requirement_corroboration]],
         name="point_placement")

regular_insertion_encoding = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[],
        other_strats=[[factor], [insertion_encoding]],
        name="regular_insertion_encoding"
)

regular_insertion_encoding_symmetries = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[],
        other_strats=[[factor], [partial(insertion_encoding, symmetry=True)]],
        name="regular_insertion_encoding_symmetries"
)

regular_insertion_encoding_top_and_bottom = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[],
        other_strats=[[factor],
                      [partial(insertion_encoding, top_and_bottom=True)]],
        name="regular_insertion_encoding_top_and_bottom"
)

regular_insertion_encoding_symmetries_top_and_bottom = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[],
        other_strats=[[factor],
                      [partial(insertion_encoding, symmetry=True,
                               top_and_bottom=True)]],
        name="regular_insertion_encoding_symmetries_top_and_bottom"
)

better_insertion_encoding = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor], [insertion_encoding]],
        name="better_insertion_encoding"
)

better_insertion_encoding_symmetries = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor], [partial(insertion_encoding, symmetry=True)]],
        name="better_insertion_encoding_symmetries"
)

better_insertion_encoding_top_and_bottom = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor],
                      [partial(insertion_encoding, top_and_bottom=True)]],
        name="better_insertion_encoding_top_and_bottom"
)

better_insertion_encoding_symmetries_top_and_bottom = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor],
                      [partial(insertion_encoding, symmetry=True,
                               top_and_bottom=True)]],
        name="better_insertion_encoding_symmetries_top_and_bottom"
)
