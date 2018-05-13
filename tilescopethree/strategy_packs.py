from comb_spec_searcher import StrategyPack
from functools import partial
from tilescopethree.strategies import (all_cell_insertions,
                                       all_point_insertions,
                                       all_requirement_extensions,
                                       database_verified,
                                       empty_cell_inferral, factor,
                                       globally_verified,
                                       fundamentally_verified,
                                       obstruction_transitivity,
                                       point_placement, requirement_placement,
                                       verify_points,
                                       requirement_corroboration,
                                       row_and_column_separation,
                                       subset_verified, insertion_encoding)
from grids_three import Tiling


inverse = Tiling.inverse
reverse = Tiling.reverse
complement = Tiling.complement
antidiagonal = Tiling.antidiagonal
rotate90 = Tiling.rotate90
rotate180 = Tiling.rotate180
rotate270 = Tiling.rotate270

point_placement_no_database_only = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [all_point_insertions],
                       [requirement_corroboration]],
         name="point_placement_no_database")

point_placement_only = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [all_point_insertions],
                       [requirement_corroboration]],
         name="point_placement")

length_2_requirement_with_point_placement_no_database = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [partial(all_cell_insertions, maxreqlen=2)],
                       [requirement_placement], [requirement_corroboration]],
         name="length_2_requirement_with_point_placement_no_database")

length_2_requirement_with_point_placement = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [partial(all_cell_insertions, maxreqlen=2)],
                       [requirement_placement], [requirement_corroboration]],
         name="length_2_requirement_with_point_placement")

length_2_requirement_with_pattern_placement_no_database = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=2),
                        partial(all_requirement_extensions, maxreqlen=2)],
                       [requirement_corroboration]],
         name="length_2_requirement_with_pattern_placement_no_database")

length_2_requirement_with_pattern_placement = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=2),
                        partial(all_requirement_extensions, maxreqlen=2)],
                       [requirement_corroboration]],
         name="length_2_requirement_with_pattern_placement")

length_3_requirement_with_point_placement_no_database = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [partial(all_cell_insertions, maxreqlen=3)],
                       [requirement_placement], [requirement_corroboration]],
         name="length_3_requirement_with_point_placement_no_database")

length_3_requirement_with_point_placement = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [partial(all_cell_insertions, maxreqlen=3)],
                       [requirement_placement], [requirement_corroboration]],
         name="length_3_requirement_with_point_placement")

length_3_requirement_with_pattern_placement_no_database = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         name="length_3_requirement_with_pattern_placement_no_database")

length_3_requirement_with_pattern_placement = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         name="length_3_requirement_with_pattern_placement")

fundamental_point_placement = StrategyPack(
         eq_strats=[point_placement],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor], [all_point_insertions],
                       [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_point_placement")

fundamental_length_2_requirement_with_point_placement = StrategyPack(
         eq_strats=[],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor],
                       [partial(all_cell_insertions, maxreqlen=2)],
                       [requirement_placement], [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_2_requirement_with_point_placement")

fundamental_length_2_requirement_with_pattern_placement = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor],
                       [partial(all_cell_insertions, maxreqlen=2),
                        partial(all_requirement_extensions, maxreqlen=2)],
                       [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_2_requirement_with_pattern_placement")

fundamental_length_3_requirement_with_point_placement = StrategyPack(
         eq_strats=[],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor],
                       [partial(all_cell_insertions, maxreqlen=3)],
                       [requirement_placement], [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_3_requirement_with_point_placement")

fundamental_length_3_requirement_with_pattern_placement = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[factor],
                       [partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_3_requirement_with_pattern_placement")

fundamental_row_placements_symmetries = StrategyPack(
        eq_strats=[],
        ver_strats=[partial(fundamentally_verified, symmetry=True)],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor], [insertion_encoding]],
        iterative=True,
        forward_equivalence=True,
        symmetries = [reverse, rotate180, complement],
        name="fundamental_row_placements_symmetries"
)

fundamental_row_placements_top_and_bottom = StrategyPack(
        eq_strats=[],
        ver_strats=[partial(fundamentally_verified, symmetry=True)],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor],
                      [insertion_encoding]],
        iterative=True,
        forward_equivalence=True,
        symmetries = [complement],
        name="fundamental_row_placements_top_and_bottom"
)

fundamental_point_placement_no_factors = StrategyPack(
         eq_strats=[point_placement],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[all_point_insertions],
                       [requirement_corroboration]],
         iterative=True,
         name="fundamental_point_placement_no_factors")

fundamental_length_2_requirement_with_point_placement_no_factors = StrategyPack(
         eq_strats=[],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(all_cell_insertions, maxreqlen=2)],
                       [requirement_placement], [requirement_corroboration]],
         iterative=True,
         name="fundamental_length_2_requirement_with_point_placement_no_factors")

fundamental_length_2_requirement_with_pattern_placement_no_factors = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(all_cell_insertions, maxreqlen=2),
                        partial(all_requirement_extensions, maxreqlen=2)],
                       [requirement_corroboration]],
         iterative=True,
         name="fundamental_length_2_requirement_with_pattern_placement_no_factors")

fundamental_length_3_requirement_with_point_placement_no_factors = StrategyPack(
         eq_strats=[],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(all_cell_insertions, maxreqlen=3)],
                       [requirement_placement], [requirement_corroboration]],
         iterative=True,
         name="fundamental_length_3_requirement_with_point_placement_no_factors")

fundamental_length_3_requirement_with_pattern_placement_no_factors = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         iterative=True,
         name="fundamental_length_3_requirement_with_pattern_placement_no_factors")

fundamental_row_placements_symmetries_no_factors = StrategyPack(
        eq_strats=[],
        ver_strats=[partial(fundamentally_verified, symmetry=True)],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[insertion_encoding]],
        iterative=True,
        symmetries = [reverse, rotate180, complement],
        name="fundamental_row_placements_symmetries_no_factors"
)

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
        other_strats=[[factor], [insertion_encoding]],
        symmetries = [reverse, rotate180, complement],
        name="regular_insertion_encoding_symmetries"
)

regular_insertion_encoding_top_and_bottom = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[],
        other_strats=[[factor],
                      [insertion_encoding]],
        symmetries = [complement],
        name="regular_insertion_encoding_top_and_bottom"
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
        other_strats=[[factor], [insertion_encoding]],
        symmetries = [reverse, rotate180, complement],
        name="better_insertion_encoding_symmetries"
)

better_insertion_encoding_top_and_bottom = StrategyPack(
        eq_strats=[],
        ver_strats=[verify_points],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor],
                      [insertion_encoding]],
        symmetries = [complement],
        name="better_insertion_encoding_top_and_bottom"
)

super_insertion_encoding = StrategyPack(
        eq_strats=[],
        ver_strats=[globally_verified],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor], [insertion_encoding]],
        name="super_insertion_encoding"
)

super_insertion_encoding_sym = StrategyPack(
        eq_strats=[],
        ver_strats=[partial(globally_verified, symmetry=True)],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor], [insertion_encoding]],
        symmetries = [reverse, rotate180, complement],
        name="super_insertion_encoding_sym"
)

super_insertion_encoding_tab = StrategyPack(
        eq_strats=[],
        ver_strats=[partial(globally_verified, symmetry=True)],
        inf_strats=[obstruction_transitivity, row_and_column_separation],
        other_strats=[[factor],
                      [insertion_encoding]],
        symmetries = [complement],
        name="super_insertion_encoding_tab"
)


natural_point_placement_no_database_only = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, workable=False, unions=True)],
                       [all_point_insertions],
                       [requirement_corroboration]],
         name="natural_point_placement_no_database")

natural_length_2_requirement_with_point_placement_no_database = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, workable=False, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=2)],
                       [requirement_placement], [requirement_corroboration]],
         name="natural_length_2_requirement_point_placement_no_database")

natural_length_2_requirement_with_pattern_placement_no_database = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, workable=False, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=2),
                        partial(all_requirement_extensions, maxreqlen=2)],
                       [requirement_corroboration]],
         name="natural_length_2_requirement_pattern_placement_no_database")

natural_length_3_requirement_with_point_placement_no_database = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, workable=False, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=3)],
                       [requirement_placement], [requirement_corroboration]],
         name="natural_length_3_requirement_point_placement_no_database")

natural_length_3_requirement_with_pattern_placement_no_database = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, workable=False, unions=True)],
                       [partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         name="natural_length_3_requirement_pattern_placement_no_database")

point_placement_no_database_interleaving = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, interleaving=True)],
                       [all_point_insertions], [requirement_corroboration]],
         forward_equivalence=True,
         name="point_placement_no_database_interleaving")

length_2_requirement_with_point_placement_no_database_interleaving = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, interleaving=True)],
                       [partial(all_cell_insertions, maxreqlen=2)],
                       [requirement_placement], [requirement_corroboration]],
         forward_equivalence=True,
         name="length_2_requirement_with_point_placement_no_database_interleaving")

length_2_requirement_with_pattern_placement_no_database_interleaving = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, unions=True, interleaving=True)],
                       [partial(all_cell_insertions, maxreqlen=2),
                        partial(all_requirement_extensions, maxreqlen=2)],
                       [requirement_corroboration]],
         forward_equivalence=True,
         name="length_2_requirement_with_pattern_placement_no_database_interleaving")

length_3_requirement_with_point_placement_no_database_interleaving = StrategyPack(
         eq_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, interleaving=True)],
                       [partial(all_cell_insertions, maxreqlen=3)],
                       [requirement_placement], [requirement_corroboration]],
         forward_equivalence=True,
         name="length_3_requirement_with_point_placement_no_database_interleaving")

length_3_requirement_with_pattern_placement_no_database_interleaving = StrategyPack(
         eq_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inf_strats=[empty_cell_inferral, obstruction_transitivity,
                     row_and_column_separation],
         other_strats=[[partial(factor, unions=True, interleaving=True)],
                       [partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         forward_equivalence=True,
         name="length_3_requirement_with_pattern_placement_no_database_interleaving")
