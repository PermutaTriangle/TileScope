import pytest

from test_fusion import small_tiling

from tilescopethree.strategies.equivalence_strategies.fusion_with_interleaving \
        import FusionWithInterleaving
from tilescopethree.strategies.equivalence_strategies.fusion_with_interleaving \
        import fusion_with_interleaving

# ------------------------------------------------
#    Fixture
# ------------------------------------------------

@pytest.fixture
def row_fusion(small_tiling):
    return FusionWithInterleaving(small_tiling, row_idx=0)

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


def test_fusable(row_fusion):
    row_fusion.fusable()
