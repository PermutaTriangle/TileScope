import pytest

from permuta import Perm
from tilings import Obstruction, Requirement, Tiling

from test_fusion import small_tiling

from tilescopethree.strategies.equivalence_strategies.fusion_with_point_req \
        import FusionWithPointReq
from tilescopethree.strategies.equivalence_strategies.fusion_with_point_req \
        import fusion_with_point_req

@pytest.fixture
def row_fusion(small_tiling):
    t = small_tiling.add_single_cell_requirement(Perm((0,)), (0,0))
    return FusionWithPointReq(t, row_idx=0)

@pytest.fixture
def row_fusion_with_two_req(small_tiling):
    t = small_tiling.add_single_cell_requirement(Perm((0,)), (0,0))
    t = t.add_single_cell_requirement(Perm((0,)), (0,1))
    t = t.add_single_cell_obstruction(Perm((0,)), (1,1))
    return FusionWithPointReq(t, row_idx=0)

def test_is_valid_count(row_fusion):
    assert row_fusion._is_valid_count(1, Requirement(Perm((0,)), ((0,0),)))
    assert not row_fusion._is_valid_count(1, Obstruction(Perm((0,)), ((0,0),)))

def test_fusable(row_fusion, row_fusion_with_two_req):
    assert row_fusion.fusable()
    assert row_fusion_with_two_req.fusable()

def test_two_point_req():
    assert (FusionWithPointReq._two_point_req((1,2)) ==
            [Requirement(Perm((0,1)), ((1,2), (1,2))),
            Requirement(Perm((1,0)), ((1,2), (1,2)))])

def test_fused_tiling(row_fusion, row_fusion_with_two_req):
    assert row_fusion.fused_tiling() == Tiling(obstructions=[
        Obstruction(Perm((1,0)), ((0,0), (0,0))),
        Obstruction(Perm((1,0)), ((0,0), (1,0))),
        Obstruction(Perm((1,0)), ((1,0), (1,0))),
    ], requirements=[
        [Requirement(Perm((0,)), ((0,0),))],
    ])
    print(row_fusion_with_two_req._tiling)
    print(row_fusion_with_two_req.fused_tiling())
    assert row_fusion_with_two_req.fused_tiling() == Tiling(obstructions=[
        Obstruction(Perm((1,0)), ((0,0), (0,0))),
    ], requirements=[
        [Requirement(Perm((0,1)), ((0,0), (0,0))),
         Requirement(Perm((1,0)), ((0,0), (0,0)))],
    ])

def test_formal_step(row_fusion):
    assert (row_fusion.formal_step() ==
            "Fuse rows 0 and 1. Ignoring point requirement.")
