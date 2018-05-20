from grids_three import Tiling, Obstruction, Requirement
from permuta import Perm
from tilescopethree.strategies import factor

pytest_plugins = [
    'tests.fixtures.simple_tiling',
    'tests.fixtures.diverse_tiling',
]


def test_factor_no_unions(simple_tiling,
                          diverse_tiling,
                          no_point_tiling):
    assert len(list(factor(simple_tiling))) == 0
    assert len(list(factor(diverse_tiling))) == 0
    tiling = Tiling(
        obstructions=[Obstruction(Perm((0, 1)), [(0, 0), (0, 0)])],
        requirements=[[Requirement(Perm((0, 1)), [(1, 1), (1, 1)]),
                       Requirement(Perm((0, 1)), [(1, 1), (1, 2)])]])
    strats = [s.comb_classes for s in factor(tiling)]
    assert len(strats) == 1
    factors = strats[0]
    assert factors[0] == Tiling(
        requirements=[[Requirement(Perm((0, 1)), [(0, 0), (0, 0)]),
                       Requirement(Perm((0, 1)), [(0, 0), (0, 1)])]])
    assert factors[1] == Tiling(
        obstructions=[Obstruction(Perm((0, 1)), [(0, 0), (0, 0)])])

    strats = [s.comb_classes for s in factor(diverse_tiling, interleaving=True)]
    assert len(strats) == 1
    factors = strats[0]
    assert len(factors) == 4
    assert factors[0] == Tiling(requirements=[
        [Requirement(Perm((1, 0)), [(0, 1), (0, 0)]),
         Requirement(Perm((0, 2, 1)), [(0, 0), (0, 1), (1, 1)])]])

    assert factors[1] == Tiling(
        obstructions=[Obstruction(Perm((0, 2, 3, 1)),
                                  [(0, 0), (1, 1), (1, 1), (2, 0)])],
        requirements=[[Requirement(Perm((0,)), [(2, 0)])]])

    assert factors[2] == Tiling(
        obstructions=[Obstruction(Perm((0, 1)), [(0, 0), (0, 0)]),
                      Obstruction(Perm((1, 0)), [(0, 0), (0, 0)])],
        requirements=[[Requirement(Perm((0,)), [(0, 0)])]])

    assert factors[3] == Tiling(
        obstructions=[Obstruction(Perm((0, 1)), [(0, 0), (0, 0)]),
                      Obstruction(Perm((1, 0)), [(0, 0), (0, 0)])],
        requirements=[[Requirement(Perm((0,)), [(0, 0)])]])
