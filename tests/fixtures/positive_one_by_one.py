import pytest

from permuta import Perm
from tilings import Tiling, Obstruction, Requirement

@pytest.fixture
def positive_one_by_one():
    return Tiling(
        obstructions=[Obstruction(Perm((0, 2, 1)), [(0, 0), (0, 0), (0, 0)])],
        requirements=[[Requirement(Perm((0, )), [(0, 0)])]])
