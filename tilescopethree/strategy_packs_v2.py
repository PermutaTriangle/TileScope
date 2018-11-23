from comb_spec_searcher import StrategyPack
from comb_spec_searcher.utils import get_func_name
from grids_three import Tiling
from functools import partial
from tilescopethree.strategies import (all_cell_insertions,
                                       col_placements as col_placements_strat,
                                       database_verified, elementary_verified,
                                       factor, globally_verified,
                                       obstruction_transitivity,
                                       partial_point_placement,
                                       requirement_corroboration,
                                       requirement_placement,
                                       root_requirement_insertion,
                                       row_and_column_separation,
                                       row_placements as row_placements_strat,
                                       subset_verified)

class TileScopePack(StrategyPack):

    def add_initial(self, strategy):
        if (strategy in self.initial_strats or
                any(strategy in x for x in self.expansion_strats)):
            raise ValueError(("The strategy {} is already in pack."
                              "".format(get_func_name(strategy))))

        initial_strats = self.initial_strats + [strategy]
        name = self.name + "_{}".format(get_func_name(strategy))
        return self.__class__(initial_strats,
                              self.inferral_strats,
                              self.expansion_strats,
                              self.ver_strats, name,
                              symmetries = self.symmetries,
                              forward_equivalence = self.forward_equivalence,
                              iterative = self.iterative)

    def add_inferral(self, strategy):
        if strategy in self.inferral_strats:
            raise ValueError(("The strategy {} is already in pack."
                              "".format(get_func_name(strategy))))

        inferral_strats = self.inferral_strats + [strategy]
        name = self.name + "_{}".format(get_func_name(strategy))
        return self.__class__(self.initial_strats,
                              inferral_strats,
                              self.expansion_strats,
                              self.ver_strats, name,
                              symmetries = self.symmetries,
                              forward_equivalence = self.forward_equivalence,
                              iterative = self.iterative)

    def add_verification(self, strategy):
        if strategy in self.ver_strats:
            raise ValueError(("The strategy {} is already in pack."
                              "".format(get_func_name(strategy))))

        verification_strats = self.ver_strats + [strategy]
        name = self.name + "_{}".format(get_func_name(strategy))
        return self.__class__(self.initial_strats,
                              self.inferral_strats,
                              self.expansion_strats,
                              verification_strats, name,
                              symmetries = self.symmetries,
                              forward_equivalence = self.forward_equivalence,
                              iterative = self.iterative)

    def add_symmetry(self):
        if self.symmetries:
            raise ValueError("Symmetries already turned on.")
        symmetries = [Tiling.inverse, Tiling.reverse, Tiling.complement,
                      Tiling.antidiagonal, Tiling.rotate90,
                      Tiling.rotate180, Tiling.rotate270]
        name = self.name + "_symmetries"
        return self.__class__(self.initial_strats,
                              self.inferral_strats,
                              self.expansion_strats,
                              self.ver_strats, name,
                              symmetries = symmetries,
                              forward_equivalence = self.forward_equivalence,
                              iterative = self.iterative)

    def make_elementary(self):
        if ([elementary_verified] == self.ver_strats and
                self.forward_equivalence and self.iterative):
            raise ValueError("The pack is already elementary.")
        name = "elementary_" + self.name
        return self.__class__(self.initial_strats,
                              self.inferral_strats,
                              self.expansion_strats,
                              [elementary_verified], name,
                              symmetries = self.symmetries,
                              forward_equivalence = True,
                              iterative = True)

    # The base packs are given as class methods below.

    @classmethod
    def pattern_placements(cls, length=1, partial_placements=False):
        if not isinstance(length, int) or length < 1:
            raise ValueError("The length {} makes no sense".format(length))
        placement = (partial_point_placement
                     if partial_placements else requirement_placement)
        return TileScopePack(
                initial_strats=[placement],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[partial(factor, unions=True)],
                                  [partial(all_cell_insertions,
                                           maxreqlen=length)],
                                  [requirement_corroboration]],
                name="{}{}{}_placements".format(
                            "length_{}_".format(length) if length > 1 else "",
                            "partial_" if partial_placements else "",
                            "pattern" if length > 1 else "point"))

    @classmethod
    def point_placements(cls, length=1, partial_placements=False):
        if not isinstance(length, int) or length < 1:
            raise ValueError("The length {} makes no sense".format(length))
        placement = (partial_point_placement
                     if partial_placements else requirement_placement)
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[partial(all_cell_insertions,
                                           maxreqlen=length)],
                                  [placement]],
                name="{}{}point_placements".format(
                            "length_{}_".format(length) if length > 1 else "",
                            "partial_" if partial_placements else ""))

    @classmethod
    def insertion_point_placements(cls, length=1):
        if not isinstance(length, int) or length < 1:
            raise ValueError("The length {} makes no sense".format(length))
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration,
                                partial(all_cell_insertions, maxreqlen=length,
                                        ignore_parent=True)],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[requirement_placement]],
                name=("insertion_{}point_placements"
                      "".format("length_{}_".format(length)
                                if length > 1 else "")))

    @classmethod
    def row_and_col_placements(cls, row_only=False, col_only=False):
        if row_only and col_only:
            raise ValueError("Can't be row and col only.")
        both = not (row_only or col_only)
        expansion_strats = []
        if not col_only:
            expansion_strats.append(partial(row_placements_strat,
                                            positive=False))
        if not row_only:
            expansion_strats.append(partial(col_placements_strat,
                                            positive=False))
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                obstruction_transitivity],
                expansion_strats=[expansion_strats],
                name="{}{}{}_placements".format("row" if not col_only else "",
                                                "_and_" if both else "",
                                                "col" if not row_only else ""))


col_placements = TileScopePack.row_and_col_placements(col_only=True)
row_placements = TileScopePack.row_and_col_placements(row_only=True)
row_and_col_placements = TileScopePack.row_and_col_placements()

partial_point_placements = TileScopePack.point_placements(
                                                partial_placements=True)
point_placements = TileScopePack.pattern_placements()
length_4_pattern_placements = TileScopePack.pattern_placements(4)
length_4_point_placements = TileScopePack.point_placements(4)
length_4_root_placements = point_placements.add_initial(
                        partial(root_requirement_insertion, maxreqlen=4))

row_placements_db = row_placements.add_verification(database_verified)
col_placements_db = col_placements.add_verification(database_verified)
row_and_col_placements_db = row_and_col_placements.add_verification(
                                                        database_verified)
partial_point_placements_db = partial_point_placements.add_verification(
                                                        database_verified)
point_placements_db = point_placements.add_verification(database_verified)
length_4_pattern_placements_db = \
            length_4_pattern_placements.add_verification(database_verified)
length_4_point_placements_db = \
            length_4_point_placements.add_verification(database_verified)
length_4_root_placements_db = \
            length_4_root_placements.add_verification(database_verified)

row_placements_db_sym = row_placements_db.add_symmetry()
col_placements_db_sym = col_placements_db.add_symmetry()
row_and_col_placements_db_sym = row_and_col_placements_db.add_symmetry()
partial_point_placements_db_sym = \
                            partial_point_placements_db.add_symmetry()
point_placements_db_sym = point_placements_db.add_symmetry()
length_4_pattern_placements_db_sym = \
                            length_4_pattern_placements_db.add_symmetry()
length_4_point_placements_db_sym = \
                            length_4_point_placements_db.add_symmetry()
length_4_root_placements_db_sym = \
                            length_4_root_placements_db.add_symmetry()
