from permuta import Perm
from tilescopethree.strategies import all_cell_insertions
from tilings import Obstruction, Requirement, Tiling

pytest_plugins = [
    'tests.fixtures.obstructions_requirements',
    'tests.fixtures.simple_tiling'
]


def test_all_cell_insertions_points(simple_tiling):
    strats = set([tuple(s.comb_classes)
                  for s in all_cell_insertions(simple_tiling, maxreqlen=1)])
    assert all(len(s) == 2 for s in strats)
    actual = set()
    actual.add((Tiling(
        obstructions=[Obstruction(Perm((0,)), [(0, 1)])],
        requirements=[[Requirement(Perm((0, 1)), [(0, 0), (1, 0)]),
                       Requirement(Perm((0, 1)), [(0, 0), (1, 1)])]]),
                Tiling(
        obstructions=[Obstruction(Perm((0,)), [(1, 0)])],
        requirements=[[Requirement(Perm((0,)), [(0, 1)])],
                      [Requirement(Perm((0, 1)), [(0, 0), (1, 1)])]])))

    actual.add((Tiling(
        obstructions=[Obstruction(Perm((0,)), ((0, 1),)),
                      Obstruction(Perm((0,)), ((1, 0),))],
        requirements=[[Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]]),
                Tiling(
        obstructions=[Obstruction(Perm((0,)), ((0, 1),))],
        requirements=[[Requirement(Perm((0,)), ((1, 0),))],
                      [Requirement(Perm((0, 1)), ((0, 0), (1, 0))),
                       Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]])))

    actual.add((Tiling(obstructions=[Obstruction(Perm(tuple()), tuple())]),
                Tiling(
        obstructions=[Obstruction(Perm((1, 0)), ((0, 1), (1, 0)))],
        requirements=[[Requirement(Perm((0,)), ((0, 0),))],
                      [Requirement(Perm((0, 1)), ((0, 0), (1, 0))),
                       Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]])))

    actual.add((Tiling(
        requirements=[[Requirement(Perm((0, 1)), ((0, 0), (1, 0)))]]),
                Tiling(
        obstructions=[Obstruction(Perm((1, 0)), ((0, 1), (1, 0)))],
        requirements=[[Requirement(Perm((0,)), ((1, 1),))],
                      [Requirement(Perm((0, 1)), ((0, 0), (1, 0))),
                       Requirement(Perm((0, 1)), ((0, 0), (1, 1)))]])))
    assert strats == actual


def test_all_cell_insertions(typical_redundant_requirements,
                             typical_redundant_obstructions):
    tiling = Tiling(obstructions=typical_redundant_obstructions,
                    requirements=typical_redundant_requirements)
    strats = set([tuple(s.comb_classes)
                  for s in all_cell_insertions(tiling, maxreqlen=3)])
    assert all(len(s) == 2 for s in strats)
    assert ((Tiling(
        obstructions=typical_redundant_obstructions + [
            Obstruction(Perm((0, 1, 2)), [(0, 1), (0, 1), (0, 1)])],
        requirements=typical_redundant_requirements),
                Tiling(
        obstructions=typical_redundant_obstructions,
        requirements=typical_redundant_requirements + [
            [Requirement(Perm((0, 1, 2)), [(0, 1), (0, 1), (0, 1)])]])
        ) in strats)
