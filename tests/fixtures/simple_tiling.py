import pytest
from grids_three import Tiling, Obstruction, Requirement
from permuta import Perm


@pytest.fixture
def simple_tiling():
    return Tiling(
        obstructions=[Obstruction(Perm((1, 0)), [(0, 1), (1, 0)])],
        requirements=[[Requirement(Perm((0, 1)), [(0, 0), (1, 0)]),
                       Requirement(Perm((0, 1)), [(0, 0), (1, 1)])]])
