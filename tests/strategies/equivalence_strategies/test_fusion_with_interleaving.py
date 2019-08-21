import pytest

from permuta import Perm
from tilings import Tiling, Obstruction

from test_fusion import small_tiling, tiling_with_req

from tilescopethree.strategies.equivalence_strategies.fusion_with_interleaving \
        import FusionWithInterleaving
from tilescopethree.strategies.equivalence_strategies.fusion_with_interleaving \
        import fusion_with_interleaving

# ------------------------------------------------
#    Fixture
# ------------------------------------------------

@pytest.fixture
def row_fusion():
    t = Tiling(obstructions=[
        Obstruction(Perm((0,1,2)), ((0,0),)*3),
        Obstruction(Perm((0,1,2)), ((0,0), (0,0), (0,1))),
        Obstruction(Perm((0,1,2)), ((0,0), (0,1), (0,1))),
        Obstruction(Perm((0,1,2)), ((0,1),)*3),
    ])
    return FusionWithInterleaving(t, row_idx=0)

# ------------------------------------------------
#    Test for fusion_with_interleaving generator
# ------------------------------------------------

def test_fusion_with_interleaving(small_tiling):
    small_tiling_rules = list(fusion_with_interleaving(small_tiling))

# ------------------------------------------------
#    Test for the class FusionWithInterleaving
# ------------------------------------------------

def test_init(small_tiling):
    FusionWithInterleaving(small_tiling, row_idx=0)
    FusionWithInterleaving(small_tiling, col_idx=1)


def test_pre_check(row_fusion, tiling_with_req):
    assert row_fusion._pre_check()
    assert not FusionWithInterleaving(tiling_with_req, 0)._pre_check()


def test_fusable(row_fusion):
    row_fusion.fusable()


def test_fused_tiling(row_fusion):
    row_fusion.fused_tiling() == Tiling(obstructions=[
        Obstruction(Perm((0,1,2)), ((0,0),)*3)
    ])
