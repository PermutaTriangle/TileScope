from tilescopethree.strategies import all_requirement_extensions
from tilings import Tiling, Requirement, Obstruction
from permuta import Perm

pytest_plugins = [
    'tests.fixtures.obstructions_requirements',
    'tests.fixtures.simple_tiling'
]


def test_requirement_extensions(typical_obstructions_with_local,
                                typical_requirements_with_local):
    tiling = Tiling(obstructions=typical_obstructions_with_local,
                    requirements=typical_requirements_with_local)
    print(tiling)
    strats = set([frozenset(s.comb_classes)
                  for s in all_requirement_extensions(tiling, maxreqlen=3)])

    actual = set([
        frozenset([tiling.add_single_cell_obstruction(Perm((0, 1)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((0, 1)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 0)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((1, 0)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((0, 1, 2)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((0, 1, 2)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((0, 2, 1)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((0, 2, 1)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 0, 2)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((1, 0, 2)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 2, 0)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((1, 2, 0)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 0, 1)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((2, 0, 1)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 1, 0)), (0, 0)),
         tiling.add_single_cell_requirement(Perm((2, 1, 0)), (0, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 0)), (3, 1)),
         tiling.add_single_cell_requirement(Perm((1, 0)), (3, 1))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 1, 0)), (3, 1)),
         tiling.add_single_cell_requirement(Perm((2, 1, 0)), (3, 1))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 1, 0)), (2, 0)),
         tiling.add_single_cell_requirement(Perm((2, 1, 0)), (2, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((0, 2, 1)), (2, 2)),
         tiling.add_single_cell_requirement(Perm((0, 2, 1)), (2, 2))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 0, 2)), (2, 2)),
         tiling.add_single_cell_requirement(Perm((1, 0, 2)), (2, 2))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 2, 0)), (2, 2)),
         tiling.add_single_cell_requirement(Perm((1, 2, 0)), (2, 2))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 0, 1)), (2, 2)),
         tiling.add_single_cell_requirement(Perm((2, 0, 1)), (2, 2))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 1, 0)), (2, 2)),
         tiling.add_single_cell_requirement(Perm((2, 1, 0)), (2, 2))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((0, 1)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((0, 1)), (3, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 0)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((1, 0)), (3, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((0, 1, 2)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((0, 1, 2)), (3, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 0, 2)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((1, 0, 2)), (3, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((1, 2, 0)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((1, 2, 0)), (3, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 0, 1)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((2, 0, 1)), (3, 0))]),
        frozenset([tiling.add_single_cell_obstruction(Perm((2, 1, 0)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((2, 1, 0)), (3, 0))])])
    for s in strats:
        if s not in actual:
            for t in s:
                print(t)
    assert strats == actual
