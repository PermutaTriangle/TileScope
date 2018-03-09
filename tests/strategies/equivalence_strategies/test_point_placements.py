import pytest
from grids_three import Obstruction, Requirement, Tiling
from permuta import Perm
from permuta.misc import (DIR_EAST, DIR_NONE, DIR_NORTH, DIR_SOUTH, DIR_WEST,
                          DIRS)
from tilescopethree.strategies import point_placement
from tilescopethree.strategies.equivalence_strategies.point_placements import \
    place_point_of_requirement

pytest_plugins = [
    'tests.fixtures.obstructions_requirements',
    'tests.fixtures.simple_tiling',
    'tests.fixtures.diverse_tiling',
    'tests.fixtures.no_point_tiling'
]


@pytest.mark.xfail
def test_point_placement(diverse_tiling):
    strats = point_placement(diverse_tiling)
    assert len(strats) == 3 * len(DIRS)
    # strats = sorted(strats, key=lambda obj: obj.formal_step)


def test_place_point_of_requirement_point_only(diverse_tiling):
    tiling = place_point_of_requirement(diverse_tiling, 0, 0, DIR_WEST)
    assert tiling == Tiling(
        obstructions=[
            Obstruction(Perm((0,)), [(1, 0)]),
            Obstruction(Perm((0,)), [(1, 2)]),
            Obstruction(Perm((0,)), [(2, 0)]),
            Obstruction(Perm((0,)), [(2, 2)]),
            Obstruction(Perm((0, 1)), [(2, 1), (2, 1)]),
            Obstruction(Perm((0, 1)), [(4, 3), (4, 3)]),
            Obstruction(Perm((1, 0)), [(2, 1), (2, 1)]),
            Obstruction(Perm((1, 0)), [(4, 3), (4, 3)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 0), (1, 3), (1, 3), (4, 0)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 0), (1, 3), (1, 3), (4, 2)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 0), (1, 3), (3, 3), (4, 0)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 0), (1, 3), (3, 3), (4, 2)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 0), (3, 3), (3, 3), (4, 0)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 0), (3, 3), (3, 3), (4, 2)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 2), (1, 3), (1, 3), (4, 2)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 2), (1, 3), (3, 3), (4, 2)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 2), (3, 3), (3, 3), (4, 2)])],
        requirements=[
            [Requirement(Perm((0,)), [(2, 1)])],
            [Requirement(Perm((0,)), [(4, 3)])],
            [Requirement(Perm((0,)), [(4, 0)]),
             Requirement(Perm((0,)), [(4, 2)])],
            [Requirement(Perm((1, 0)), [(0, 4), (0, 3)]),
             Requirement(Perm((0, 2, 1)), [(0, 3), (0, 4), (1, 4)]),
             Requirement(Perm((0, 2, 1)), [(0, 3), (0, 4), (3, 4)])]])

    assert tiling == place_point_of_requirement(diverse_tiling, 0, 0, DIR_EAST)
    assert tiling == place_point_of_requirement(
        diverse_tiling, 0, 0, DIR_NORTH)
    assert tiling == place_point_of_requirement(
        diverse_tiling, 0, 0, DIR_SOUTH)

    tiling = place_point_of_requirement(diverse_tiling, 1, 0, DIR_WEST)
    assert tiling == Tiling(
        obstructions=[
            Obstruction(Perm((0,)), [(2, 0)]),
            Obstruction(Perm((0,)), [(2, 2)]),
            Obstruction(Perm((0, 1)), [(1, 0), (1, 0)]),
            Obstruction(Perm((0, 1)), [(1, 0), (1, 2)]),
            Obstruction(Perm((0, 1)), [(1, 2), (1, 2)]),
            Obstruction(Perm((0, 1)), [(3, 1), (3, 1)]),
            Obstruction(Perm((0, 1)), [(2, 3), (2, 3)]),
            Obstruction(Perm((0, 1)), [(2, 3), (4, 3)]),
            Obstruction(Perm((0, 1)), [(4, 3), (4, 3)]),
            Obstruction(Perm((1, 0)), [(1, 0), (1, 0)]),
            Obstruction(Perm((1, 0)), [(1, 2), (1, 0)]),
            Obstruction(Perm((1, 0)), [(1, 2), (1, 2)]),
            Obstruction(Perm((1, 0)), [(3, 1), (3, 1)]),
            Obstruction(Perm((1, 0)), [(2, 3), (2, 3)]),
            Obstruction(Perm((1, 0)), [(2, 3), (4, 3)]),
            Obstruction(Perm((1, 0)), [(4, 3), (4, 3)]),
            Obstruction(Perm((0, 1, 2)), [(0, 0), (1, 3), (1, 3)]),
            Obstruction(Perm((0, 2, 3, 1)), [(0, 2), (1, 3), (1, 3), (4, 2)])],
        requirements=[
            [Requirement(Perm((0,)), [(3, 1)])],
            [Requirement(Perm((0,)), [(1, 0)]),
             Requirement(Perm((0,)), [(1, 2)])],
            [Requirement(Perm((0,)), [(2, 3)]),
             Requirement(Perm((0,)), [(4, 3)])],
            [Requirement(Perm((1, 0)), [(0, 4), (0, 3)]),
             Requirement(Perm((0, 2, 1)), [(0, 3), (0, 4), (1, 4)])]])


def test_place_point_of_requirement(no_point_tiling):
    tiling = place_point_of_requirement(no_point_tiling, 2, 1, DIR_WEST)
    tiling2 = Tiling(
        obstructions=[
            Obstruction(Perm((0, 1)), [(0, 1), (1, 3)]),
            Obstruction(Perm((0, 1)), [(2, 2), (2, 2)]),
            Obstruction(Perm((1, 0)), [(0, 1), (0, 1)]),
            Obstruction(Perm((1, 0)), [(0, 3), (0, 1)]),
            Obstruction(Perm((1, 0)), [(0, 3), (0, 3)]),
            Obstruction(Perm((1, 0)), [(2, 2), (2, 2)]),
            Obstruction(Perm((0, 1, 2)), [(0, 0), (1, 0), (1, 0)]),
            Obstruction(Perm((0, 1, 2)), [(0, 0), (1, 0), (3, 0)]),
            Obstruction(Perm((0, 1, 2)), [(0, 0), (3, 0), (3, 0)]),
            Obstruction(Perm((0, 1, 2)), [(1, 0), (1, 0), (4, 0)]),
            Obstruction(Perm((0, 1, 2)), [(1, 0), (3, 0), (4, 0)]),
            Obstruction(Perm((0, 1, 2)), [(3, 0), (3, 0), (4, 0)]),
            Obstruction(Perm((0, 2, 1)), [(0, 1), (1, 1), (1, 1)]),
            Obstruction(Perm((0, 2, 1)), [(0, 1), (1, 1), (3, 1)]),
            Obstruction(Perm((0, 2, 1)), [(0, 3), (1, 3), (1, 3)]),
            Obstruction(Perm((0, 2, 1)), [(0, 3), (1, 3), (3, 3)]),
            Obstruction(Perm((0, 2, 1)), [(0, 4), (0, 4), (1, 4)]),
            Obstruction(Perm((0, 2, 1)), [(0, 4), (0, 4), (3, 4)]),
            Obstruction(Perm((0, 2, 1)), [(0, 4), (1, 4), (1, 4)]),
            Obstruction(Perm((0, 2, 1)), [(0, 4), (1, 4), (3, 4)]),
            Obstruction(Perm((0, 2, 1)), [(0, 4), (3, 4), (3, 4)])],
        requirements=[
            [Requirement(Perm((0,)), [(2, 2)])],
            [Requirement(Perm((0, 1)), [(0, 0), (0, 0)]),
             Requirement(Perm((0, 1)), [(0, 0), (4, 0)])],
            [Requirement(Perm((0, 1)), [(0, 1), (3, 1)])],
            [Requirement(Perm((0, 1)), [(1, 1), (4, 1)]),
             Requirement(Perm((0,)), [(4, 3)]),
             Requirement(Perm((0,)), [(4, 4)]),
             Requirement(Perm((0, 1)), [(3, 1), (4, 1)])]]
    )
    assert tiling == tiling2
