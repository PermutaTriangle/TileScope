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

    strats = set([tuple(s.comb_classes)
                  for s in all_requirement_extensions(tiling, maxreqlen=3)])
    actual = set([
        (tiling.add_single_cell_obstruction(Perm((2, 1, 0)), (2, 0)),
         tiling.add_single_cell_requirement(Perm((2, 1, 0)), (2, 0))),
        (tiling.add_single_cell_obstruction(Perm((0, 1)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((0, 1)), (3, 0))),
        (tiling.add_single_cell_obstruction(Perm((1, 0)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((1, 0)), (3, 0))),
        (tiling.add_single_cell_obstruction(Perm((0, 1, 2)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((0, 1, 2)), (3, 0))),
        (tiling.add_single_cell_obstruction(Perm((1, 0, 2)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((1, 0, 2)), (3, 0))),
        (tiling.add_single_cell_obstruction(Perm((1, 2, 0)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((1, 2, 0)), (3, 0))),
        (tiling.add_single_cell_obstruction(Perm((2, 0, 1)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((2, 0, 1)), (3, 0))),
        (tiling.add_single_cell_obstruction(Perm((2, 1, 0)), (3, 0)),
         tiling.add_single_cell_requirement(Perm((2, 1, 0)), (3, 0)))])
    assert strats == actual
