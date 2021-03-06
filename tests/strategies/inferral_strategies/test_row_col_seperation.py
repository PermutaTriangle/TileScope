import pytest

from comb_spec_searcher import InferralRule
from permuta import Perm
from tilescopethree.strategies.inferral_strategies import \
    row_and_column_separation
from tilings import Obstruction, Tiling


@pytest.fixture
def not_separable_tilings():
    t1 = Tiling(obstructions=[
        Obstruction(Perm((0, 1, 2)), ((0, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((1, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((2, 0),)*3),
        Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (2, 0)))
    ])
    t2 = Tiling(obstructions=[
        Obstruction(Perm((0, 1, 2)), ((0, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((1, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((2, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((3, 0),)*3),
        Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
        Obstruction(Perm((0, 1)), ((0, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((2, 0), (3, 0))),
    ])
    t3 = Tiling(obstructions=[
        Obstruction(Perm((0, 1, 2)), ((0, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((1, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((2, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((3, 0),)*3),
        Obstruction(Perm((0, 1)), ((0, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((0, 0), (3, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (3, 0))),
    ])
    return [t1, t2, t3]


@pytest.fixture
def seperable_tiling1():
    t1 = Tiling(obstructions=[
        Obstruction(Perm((0, 1, 2)), ((0, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((1, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((2, 0),)*3),
        Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((0, 0), (2, 0))),
    ])
    return t1


@pytest.fixture
def seperable_tiling2():
    t2 = Tiling(obstructions=[
        Obstruction(Perm((0, 1, 2)), ((0, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((1, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((2, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((3, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((0, 1),)*3),
        Obstruction(Perm((0, 1, 2)), ((1, 1),)*3),
        Obstruction(Perm((0, 1, 2)), ((2, 1),)*3),
        Obstruction(Perm((0,)), ((3, 1),)),
        Obstruction(Perm((0, 1)), ((0, 0), (0, 1))),
        Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
        Obstruction(Perm((0, 1)), ((0, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((0, 0), (3, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((2, 0), (3, 0))),
        Obstruction(Perm((0, 1)), ((0, 1), (1, 1))),
        Obstruction(Perm((0, 1)), ((0, 1), (2, 1))),
        Obstruction(Perm((0, 1)), ((0, 1), (3, 1))),
        Obstruction(Perm((0, 1)), ((1, 1), (2, 1))),
        Obstruction(Perm((0, 1)), ((2, 1), (3, 1))),
    ])
    return t2


@pytest.fixture
def seperable_tiling3():
    t3 = Tiling(obstructions=[
        Obstruction(Perm((0, 1, 2)), ((0, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((1, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((2, 0),)*3),
        Obstruction(Perm((0, 1, 2)), ((3, 0),)*3),
        Obstruction(Perm((0, 1)), ((0, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((0, 0), (3, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (2, 0))),
        Obstruction(Perm((0, 1)), ((1, 0), (3, 0))),
    ])
    return t3


def test_row_col_seperation(not_separable_tilings, seperable_tiling1,
                            seperable_tiling2, seperable_tiling3):
    t = Tiling(obstructions=[
        Obstruction(Perm((0, 1)), ((0, 0),)*2),
        Obstruction(Perm((0, 1)), ((1, 0),)*2),
        Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
    ])
    rcs = row_and_column_separation(t)
    assert rcs.comb_classes[0] == Tiling(obstructions=[
        Obstruction(Perm((0, 1)), ((0, 1),)*2),
        Obstruction(Perm((0, 1)), ((1, 0),)*2),
    ])

    for t in not_separable_tilings:
        assert row_and_column_separation(t) is None
    t1_sep = Tiling(obstructions=(
        Obstruction(Perm((0,)), ((0, 0),)),
        Obstruction(Perm((0,)), ((0, 1),)),
        Obstruction(Perm((0,)), ((1, 0),)),
        Obstruction(Perm((0,)), ((1, 2),)),
        Obstruction(Perm((0,)), ((2, 1),)),
        Obstruction(Perm((0,)), ((2, 2),)),
        Obstruction(Perm((0, 1, 2)), ((0, 2), (0, 2), (0, 2))),
        Obstruction(Perm((0, 1, 2)), ((1, 1), (1, 1), (1, 1))),
        Obstruction(Perm((0, 1, 2)), ((2, 0), (2, 0), (2, 0)))
    ), requirements=())
    t2_sep = Tiling(obstructions=(
        Obstruction(Perm((0,)), ((0, 0),)),
        Obstruction(Perm((0,)), ((0, 1),)),
        Obstruction(Perm((0,)), ((0, 2),)),
        Obstruction(Perm((0,)), ((0, 3),)),
        Obstruction(Perm((0,)), ((1, 0),)),
        Obstruction(Perm((0,)), ((1, 2),)),
        Obstruction(Perm((0,)), ((1, 3),)),
        Obstruction(Perm((0,)), ((1, 4),)),
        Obstruction(Perm((0,)), ((2, 1),)),
        Obstruction(Perm((0,)), ((2, 2),)),
        Obstruction(Perm((0,)), ((2, 4),)),
        Obstruction(Perm((0,)), ((3, 1),)),
        Obstruction(Perm((0,)), ((3, 3),)),
        Obstruction(Perm((0,)), ((3, 4),)),
        Obstruction(Perm((0,)), ((4, 1),)),
        Obstruction(Perm((0,)), ((4, 2),)),
        Obstruction(Perm((0,)), ((4, 3),)),
        Obstruction(Perm((0,)), ((4, 4),)),
        Obstruction(Perm((0, 1)), ((2, 0), (3, 0))),
        Obstruction(Perm((0, 1)), ((3, 0), (4, 0))),
        Obstruction(Perm((0, 1, 2)), ((0, 4), (0, 4), (0, 4))),
        Obstruction(Perm((0, 1, 2)), ((1, 1), (1, 1), (1, 1))),
        Obstruction(Perm((0, 1, 2)), ((2, 0), (2, 0), (2, 0))),
        Obstruction(Perm((0, 1, 2)), ((2, 3), (2, 3), (2, 3))),
        Obstruction(Perm((0, 1, 2)), ((3, 0), (3, 0), (3, 0))),
        Obstruction(Perm((0, 1, 2)), ((3, 2), (3, 2), (3, 2))),
        Obstruction(Perm((0, 1, 2)), ((4, 0), (4, 0), (4, 0)))
    ), requirements=())
    t3_sep = Tiling(obstructions=(
        Obstruction(Perm((0,)), ((0, 0),)),
        Obstruction(Perm((0,)), ((1, 0),)),
        Obstruction(Perm((0,)), ((2, 1),)),
        Obstruction(Perm((0,)), ((3, 1),)),
        Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1))),
        Obstruction(Perm((0, 1, 2)), ((1, 1), (1, 1), (1, 1))),
        Obstruction(Perm((0, 1, 2)), ((2, 0), (2, 0), (2, 0))),
        Obstruction(Perm((0, 1, 2)), ((3, 0), (3, 0), (3, 0)))
    ), requirements=())
    assert (row_and_column_separation(seperable_tiling1).comb_classes[0] ==
            t1_sep)
    assert (row_and_column_separation(seperable_tiling2).comb_classes[0] ==
            t2_sep)
    assert (row_and_column_separation(seperable_tiling3).comb_classes[0] ==
            t3_sep)
