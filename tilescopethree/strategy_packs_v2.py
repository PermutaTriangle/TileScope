from comb_spec_searcher import StrategyPack
from comb_spec_searcher.utils import get_func_name
from grids_three import Tiling
from functools import partial
from tilescopethree.strategies import (all_cell_insertions, col_placements,
                                       database_verified, factor,
                                       fundamentally_verified,
                                       globally_verified,
                                       obstruction_transitivity,
                                       partial_point_placement,
                                       requirement_corroboration,
                                       requirement_placement,
                                       row_and_column_separation,
                                       row_placements, subset_verified)

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

    def make_fundamental(self):
        if ([fundamentally_verified] == self.ver_strats and
                self.forward_equivalence and self.iterative):
            raise ValueError("The pack is already fundamental.")
        name = "fundamental_" + self.name
        return self.__class__(self.initial_strats,
                              self.inferral_strats,
                              self.expansion_strats,
                              [fundamentally_verified], name,
                              symmetries = self.symmetries,
                              forward_equivalence = True,
                              iterative = True)

    # The base packs are given as class methods below.

    @classmethod
    def pattern_placements(cls, length=1):
        if not isinstance(length, int) or length < 1:
            raise ValueError("The length {} makes no sense".format(length))
        return TileScopePack(
                initial_strats=[requirement_placement],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[partial(factor, unions=True)],
                                  [partial(all_cell_insertions,
                                           maxreqlen=length)],
                                  [requirement_corroboration]],
                name="{}{}_placements".format("length_{}".format(length)
                                              if length > 1 else "",
                                              "pattern"
                                              if length > 1 else "point"))

    @classmethod
    def point_placements(cls, length=1):
        if not isinstance(length, int) or length < 1:
            raise ValueError("The length {} makes no sense".format(length))
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[partial(all_cell_insertions,
                                           maxreqlen=length)],
                                  [requirement_placement]],
                name="{}point_placements".format("length_{}_".format(length)
                                                 if length > 1 else ""))

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
            expansion_strats.append(partial(row_placements, positive=False))
        if not row_only:
            expansion_strats.append(partial(col_placements, positive=False))
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                obstruction_transitivity],
                expansion_strats=[expansion_strats],
                name="{}{}{}_placements".format("row" if not col_only else "",
                                                "_and_" if both else "",
                                                "col" if not row_only else ""))


if __name__ == "__main__":
    print("HERE")
    point_placements = TileScopePack.row_and_col_placements(col_only=True)

    print(point_placements.name)

    print(point_placements)