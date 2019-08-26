import pytest
from permuta import Perm
from tilings import Obstruction, Requirement, Tiling


@pytest.fixture
def positive_one_by_one():
    return Tiling(
        obstructions=[Obstruction(Perm((0, 2, 1)), [(0, 0), (0, 0), (0, 0)])],
        requirements=[[Requirement(Perm((0, )), [(0, 0)])]])
