import pytest

from comb_spec_searcher import Rule
from permuta import Perm
from tilescopethree.strategies.equivalence_strategies.fusion import (
    FusionRuleFactory, fusion)
from tilings import Obstruction, Tiling


@pytest.fixture
def small_tiling():
    t = Tiling(obstructions=[
        Obstruction(Perm((1, 0)), ((0, 1), (1, 1))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 1))),
        Obstruction(Perm((1, 0)), ((0, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 1)))
    ])
    return t


@pytest.fixture
def big_tiling():
    """ The original tiling from Jay's idea """
    t = Tiling(obstructions=(
        Obstruction(Perm((0,)), ((0, 1),)),
        Obstruction(Perm((0,)), ((0, 2),)),
        Obstruction(Perm((0,)), ((0, 3),)),
        Obstruction(Perm((0,)), ((1, 2),)),
        Obstruction(Perm((0,)), ((1, 3),)),
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (2, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (2, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 1))),
        Obstruction(Perm((1, 0)), ((1, 1), (2, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (2, 1))),
        Obstruction(Perm((1, 0)), ((2, 0), (2, 0))),
        Obstruction(Perm((1, 0)), ((2, 1), (2, 0))),
        Obstruction(Perm((1, 0)), ((2, 1), (2, 1))),
        Obstruction(Perm((1, 0)), ((2, 2), (2, 0))),
        Obstruction(Perm((1, 0)), ((2, 2), (2, 1))),
        Obstruction(Perm((1, 0)), ((2, 2), (2, 2))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 0))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 1))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 2))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 3)))
    ), requirements=())
    return t


@pytest.fixture
def row_fusion(small_tiling):
    return FusionRuleFactory(small_tiling, row_idx=0)


@pytest.fixture
def col_fusion(small_tiling):
    return FusionRuleFactory(small_tiling, col_idx=0)


def test_formal_step(row_fusion, col_fusion):
    assert row_fusion.formal_step() == "Fuse rows 0 and 1."
    assert col_fusion.formal_step() == "Fuse columns 0 and 1."


def test_rule(row_fusion):
    rule = row_fusion.rule()
    assert rule.formal_step == row_fusion.formal_step()
    assert rule.comb_classes == [row_fusion.fused_tiling()]
    assert rule.inferable == [True]
    assert rule.workable == [True]
    assert rule.possibly_empty == [False]
    assert rule.constructor == 'other'


def test_fusion(small_tiling, big_tiling):
    assert len(list(fusion(big_tiling))) == 0
    small_tiling_rules = list(fusion(small_tiling))
    assert len(small_tiling_rules) == 2
    assert isinstance(small_tiling_rules[0], Rule)
    t = Tiling(obstructions=[
        Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
        Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
    ])
    t_rules = list(fusion(t))
    assert len(t_rules) == 1
