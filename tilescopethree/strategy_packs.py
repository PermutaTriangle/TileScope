from comb_spec_searcher import StrategyPack as Pack
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
                                       subset_verified, insertion_encoding,
                                       subclass_verified)

point_placements = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor], [all_point_insertions],
                           [requirement_corroboration]],
         name="point_placements")

point_placements_scv = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified, subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor], [all_point_insertions],
                           [requirement_corroboration]],
         name="point_placements_scv")

point_placements_db = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor], [all_point_insertions],
                           [requirement_corroboration]],
         name="point_placements_db")

insertion_point_placements_scv = Pack(
         initial_strats=[factor, requirement_corroboration,
                         partial(all_point_insertions, ignore_parent=True)],
         ver_strats=[subset_verified, globally_verified,
                     subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[requirement_placement]],
         name="insertion_point_placements_scv")

insertion_point_placements_db = Pack(
         initial_strats=[factor, requirement_corroboration,
                         partial(all_point_insertions, ignore_parent=True)],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[requirement_placement]],
         name="insertion_point_placements_db")

length_2_requirement_with_point_placements = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=2)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="length_2_requirement_with_point_placements")

length_2_requirement_with_point_placements_scv = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified,
                     subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=2)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="length_2_requirement_with_point_placements_scv")

length_2_requirement_with_point_placements_db = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=2)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="length_2_requirement_with_point_placements_db")

insertion_length_2_requirement_with_point_placements_scv = Pack(
         initial_strats=[factor, requirement_corroboration,
                         partial(all_cell_insertions, maxreqlen=2,
                                 ignore_parent=True)],
         ver_strats=[subset_verified, globally_verified,
                     subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[requirement_placement]],
         name="insertion_length_2_requirement_with_point_placements_scv")

insertion_length_2_requirement_with_point_placements_db = Pack(
         initial_strats=[factor, requirement_corroboration,
                         partial(all_cell_insertions, maxreqlen=2,
                                 ignore_parent=True)],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[requirement_placement]],
         name="insertion_length_2_requirement_with_point_placements_db")

length_2_requirement_with_pattern_placements = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=2),
                            partial(all_requirement_extensions, maxreqlen=2)],
                           [requirement_corroboration]],
         name="length_2_requirement_with_pattern_placements")

length_2_requirement_with_pattern_placements_scv = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=2),
                            partial(all_requirement_extensions, maxreqlen=2)],
                           [requirement_corroboration]],
         name="length_2_requirement_with_pattern_placements_scv")

length_2_requirement_with_pattern_placements_db = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=2),
                            partial(all_requirement_extensions, maxreqlen=2)],
                           [requirement_corroboration]],
         name="length_2_requirement_with_pattern_placements_db")

length_3_requirement_with_point_placements = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=3)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="length_3_requirement_with_point_placements")

length_3_requirement_with_point_placements_scv = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified,
                     subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=3)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="length_3_requirement_with_point_placements_scv")

length_3_requirement_with_point_placements_db = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=3)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="length_3_requirement_with_point_placements_db")

insertion_length_3_requirement_with_point_placements_db = Pack(
         initial_strats=[factor, requirement_corroboration,
                         partial(all_cell_insertions, maxreqlen=3,
                                 ignore_parent=True)],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[requirement_placement]],
         name="length_3_requirement_with_point_placements_db")

insertion_length_3_requirement_with_point_placements_scv = Pack(
         initial_strats=[factor, requirement_corroboration,
                         partial(all_cell_insertions, maxreqlen=3,
                                 ignore_parent=True)],
         ver_strats=[subset_verified, globally_verified,
                     subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[requirement_placement]],
         name="length_3_requirement_with_point_placements_scv")

length_3_requirement_with_pattern_placements = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=3),
                            partial(all_requirement_extensions, maxreqlen=3)],
                           [requirement_corroboration]],
         name="length_3_requirement_with_pattern_placements")

length_3_requirement_with_pattern_placements_db = Pack(
         initial_strats=[factor, requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     database_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[
                       [partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         name="length_3_requirement_with_pattern_placements_db")

length_3_requirement_with_pattern_placements_scv = Pack(
         initial_strats=[factor, requirement_placement],
         ver_strats=[subset_verified, globally_verified,
                     subclass_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[
                       [partial(all_cell_insertions, maxreqlen=3),
                        partial(all_requirement_extensions, maxreqlen=3)],
                       [requirement_corroboration]],
         name="length_3_requirement_with_pattern_placements_scv")

fundamental_point_placement = Pack(
         initial_strats=[point_placement],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor], [all_point_insertions],
                           [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_point_placement")

fundamental_length_2_requirement_with_point_placement = Pack(
         initial_strats=[],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=2)],
                           [requirement_placement],
                           [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_2_requirement_with_point_placement")

fundamental_length_2_requirement_with_pattern_placement = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=2),
                            partial(all_requirement_extensions, maxreqlen=2)],
                           [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_2_requirement_with_pattern_placement")

fundamental_length_3_requirement_with_point_placement = Pack(
         initial_strats=[],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=3)],
                           [requirement_placement],
                           [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_3_requirement_with_point_placement")

fundamental_length_3_requirement_with_pattern_placement = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[factor],
                           [partial(all_cell_insertions, maxreqlen=3),
                            partial(all_requirement_extensions, maxreqlen=3)],
                           [requirement_corroboration]],
         iterative=True,
         forward_equivalence=True,
         name="fundamental_length_3_requirement_with_pattern_placement")

fundamental_row_placements_symmetries = Pack(
        initial_strats=[],
        ver_strats=[partial(fundamentally_verified, symmetry=True)],
        inferral_strats=[obstruction_transitivity, row_and_column_separation],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True)]],
        iterative=True,
        forward_equivalence=True,
        name="fundamental_row_placements_symmetries")

fundamental_row_placements_symmetries_top_and_bottom = Pack(
        initial_strats=[],
        ver_strats=[partial(fundamentally_verified, symmetry=True)],
        inferral_strats=[obstruction_transitivity, row_and_column_separation],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True,
                                   top_and_bottom=True)]],
        iterative=True,
        forward_equivalence=True,
        name="fundamental_row_placements_symmetries_top_and_bottom")

fundamental_point_placement_no_factors = Pack(
         initial_strats=[point_placement],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[all_point_insertions],
                           [requirement_corroboration]],
         iterative=True,
         name="fundamental_point_placement_no_factors")

fundamental_length_2_requirement_with_point_placement_no_factors = Pack(
         initial_strats=[],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(all_cell_insertions, maxreqlen=2)],
                           [requirement_placement],
                           [requirement_corroboration]],
         iterative=True,
         name=("fundamental_length_2_requirement_with_point_placement_"
               "no_factors"))

fundamental_length_2_requirement_with_pattern_placement_no_factors = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(all_cell_insertions, maxreqlen=2),
                            partial(all_requirement_extensions, maxreqlen=2)],
                           [requirement_corroboration]],
         iterative=True,
         name=("fundamental_length_2_requirement_with_pattern_placement_"
               "no_factors"))

fundamental_length_3_requirement_with_point_placement_no_factors = Pack(
         initial_strats=[],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(all_cell_insertions, maxreqlen=3)],
                           [requirement_placement],
                           [requirement_corroboration]],
         iterative=True,
         name=("fundamental_length_3_requirement_with_point_placement_"
               "no_factors"))

fundamental_length_3_requirement_with_pattern_placement_no_factors = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[fundamentally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(all_cell_insertions, maxreqlen=3),
                            partial(all_requirement_extensions, maxreqlen=3)],
                           [requirement_corroboration]],
         iterative=True,
         name=("fundamental_length_3_requirement_with_pattern_placement_"
               "no_factors"))

fundamental_row_placements_symmetries_no_factors = Pack(
        initial_strats=[],
        ver_strats=[partial(fundamentally_verified, symmetry=True)],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[partial(insertion_encoding, symmetry=True)]],
        iterative=True,
        name="fundamental_row_placements_symmetries_no_factors")

fundamental_row_placements_symmetries_top_and_bottom_no_factors = Pack(
        initial_strats=[],
        ver_strats=[partial(fundamentally_verified, symmetry=True)],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[partial(insertion_encoding, symmetry=True,
                                   top_and_bottom=True)]],
        iterative=True,
        name="fundamental_row_placements_symmetries_top_and_bottom_no_factors")

regular_insertion_encoding = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[],
        expansion_strats=[[factor], [insertion_encoding]],
        name="regular_insertion_encoding")

regular_insertion_encoding_symmetries = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True)]],
        name="regular_insertion_encoding_symmetries")

regular_insertion_encoding_top_and_bottom = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, top_and_bottom=True)]],
        name="regular_insertion_encoding_top_and_bottom")

regular_insertion_encoding_symmetries_top_and_bottom = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True,
                                   top_and_bottom=True)]],
        name="regular_insertion_encoding_symmetries_top_and_bottom")

better_insertion_encoding = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor], [insertion_encoding]],
        name="better_insertion_encoding")

better_insertion_encoding_symmetries = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True)]],
        name="better_insertion_encoding_symmetries")

better_insertion_encoding_top_and_bottom = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, top_and_bottom=True)]],
        name="better_insertion_encoding_top_and_bottom")

better_insertion_encoding_symmetries_top_and_bottom = Pack(
        initial_strats=[],
        ver_strats=[verify_points],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True,
                                   top_and_bottom=True)]],
        name="better_insertion_encoding_symmetries_top_and_bottom")

super_insertion_encoding = Pack(
        initial_strats=[],
        ver_strats=[globally_verified],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor], [insertion_encoding]],
        name="super_insertion_encoding")

super_insertion_encoding_sym = Pack(
        initial_strats=[],
        ver_strats=[partial(globally_verified, symmetry=True)],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True)]],
        name="super_insertion_encoding_sym")

super_insertion_encoding_tab = Pack(
        initial_strats=[],
        ver_strats=[partial(globally_verified, symmetry=True)],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, top_and_bottom=True)]],
        name="super_insertion_encoding_tab")

super_insertion_encoding_sym_tab = Pack(
        initial_strats=[],
        ver_strats=[partial(globally_verified, symmetry=True)],
        inferral_strats=[row_and_column_separation, obstruction_transitivity],
        expansion_strats=[[factor],
                          [partial(insertion_encoding, symmetry=True,
                                   top_and_bottom=True)]],
        name="super_insertion_encoding_sym_tab")

natural_point_placement_no_database_only = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, workable=False, unions=True)],
                           [all_point_insertions],
                           [requirement_corroboration]],
         name="natural_point_placement_no_database")

natural_length_2_requirement_with_point_placement_no_database = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, workable=False, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=2)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="natural_length_2_requirement_point_placement_no_database")

natural_length_2_requirement_with_pattern_placement_no_database = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, workable=False, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=2),
                            partial(all_requirement_extensions, maxreqlen=2)],
                           [requirement_corroboration]],
         name="natural_length_2_requirement_pattern_placement_no_database")

natural_length_3_requirement_with_point_placement_no_database = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, workable=False, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=3)],
                           [requirement_placement],
                           [requirement_corroboration]],
         name="natural_length_3_requirement_point_placement_no_database")

natural_length_3_requirement_with_pattern_placement_no_database = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, workable=False, unions=True)],
                           [partial(all_cell_insertions, maxreqlen=3),
                            partial(all_requirement_extensions, maxreqlen=3)],
                           [requirement_corroboration]],
         name="natural_length_3_requirement_pattern_placement_no_database")

point_placement_no_database_interleaving = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, interleaving=True)],
                           [all_point_insertions],
                           [requirement_corroboration]],
         forward_equivalence=True,
         name="point_placement_no_database_interleaving")

length_2_requirement_with_point_placement_no_database_interleaving = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, interleaving=True)],
                           [partial(all_cell_insertions, maxreqlen=2)],
                           [requirement_placement],
                           [requirement_corroboration]],
         forward_equivalence=True,
         name=("length_2_requirement_with_point_placement_"
               "no_database_interleaving"))

length_2_requirement_with_pattern_placement_no_database_interleaving = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, unions=True, interleaving=True)],
                           [partial(all_cell_insertions, maxreqlen=2),
                            partial(all_requirement_extensions, maxreqlen=2)],
                           [requirement_corroboration]],
         forward_equivalence=True,
         name=("length_2_requirement_with_pattern_placement_"
               "no_database_interleaving"))

length_3_requirement_with_point_placement_no_database_interleaving = Pack(
         initial_strats=[],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, interleaving=True)],
                           [partial(all_cell_insertions, maxreqlen=3)],
                           [requirement_placement],
                           [requirement_corroboration]],
         forward_equivalence=True,
         name=("length_3_requirement_with_point_placement_"
               "no_database_interleaving"))

length_3_requirement_with_pattern_placement_no_database_interleaving = Pack(
         initial_strats=[requirement_placement],
         ver_strats=[subset_verified, globally_verified],
         inferral_strats=[row_and_column_separation, obstruction_transitivity],
         expansion_strats=[[partial(factor, unions=True, interleaving=True)],
                           [partial(all_cell_insertions, maxreqlen=3),
                            partial(all_requirement_extensions, maxreqlen=3)],
                           [requirement_corroboration]],
         forward_equivalence=True,
         name=("length_3_requirement_with_pattern_placement_no"
               "_database_interleaving"))
