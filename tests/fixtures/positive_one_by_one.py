import pytest
from tilings import Tiling, Obstruction, Requirement
from permuta import Perm


@pytest.fixture
def positive_one_by_one():
    return Tiling(
        obstructions=[Obstruction(Perm((0, 2, 1)), [(0, 0), (0, 0), (0, 0)])],
        requirements=[[Requirement(Perm((0, )), [(0, 0)])]])
