from tilescopethree.strategies import requirement_corroboration

from permuta import Perm
from tilings import Obstruction, Requirement, Tiling

pytest_plugins = [
    'tests.fixtures.obstructions_requirements'
]


def test_requirement_corroboration(typical_redundant_requirements,
                                   typical_redundant_obstructions):
    tiling = Tiling(
        obstructions=[Obstruction(Perm((1, 0)), [(0, 1), (1, 0)])],
        requirements=[[Requirement(Perm((0, 1)), [(0, 0), (1, 0)]),
                       Requirement(Perm((0, 1)), [(0, 0), (1, 1)])]])
    reqins = list(strat.comb_classes
                  for strat in requirement_corroboration(tiling, None))
    assert len(reqins) == 2
    strat1, strat2 = reqins

    assert len(strat1) == 2
    til1, til2 = strat1
    assert til1 == Tiling(
        obstructions=[Obstruction(Perm((0, 1)), [(0, 0), (1, 0)]),
                      Obstruction(Perm((1, 0)), [(0, 1), (1, 0)])],
        requirements=[[Requirement(Perm((0,)), [(0, 0)])],
                      [Requirement(Perm((0,)), [(1, 1)])]])
    assert til2 == Tiling(
        obstructions=[],
        requirements=[[Requirement(Perm((0, 1)), [(0, 0), (1, 0)])]])

    tiling = Tiling(
        obstructions=typical_redundant_obstructions,
        requirements=typical_redundant_requirements)
    reqins = list(strat.comb_classes
                  for strat in requirement_corroboration(tiling, None))
    assert len(reqins) == sum(len(reqs) for reqs in tiling.requirements
                              if len(reqs) > 1)
    til1, til2 = reqins[0]
    assert (set([til1, til2]) == set([
            Tiling(requirements=[
                   [Requirement(Perm((0, 1)), ((2, 0), (3, 1)))],
                   [Requirement(Perm((1, 0)), ((3, 2), (3, 1)))],
                   [Requirement(Perm((0, 1, 2)), ((0, 0), (1, 0), (2, 2)))],
                   [Requirement(Perm((0, 1, 2)), ((2, 2), (2, 2), (2, 2))),
                    Requirement(Perm((1, 0, 2)), ((0, 0), (0, 0), (0, 0)))]],
                   obstructions=typical_redundant_obstructions),
            Tiling(requirements=[
                   [Requirement(Perm((0, 1)), ((2, 0), (3, 1)))],
                   [Requirement(Perm((1, 0)), ((3, 2), (3, 1)))],
                   [Requirement(Perm((0, 1, 2)), ((0, 0), (1, 0), (2, 3))),
                    Requirement(Perm((1, 0, 2)), ((0, 0), (1, 0), (2, 2))),
                    Requirement(Perm((1, 0, 2)), ((0, 1), (1, 0), (2, 2)))],
                   [Requirement(Perm((0, 1, 2)), ((2, 2), (2, 2), (2, 2))),
                    Requirement(Perm((1, 0, 2)), ((0, 0), (0, 0), (0, 0)))]],
                   obstructions=(typical_redundant_obstructions +
                [Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (2, 2)))]))]))
