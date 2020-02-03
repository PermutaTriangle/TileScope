import pytest

from permuta import Perm
from tilescopethree.strategies import component_fusion
from tilings import Obstruction, Tiling


@pytest.fixture
def tiling1():
    t = Tiling(obstructions=[
        Obstruction(Perm((1, 0)), ((0, 1), (1, 1))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 1))),
        Obstruction(Perm((1, 0)), ((0, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 1)))
    ])
    return t


@pytest.fixture
def tiling2():
    t = Tiling(obstructions=[
        Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
        Obstruction(Perm((0, 2, 1)), ((0, 0), (0, 0), (0, 0))),
        Obstruction(Perm((0, 2, 1)), ((1, 0), (1, 0), (1, 0))),
        Obstruction(Perm((0, 2, 1, 3)), ((0, 0), (0, 0), (2, 0), (2, 0))),
        Obstruction(Perm((0, 2, 1, 3)), ((0, 0), (2, 0), (2, 0), (2, 0))),
        Obstruction(Perm((0, 2, 1, 3)), ((1, 0), (1, 0), (2, 0), (2, 0))),
        Obstruction(Perm((0, 2, 1, 3)), ((1, 0), (2, 0), (2, 0), (2, 0))),
        Obstruction(Perm((0, 2, 1, 3)), ((2, 0), (2, 0), (2, 0), (2, 0)))
    ])
    return t


def test_fusion_with_interleaving(tiling1, tiling2):
    assert len(list(component_fusion(tiling1))) == 0
    assert len(list(component_fusion(tiling2))) == 1
