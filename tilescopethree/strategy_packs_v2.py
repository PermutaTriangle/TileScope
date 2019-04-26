from comb_spec_searcher import StrategyPack
from comb_spec_searcher.utils import get_func_name
from grids_three import Tiling
from functools import partial
from tilescopethree.strategies import (all_cell_insertions,
                                       all_col_insertions, all_row_insertions,
                                       col_placements as col_placements_strat,
                                       database_verified, elementary_verified,
                                       factor, fusion,
                                       fusion_with_interleaving,
                                       globally_verified,
                                       obstruction_transitivity,
                                       one_by_one_verification,
                                       partial_requirement_placement,
                                       requirement_corroboration,
                                       requirement_list_placement,
                                       requirement_placement,
                                       root_requirement_insertion,
                                       row_and_column_separation,
                                       row_placements as row_placements_strat,
                                       subobstruction_inferral,
                                       subclass_verified,
                                       subset_verified, verify_points)

import importlib

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
                              symmetries=self.symmetries,
                              forward_equivalence=self.forward_equivalence,
                              iterative=self.iterative)

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
                              symmetries=self.symmetries,
                              forward_equivalence=self.forward_equivalence,
                              iterative=self.iterative)

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
                              symmetries=self.symmetries,
                              forward_equivalence=self.forward_equivalence,
                              iterative=self.iterative)

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
                              symmetries=symmetries,
                              forward_equivalence=self.forward_equivalence,
                              iterative=self.iterative)

    def make_elementary(self):
        if ([elementary_verified] == self.ver_strats and
                self.forward_equivalence and self.iterative):
            raise ValueError("The pack is already elementary.")
        name = "elementary_" + self.name
        return self.__class__(self.initial_strats,
                              self.inferral_strats,
                              self.expansion_strats,
                              [elementary_verified], name,
                              symmetries=self.symmetries,
                              forward_equivalence=True,
                              iterative=True)

    def make_fusion(self, interleaving=False):
        try:
            if interleaving:
                with_fuse = self.add_initial(fusion_with_interleaving)
            else:
                with_fuse = self.add_initial(fusion)
        except ValueError as e:
            raise ValueError(e)
        with_fuse.forward_equivalence = True
        return with_fuse

    # The base packs are given as class methods below.

    @classmethod
    def all_the_strategies(cls, length=1):
        return TileScopePack(
                initial_strats=[partial(factor, unions=True)],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[partial(all_cell_insertions,
                                           maxreqlen=length),
                                   all_row_insertions,
                                   all_col_insertions],
                                  [row_placements_strat,
                                   col_placements_strat,
                                   partial(row_placements_strat,
                                           positive=False),
                                   partial(col_placements_strat,
                                           positive=False),
                                   partial_requirement_placement,
                                   requirement_placement,
                                   requirement_list_placement],
                                  [requirement_corroboration]],
                name="all_the_strategies")

    @classmethod
    def pattern_placements(cls, length=1, partial_placements=False):
        if not isinstance(length, int) or length < 1:
            raise ValueError("The length {} makes no sense".format(length))
        placement = (partial_requirement_placement
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
        placement = (partial_requirement_placement
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
    def regular_insertion_encoding(cls, direction=None):
        """This pack finds insertion encodings."""
        if direction in [1, 3]:
            expansion_strats = [partial(row_placements_strat,
                                        positive=True,
                                        direction=direction)]
        elif direction in [0, 2]:
            expansion_strats = [partial(col_placements_strat,
                                        positive=True,
                                        direction=direction)]
        else:
            raise ValueError("Must be direction in {0, 1, 2, 3}.")
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration,
                                partial(all_cell_insertions,
                                        ignore_parent=True)],
                ver_strats=[verify_points],
                inferral_strats=[],
                expansion_strats=[expansion_strats],
                name="regular_insertion_encoding_{}".format(
                                                "left" if direction == 0 else
                                                "bottom" if direction == 1 else
                                                "right" if direction == 2 else
                                                "top"))

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
    @classmethod
    def insertion_row_and_col_placements(cls, row_only=False, col_only=False):
        if row_only and col_only:
            raise ValueError("Can't be row and col only.")
        both = not (row_only or col_only)
        expansion_strats = []
        if not col_only:
            expansion_strats.append(partial(row_placements_strat,
                                            positive=True))
        if not row_only:
            expansion_strats.append(partial(col_placements_strat,
                                            positive=True))
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration,
                                partial(all_cell_insertions,
                                        ignore_parent=True)],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[expansion_strats],
                name="insertion_{}{}{}_placements".format(
                                                "row" if not col_only else "",
                                                "_and_" if both else "",
                                                "col" if not row_only else ""))

    @classmethod
    def only_root_placements(cls, length=1):
        return TileScopePack(
            initial_strats=[partial(requirement_placement,
                                    ignore_parent=True),
                            factor],
            ver_strats=[verify_points,
                        partial(subset_verified,
                                no_factors=True, no_reqs=True)],
            inferral_strats=[row_and_column_separation,
                             obstruction_transitivity],
            expansion_strats=[[partial(root_requirement_insertion,
                                       maxreqlen=length)]],
            name="only_length_{}_root_placements".format(length)
        )


basepacks = [
    TileScopePack.insertion_row_and_col_placements(col_only=True),
    TileScopePack.insertion_row_and_col_placements(row_only=True),
    TileScopePack.insertion_row_and_col_placements(),
    TileScopePack.row_and_col_placements(col_only=True),
    TileScopePack.row_and_col_placements(row_only=True),
    TileScopePack.row_and_col_placements(),
    TileScopePack.point_placements(partial_placements=True),
    TileScopePack.point_placements(),
    TileScopePack.pattern_placements(4),
    TileScopePack.point_placements(4),
    TileScopePack.only_root_placements(2),
    TileScopePack.only_root_placements(3),
    TileScopePack.only_root_placements(4),
    TileScopePack.all_the_strategies(),
    TileScopePack.regular_insertion_encoding(0),
    TileScopePack.regular_insertion_encoding(1),
    TileScopePack.regular_insertion_encoding(2),
    TileScopePack.regular_insertion_encoding(3),
]

length_3_root_placements_pp = TileScopePack.point_placements().add_initial(
                            partial(root_requirement_insertion, maxreqlen=3))
length_4_root_placements_pp = TileScopePack.point_placements().add_initial(
                            partial(root_requirement_insertion, maxreqlen=4))
length_3_root_placements_pp.name = "length_3_root_placements_pp"
length_4_root_placements_pp.name = "length_4_root_placements_pp"
basepacks.append(length_3_root_placements_pp)
basepacks.append(length_4_root_placements_pp)

length_3_root_placements_pp = TileScopePack.pattern_placements().add_initial(
                            partial(root_requirement_insertion, maxreqlen=3))
length_4_root_placements_pp = TileScopePack.pattern_placements().add_initial(
                            partial(root_requirement_insertion, maxreqlen=4))
length_3_root_placements_pp.name = "length_3_root_pattern_pp"
length_4_root_placements_pp.name = "length_4_root_pattern_pp"
basepacks.append(length_3_root_placements_pp)
basepacks.append(length_4_root_placements_pp)

length_3_root_placements_rc = TileScopePack.row_and_col_placements().add_initial(
                            partial(root_requirement_insertion, maxreqlen=3))
length_4_root_placements_rc = TileScopePack.row_and_col_placements().add_initial(
                            partial(root_requirement_insertion, maxreqlen=4))
length_3_root_placements_rc.name = "length_3_root_placements_rc"
length_4_root_placements_rc.name = "length_4_root_placements_rc"
basepacks.append(length_3_root_placements_rc)
basepacks.append(length_4_root_placements_rc)

module = importlib.import_module(TileScopePack.__module__)

for pack in basepacks:
    fusion_pack = pack.make_fusion()
    fusion_datab = fusion_pack.add_verification(database_verified)
    fusion_scv = fusion_pack.add_verification(subclass_verified)
    other_fusion = pack.make_fusion(interleaving=True)
    other_fusion_datab = other_fusion.add_verification(database_verified)
    unreasonable_fusion = other_fusion.make_fusion()
    setattr(module, fusion_pack.name, fusion_pack)
    setattr(module, fusion_datab.name, fusion_datab)
    setattr(module, fusion_scv.name, fusion_scv)
    setattr(module, other_fusion.name, other_fusion)
    setattr(module, other_fusion_datab.name, other_fusion_datab)
    setattr(module, unreasonable_fusion.name, unreasonable_fusion)
delattr(module, 'fusion_pack')
delattr(module, 'fusion_datab')
delattr(module, 'other_fusion')
delattr(module, 'other_fusion_datab')
delattr(module, 'unreasonable_fusion')

for pack in basepacks:
    new_packs = [pack]
    for new_pack in tuple(new_packs):
        new_packs.append(new_pack.add_verification(database_verified))
    for new_pack in tuple(new_packs):
        new_packs.append(new_pack.add_symmetry())
    for new_pack in tuple(new_packs):
        new_packs.append(new_pack.add_inferral(subobstruction_inferral))
    for new_pack in new_packs:
        setattr(module, new_pack.name, new_pack)

delattr(module, 'pack')
delattr(module, 'new_pack')

restricted_fusion = TileScopePack(
                initial_strats=[factor, fusion, requirement_placement],
                inferral_strats=[row_and_column_separation],
                expansion_strats=[[all_cell_insertions,
                                   partial(row_placements_strat, positive=False),
                                   partial(col_placements_strat, positive=False)]],
                ver_strats=[one_by_one_verification],
                forward_equivalence=True,
                name="restricted_fusion")