from comb_spec_searcher import StrategyPack
from comb_spec_searcher.utils import get_func_name
from tilings import Tiling
from functools import partial
from tilescopethree.strategies import (all_cell_insertions,
                                       all_requirement_insertions,
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
                initial_strats=[partial(factor, unions=True),
                                requirement_corroboration],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[partial(all_cell_insertions,
                                           maxreqlen=length),
                                   all_row_insertions,
                                   all_col_insertions,
                                   all_requirement_insertions],
                                  [partial(row_placements_strat,
                                           positive=False),
                                   partial(col_placements_strat,
                                           positive=False),
                                   partial_requirement_placement,
                                   requirement_placement]],
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

    @classmethod
    def requirement_placements(cls, length=2, partial_placements=False):
        if not isinstance(length, int) or length < 1:
            raise ValueError("The length {} makes no sense".format(length))
        placement = (partial_requirement_placement
                     if partial_placements else requirement_placement)
        return TileScopePack(
                initial_strats=[factor, requirement_corroboration],
                ver_strats=[subset_verified, globally_verified],
                inferral_strats=[row_and_column_separation,
                                 obstruction_transitivity],
                expansion_strats=[[partial(all_requirement_insertions,
                                           maxlen=length)],
                                  [placement]],
                name="{}{}requirement_placements".format(
                            "length_{}_".format(length) if length != 2 else "",
                            "partial_" if partial_placements else ""))


basepacks = [
    TileScopePack.insertion_row_and_col_placements(col_only=True),
    TileScopePack.insertion_row_and_col_placements(row_only=True),
    TileScopePack.insertion_row_and_col_placements(),
    TileScopePack.insertion_point_placements(),
    TileScopePack.row_and_col_placements(col_only=True),
    TileScopePack.row_and_col_placements(row_only=True),
    TileScopePack.row_and_col_placements(),
    TileScopePack.point_placements(partial_placements=True),
    TileScopePack.point_placements(),
    TileScopePack.pattern_placements(2),
    TileScopePack.pattern_placements(3),
    TileScopePack.pattern_placements(4),
    TileScopePack.point_placements(2),
    TileScopePack.point_placements(3),
    TileScopePack.point_placements(4),
    TileScopePack.point_placements(partial_placements=True),
    TileScopePack.requirement_placements(),
    TileScopePack.requirement_placements(3),
    TileScopePack.requirement_placements(4),
    TileScopePack.requirement_placements(partial_placements=True),
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

from comb_spec_searcher import VerificationRule
from tilings import *
from permuta import *

f7 = Tiling(obstructions=(Obstruction(Perm((0,)), ((0, 1),)), Obstruction(Perm((0,)), ((0, 2),)), Obstruction(Perm((1, 0)), ((1, 1), (1, 1))), Obstruction(Perm((1, 0)), ((1, 2), (1, 1))), Obstruction(Perm((1, 0)), ((1, 2), (1, 2))), Obstruction(Perm((0, 2, 1)), ((0, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 2)), ((0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 1), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 2), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 1), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 2), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 1), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 2), (1, 0)))), requirements=())

# til2 = Tiling(obstructions=(Obstruction(Perm((0,)), ((0, 1),)), Obstruction(Perm((0,)), ((0, 2),)), Obstruction(Perm((0,)), ((0, 3),)), Obstruction(Perm((1, 0)), ((1, 1), (1, 1))), Obstruction(Perm((1, 0)), ((1, 2), (1, 1))), Obstruction(Perm((1, 0)), ((1, 2), (1, 2))), Obstruction(Perm((1, 0)), ((1, 3), (1, 1))), Obstruction(Perm((1, 0)), ((1, 3), (1, 2))), Obstruction(Perm((1, 0)), ((1, 3), (1, 3))), Obstruction(Perm((0, 2, 1)), ((0, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 2)), ((0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 1), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 2), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 3), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 1), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 2), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 3), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 1), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 2), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 3), (1, 0)))), requirements=((Requirement(Perm((0,)), ((1, 2),)),),))

# til3 = Tiling(obstructions=(Obstruction(Perm((0,)), ((0, 0),)), Obstruction(Perm((0,)), ((0, 3),)), Obstruction(Perm((0,)), ((1, 1),)), Obstruction(Perm((0,)), ((1, 2),)), Obstruction(Perm((0,)), ((1, 3),)), Obstruction(Perm((0,)), ((2, 1),)), Obstruction(Perm((1, 0)), ((0, 1), (0, 1))), Obstruction(Perm((1, 0)), ((0, 2), (0, 2))), Obstruction(Perm((1, 0)), ((2, 2), (2, 2))), Obstruction(Perm((1, 0)), ((2, 3), (2, 2))), Obstruction(Perm((1, 0)), ((2, 3), (2, 3))), Obstruction(Perm((0, 2, 1)), ((1, 0), (2, 0), (2, 0))), Obstruction(Perm((1, 0, 2)), ((0, 2), (0, 1), (2, 2))), Obstruction(Perm((1, 0, 2)), ((1, 0), (1, 0), (2, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 0), (1, 0), (2, 0))), Obstruction(Perm((0, 3, 2, 1)), ((2, 0), (2, 0), (2, 0), (2, 0))), Obstruction(Perm((0, 3, 2, 1)), ((2, 0), (2, 2), (2, 0), (2, 0))), Obstruction(Perm((0, 3, 2, 1)), ((2, 0), (2, 3), (2, 0), (2, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (2, 0), (2, 2), (2, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (2, 0), (2, 3), (2, 0))), Obstruction(Perm((1, 0, 3, 2)), ((2, 0), (2, 0), (2, 0), (2, 0))), Obstruction(Perm((1, 0, 3, 2)), ((2, 0), (2, 0), (2, 2), (2, 0))), Obstruction(Perm((1, 0, 3, 2)), ((2, 0), (2, 0), (2, 3), (2, 0)))), requirements=())

# tils = [row_and_column_separation(t).comb_classes[0] for t in (til1, til2, til3) if row_and_column_separation(t) is not None]
# print(len(tils))

f3 = Tiling(obstructions=(Obstruction(Perm((1, 0)), ((0, 1), (0, 1))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 1), (0, 0), (0, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (0, 0), (0, 1), (0, 0)))), requirements=())

f14 = Tiling(obstructions=(Obstruction(Perm((0,)), ((0, 1),)), Obstruction(Perm((1, 0)), ((1, 1), (1, 1))), Obstruction(Perm((0, 2, 1)), ((0, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 2)), ((0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 1), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 1), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 1), (1, 0)))), requirements=())

f8 = Tiling(obstructions=(Obstruction(Perm((0,)), ((0, 1),)), Obstruction(Perm((0,)), ((0, 2),)), Obstruction(Perm((0,)), ((0, 3),)), Obstruction(Perm((1, 0)), ((1, 1), (1, 1))), Obstruction(Perm((1, 0)), ((1, 2), (1, 1))), Obstruction(Perm((1, 0)), ((1, 2), (1, 2))), Obstruction(Perm((1, 0)), ((1, 3), (1, 1))), Obstruction(Perm((1, 0)), ((1, 3), (1, 2))), Obstruction(Perm((1, 0)), ((1, 3), (1, 3))), Obstruction(Perm((0, 2, 1)), ((0, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 2)), ((0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((0, 3, 2, 1)), ((0, 0), (0, 0), (0, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 1), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 2), (1, 0), (1, 0))), Obstruction(Perm((0, 3, 2, 1)), ((1, 0), (1, 3), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (0, 0), (0, 0), (0, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 1), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 2), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((0, 0), (1, 0), (1, 3), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 0), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 1), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 2), (1, 0))), Obstruction(Perm((1, 0, 3, 2)), ((1, 0), (1, 0), (1, 3), (1, 0)))), requirements=((Requirement(Perm((0,)), ((1, 2),)),),))


def fake_verify(tiling, **kwargs):
    #if tiling == f7:
    #    print("="*20 + "VERIFIED" + "="*20)
    #    print(f7)
    #    return VerificationRule('fake verified')
    #if tiling == f3:
    #    print("="*20 + "VERIFIED" + "="*20)
    #    print(f3)
    #    return VerificationRule('fake_verified')
    if tiling == f14:
        print("="*20 + "VERIFIED" + "="*20)
        print(f14)
        return VerificationRule('fake_verified')
    #if tiling == f8:
    #    print("="*20 + "VERIFIED" + "="*20)
    #    print(f8)
    #    return VerificationRule('fake_verified')
    # if tiling == til2:
    #     print(til2)
    #     print("="*20 + "VERIFIED2" + "="*20)
    #     return VerificationRule('fake verified')
    # if tiling == til3:
    #     print(til3)
    #     print("="*20 + "VERIFIED3" + "="*20)
    #     return VerificationRule('fake verified')
    # if tiling in tils:
    #     print("="*20 + "VERIFIEDs" + "="*20)
    #     return VerificationRule('fake verified')

from comb_spec_searcher import Strategy
special = set()
def hack(tiling, **kwargs):
    if tiling in special:
        print("Shortcutting to place 1324")
        print(tiling)
        for s in requirement_placement(tiling):
            special.update(s.comb_classes)
            yield s
    if tiling == f14:
        gp = Obstruction(Perm((0, 2, 1, 3)), ((0, 0), (0, 0), (1, 0), (1, 0)))
        print("inserting {} into".format(str(gp)))
        print(tiling)
        av = Tiling((tiling.obstructions +
                    (Obstruction(gp.patt, gp.pos),)),
                    tiling.requirements)
        co = Tiling(tiling.obstructions,
                    (tiling.requirements) +
                    ((Requirement(gp.patt, gp.pos),),))
        special.add(co)
        yield Strategy(formal_step="Insert {}.".format(str(gp)),
                        comb_classes=[av, co],
                        ignore_parent=False,
                        inferable=[True for _ in range(2)],
                        possibly_empty=[True for _ in range(2)],
                        workable=[True for _ in range(2)],
                        constructor='disjoint')

from tilescopethree.strategies.equivalence_strategies.fusion_with_point_req import fusion_with_point_req 

hack_pack = TileScopePack(
    initial_strats=[hack, partial(factor, interleaving=True, unions=True), requirement_corroboration, fusion],
    inferral_strats=[row_and_column_separation, obstruction_transitivity],
    expansion_strats=[[partial(all_requirement_insertions, no_reqs=True, maxlen=2), requirement_placement]],
    ver_strats=[subset_verified, globally_verified],
    forward_equivalence=True,
    name="hack_pack")

try_everything2 = TileScopePack(
    initial_strats=[partial(factor, interleaving=True, unions=True), requirement_corroboration, fusion_with_point_req],
    inferral_strats=[row_and_column_separation, obstruction_transitivity],
    expansion_strats=[[partial(all_requirement_insertions, no_reqs=True, maxlen=2), requirement_placement]],
    ver_strats=[subset_verified, globally_verified],
    forward_equivalence=True,
    name="try_everything2")

try_everything3 = TileScopePack(
    initial_strats=[partial(factor, interleaving=True, unions=True), requirement_corroboration, fusion_with_point_req],
    inferral_strats=[row_and_column_separation, obstruction_transitivity],
    expansion_strats=[[partial(all_requirement_insertions, no_reqs=True, maxlen=3), requirement_placement]],
    ver_strats=[subset_verified, globally_verified],
    forward_equivalence=True,
    name="try_everything3")

try_everything4 = TileScopePack(
    initial_strats=[partial(factor, interleaving=True, unions=True), requirement_corroboration, fusion_with_point_req],
    inferral_strats=[row_and_column_separation, obstruction_transitivity],
    expansion_strats=[[partial(all_requirement_insertions, no_reqs=True, maxlen=4), requirement_placement]],
    ver_strats=[subset_verified, globally_verified],
    forward_equivalence=True,
    name="try_everything4")
