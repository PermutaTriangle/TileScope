from tilescopethree.strategies import all_cell_insertions

from permuta import Perm
from tilings import Obstruction, Requirement, Tiling

pytest_plugins = [
    'tests.fixtures.obstructions_requirements',
    'tests.fixtures.simple_tiling'
]


def test_all_cell_insertions_points(simple_tiling):
    strats = [s.comb_classes
              for s in all_cell_insertions(simple_tiling, maxreqlen=1)]
    assert all(len(s) == 2 for s in strats)
    s = strats[0]
    assert s[0] == Tiling(
        obstructions=[Obstruction(Perm((0,)), [(0, 1)])],
        requirements=[[Requirement(Perm((0, 1)), [(0, 0), (1, 0)]),
                       Requirement(Perm((0, 1)), [(0, 0), (1, 1)])]])
    assert s[1] == Tiling(
        obstructions=[Obstruction(Perm((0,)), [(1, 0)])],
        requirements=[[Requirement(Perm((0,)), [(0, 1)])],
                      [Requirement(Perm((0, 1)), [(0, 0), (1, 1)])]])

    s = strats[1]
    assert s[0] == Tiling(
        obstructions=[Obstruction(Perm((0,)), ((0, 1),)),
                      Obstruction(Perm((0,)), ((1, 0),))],
        requirements=[[Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]])
    assert s[1] == Tiling(
        obstructions=[Obstruction(Perm((0,)), ((0, 1),))],
        requirements=[[Requirement(Perm((0,)), ((1, 0),))],
                      [Requirement(Perm((0, 1)), ((0, 0), (1, 0))),
                       Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]])

    s = strats[2]
    assert s[0] == Tiling(obstructions=[Obstruction(Perm(tuple()), tuple())])
    assert s[1] == Tiling(
        obstructions=[Obstruction(Perm((1, 0)), ((0, 1), (1, 0)))],
        requirements=[[Requirement(Perm((0,)), ((0, 0),))],
                      [Requirement(Perm((0, 1)), ((0, 0), (1, 0))),
                       Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]])

    s = strats[3]
    assert s[0] == Tiling(
        requirements=[[Requirement(Perm((0, 1)), ((0, 0), (1, 0)))]])
    assert s[1] == Tiling(
        obstructions=[Obstruction(Perm((1, 0)), ((0, 1), (1, 0)))],
        requirements=[[Requirement(Perm((0,)), ((1, 1),))],
                      [Requirement(Perm((0, 1)), ((0, 0), (1, 0))),
                       Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]])


def test_all_cell_insertions(typical_redundant_requirements,
                             typical_redundant_obstructions):
    tiling = Tiling(obstructions=typical_redundant_obstructions,
                    requirements=typical_redundant_requirements)
    strats = list(all_cell_insertions(tiling, maxreqlen=3))
    assert all(len(s.comb_classes) == 2 for s in strats)
    s = strats[-1]
    print(tiling)
    print(s.formal_step)
    print(s.comb_classes[0])
    print(s.comb_classes[1])
    assert s.comb_classes[0] == Tiling(
        obstructions=typical_redundant_obstructions + [
            Obstruction(Perm((0, 1, 2)), [(0, 1), (0, 1), (0, 1)])],
        requirements=typical_redundant_requirements)
    assert s.comb_classes[1] == Tiling(
        obstructions=typical_redundant_obstructions,
        requirements=typical_redundant_requirements + [
            [Requirement(Perm((0, 1, 2)), [(0, 1), (0, 1), (0, 1)])]])
