from tilescopethree.strategies import all_cell_insertions
from grids_three import Tiling, Requirement, Obstruction
from permuta import Perm

pytest_plugins = [
    'tests.fixtures.obstructions_requirements',
    'tests.fixtures.simple_tiling'
]


def test_all_cell_insertions_points(simple_tiling):
    strats = [s.objects
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
    Tiling(obstructions=s[0].obstructions,
           requirements=s[0].requirements)
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
    assert all(len(s.objects) == 2 for s in strats)
    s = strats[-1]
    assert s.objects[0] == Tiling(
        obstructions=typical_redundant_obstructions + [
            Obstruction(Perm((1, 0, 2)), [(2, 3), (2, 3), (2, 3)])],
        requirements=typical_redundant_requirements)
    assert s.objects[1] == Tiling(
        obstructions=typical_redundant_obstructions,
        requirements=typical_redundant_requirements + [
            [Requirement(Perm((1, 0, 2)), [(2, 3), (2, 3), (2, 3)])]])
