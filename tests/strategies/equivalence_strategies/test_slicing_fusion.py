import pytest

from permuta import Perm
from tilings import Tiling
from tilings.obstruction import Obstruction

from tilescopethree.strategies.equivalence_strategies.slicing_fusion import Fusion
from tilescopethree.strategies.equivalence_strategies.slicing_fusion import SlicingFusion
from tilescopethree.strategies.equivalence_strategies.slicing_fusion import SlicingFusionLevel3
from tilescopethree.strategies.equivalence_strategies.slicing_fusion import slicing_fusion

@pytest.fixture
def small_tiling():
    t = Tiling(obstructions=(
        Obstruction(Perm((0,)), ((0, 1),)),
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 1)))
    ), requirements=())
    return t

@pytest.fixture
def big_tiling():
    """ The original tiling from Jay's idea """
    t = Tiling(obstructions=(
        Obstruction(Perm((0,)), ((0, 1),)),
        Obstruction(Perm((0,)), ((0, 2),)),
        Obstruction(Perm((0,)), ((0, 3),)),
        Obstruction(Perm((0,)), ((1, 2),)),
        Obstruction(Perm((0,)), ((1, 3),)),
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (2, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (2, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 1))),
        Obstruction(Perm((1, 0)), ((1, 1), (2, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (2, 1))),
        Obstruction(Perm((1, 0)), ((2, 0), (2, 0))),
        Obstruction(Perm((1, 0)), ((2, 1), (2, 0))),
        Obstruction(Perm((1, 0)), ((2, 1), (2, 1))),
        Obstruction(Perm((1, 0)), ((2, 2), (2, 0))),
        Obstruction(Perm((1, 0)), ((2, 2), (2, 1))),
        Obstruction(Perm((1, 0)), ((2, 2), (2, 2))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 0))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 1))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 2))),
        Obstruction(Perm((2, 1, 0)), ((2, 3), (2, 3), (2, 3)))
    ), requirements=())
    return t

@pytest.fixture
def row_fusion(small_tiling):
    return SlicingFusion(small_tiling, True, 0, 0)

@pytest.fixture
def col_fusion(small_tiling):
    return SlicingFusion(small_tiling, False, 1, 0)

@pytest.fixture
def row_fusion_big(big_tiling):
    return SlicingFusion(big_tiling, True, 0, 0)

@pytest.fixture
def col_fusion_big(big_tiling):
    return SlicingFusion(big_tiling, False, 1, 0)

@pytest.fixture
def gp1():
    return Obstruction(Perm((0,1,2)), ((0,0),(1,0),(1,1)))

@pytest.fixture
def gp2():
    return Obstruction(Perm((0,1,2)), ((0,0),(1,0),(1,0)))

# ------------------------------------------------
#       Test for the class SlicingFusion
# ------------------------------------------------

def test_init(small_tiling):
    SlicingFusion(small_tiling, 1, 0, True)
    SlicingFusion(small_tiling, 0, 1, False)

def test_precheck(row_fusion, col_fusion, col_fusion_big):
    assert not hasattr(row_fusion, '_special_cell')
    assert row_fusion._pre_check()
    assert hasattr(row_fusion, '_special_cell')
    assert col_fusion._pre_check()
    assert col_fusion_big._pre_check()

def test_special_cell(row_fusion, col_fusion):
    assert row_fusion.special_cell == (0, 1)
    assert col_fusion.special_cell == (0, 1)

def test_fuse_gridded_perm(row_fusion, col_fusion, gp1):
    assert (row_fusion._fuse_gridded_perm(gp1) ==
            Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))))
    assert (col_fusion._fuse_gridded_perm(gp1) ==
            Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 1))))

def test_unfuse_gridded_perm():
    rf0 = Fusion(Tiling(), row_idx=0)
    rf1 = Fusion(Tiling(), row_idx=1)
    cf0 = Fusion(Tiling(), col_idx=0)
    ob1 = Obstruction(Perm((0,1,2,3)), ((0,0), (0,1), (0,1), (0,2)))
    assert list(rf1._unfuse_gridded_perm(ob1)) == [
        Obstruction(Perm((0,1,2,3)), ((0,0), (0,2), (0,2), (0,3))),
        Obstruction(Perm((0,1,2,3)), ((0,0), (0,1), (0,2), (0,3))),
        Obstruction(Perm((0,1,2,3)), ((0,0), (0,1), (0,1), (0,3))),
    ]
    ob2 = Obstruction(Perm((0,2,1,3)), ((0,0), (0,1), (0,1), (0,2)))
    assert list(rf1._unfuse_gridded_perm(ob2)) == [
        Obstruction(Perm((0,2,1,3)), ((0,0), (0,2), (0,2), (0,3))),
        Obstruction(Perm((0,2,1,3)), ((0,0), (0,2), (0,1), (0,3))),
        Obstruction(Perm((0,2,1,3)), ((0,0), (0,1), (0,1), (0,3))),
    ]
    ob3 = Obstruction(Perm((0,2,1,4,3)), ((0,0), (0,1), (0,1), (0,2), (0,1)))
    assert list(rf1._unfuse_gridded_perm(ob3)) == [
        Obstruction(Perm((0,2,1,4,3)), ((0,0), (0,2), (0,2), (0,3), (0,2))),
        Obstruction(Perm((0,2,1,4,3)), ((0,0), (0,2), (0,1), (0,3), (0,2))),
        Obstruction(Perm((0,2,1,4,3)), ((0,0), (0,1), (0,1), (0,3), (0,2))),
        Obstruction(Perm((0,2,1,4,3)), ((0,0), (0,1), (0,1), (0,3), (0,1))),
    ]
    ob4 = Obstruction(Perm((0,2,3,1)), ((0,0), (0,1), (1,1), (1,0)))
    assert list(rf0._unfuse_gridded_perm(ob4)) == [
        Obstruction(Perm((0,2,3,1)), ((0,1), (0,2), (1,2), (1,1))),
        Obstruction(Perm((0,2,3,1)), ((0,0), (0,2), (1,2), (1,1))),
        Obstruction(Perm((0,2,3,1)), ((0,0), (0,2), (1,2), (1,0))),
    ]
    assert list(cf0._unfuse_gridded_perm(ob4)) == [
        Obstruction(Perm((0,2,3,1)), ((1,0), (1,1), (2,1), (2,0))),
        Obstruction(Perm((0,2,3,1)), ((0,0), (1,1), (2,1), (2,0))),
        Obstruction(Perm((0,2,3,1)), ((0,0), (0,1), (2,1), (2,0))),
    ]
    #Unfuse column
    ob5 = Obstruction(Perm((2,0,1)), ((0,0), (0,0), (0,0)))
    assert list(cf0._unfuse_gridded_perm(ob5)) == [
        Obstruction(Perm((2,0,1)), ((1,0), (1,0), (1,0))),
        Obstruction(Perm((2,0,1)), ((0,0), (1,0), (1,0))),
        Obstruction(Perm((2,0,1)), ((0,0), (0,0), (1,0))),
        Obstruction(Perm((2,0,1)), ((0,0), (0,0), (0,0))),
    ]
    #Unfuse pattern with no point in the fuse region
    ob6 = Obstruction(Perm((0,1,2)), ((1,0), (1,0), (1,0)))
    assert list(cf0._unfuse_gridded_perm(ob6)) == [
        Obstruction(Perm((0,1,2)), ((2,0), (2,0), (2,0))),
    ]
    ob6 = Obstruction(Perm((1,0,2)), ((0,0), (0,0), (1,0)))
    assert list(cf0._unfuse_gridded_perm(ob6)) == [
        Obstruction(Perm((1,0,2)), ((1,0), (1,0), (2,0))),
        Obstruction(Perm((1,0,2)), ((0,0), (1,0), (2,0))),
        Obstruction(Perm((1,0,2)), ((0,0), (0,0), (2,0))),
    ]

def test_fuse_counter(row_fusion, col_fusion, gp1, gp2):
    assert (row_fusion._fuse_counter([gp1, gp2]) ==
            {Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))): 2})
    assert (col_fusion._fuse_counter([gp1, gp2]) == {
        Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 1))): 1,
        Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))): 1
    })

def test_is_localized_in_sepcial_cell(row_fusion, gp1):
    assert not row_fusion._is_localized_in_special_cell(gp1)
    obs = Obstruction(Perm((0,)), ((0,1),))
    assert row_fusion._is_localized_in_special_cell(obs)

def test_obstruction_fuse_counter(row_fusion, col_fusion, col_fusion_big):
    assert (row_fusion.obstruction_fuse_counter == {
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))): 1,
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))): 1,
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))): 3
    })
    assert (col_fusion.obstruction_fuse_counter == {
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))): 3,
        Obstruction(Perm((1, 0)), ((0, 1), (0, 0))): 1,
        Obstruction(Perm((1, 0)), ((0, 1), (0, 1))): 1
    })
    assert (col_fusion_big.obstruction_fuse_counter == {
        Obstruction(Perm((0,)), ((0, 2),)): 2,
        Obstruction(Perm((0,)), ((0, 3),)): 2,
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))): 3,
        Obstruction(Perm((1, 0)), ((0, 1), (0, 1))): 1,
        Obstruction(Perm((1, 0)), ((0, 1), (0, 0))): 1,
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))): 2,
        Obstruction(Perm((1, 0)), ((0, 1), (1, 0))): 1,
        Obstruction(Perm((1, 0)), ((0, 1), (1, 1))): 1,

        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))): 1,
        Obstruction(Perm((1, 0)), ((1, 1), (1, 0))): 1,
        Obstruction(Perm((1, 0)), ((1, 1), (1, 1))): 1,
        Obstruction(Perm((1, 0)), ((1, 2), (1, 0))): 1,
        Obstruction(Perm((1, 0)), ((1, 2), (1, 1))): 1,
        Obstruction(Perm((1, 0)), ((1, 2), (1, 2))): 1,

        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 0))): 1,
        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 1))): 1,
        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 2))): 1,
        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 3))): 1
    })

def test_can_fuse_set_of_gridded_perms(row_fusion, col_fusion):
    counter = row_fusion.obstruction_fuse_counter
    assert row_fusion._can_fuse_set_of_gridded_perms(counter)
    counter = col_fusion.obstruction_fuse_counter
    assert col_fusion._can_fuse_set_of_gridded_perms(counter)

def test_is_valid_count(row_fusion):
    assert row_fusion._is_valid_count(1, Obstruction(Perm((1, 0)), ((0, 0), (0, 0))))
    assert row_fusion._is_valid_count(1, Obstruction(Perm((1, 0)), ((0, 0), (1, 0))))
    assert row_fusion._is_valid_count(3, Obstruction(Perm((1, 0)), ((1, 0), (1, 0))))
    assert not row_fusion._is_valid_count(1, Obstruction(Perm((1, 0)), ((1, 0), (1, 0))))

def test_fusable(row_fusion, col_fusion, row_fusion_big, col_fusion_big):
    assert row_fusion.fusable()
    assert col_fusion.fusable()
    assert row_fusion_big.fusable()
    assert col_fusion_big.fusable()

def test_fusion(row_fusion, col_fusion, row_fusion_big, col_fusion_big):
    assert (row_fusion.fusion() == Tiling(obstructions=[
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0)))
    ]))
    assert (col_fusion.fusion() == Tiling(obstructions=[
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 1))),
    ]))
    assert (col_fusion_big.fusion() == Tiling(obstructions=[
        Obstruction(Perm((0,)), ((0, 2),)),
        Obstruction(Perm((0,)), ((0, 3),)),
        Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 1))),
        Obstruction(Perm((1, 0)), ((0, 1), (0, 0))),
        Obstruction(Perm((1, 0)), ((0, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((0, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((0, 1), (1, 1))),
        Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 1), (1, 1))),
        Obstruction(Perm((1, 0)), ((1, 2), (1, 0))),
        Obstruction(Perm((1, 0)), ((1, 2), (1, 1))),
        Obstruction(Perm((1, 0)), ((1, 2), (1, 2))),
        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 0))),
        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 1))),
        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 2))),
        Obstruction(Perm((2, 1, 0)), ((1, 3), (1, 3), (1, 3))),
    ]))

def test_description(row_fusion_big, col_fusion_big):
    assert (row_fusion_big.description() ==
            "Slice fuse rows 0 and 1. The special cell is (0, 1).")
    assert (col_fusion_big.description() ==
            "Slice fuse columns 0 and 1. The special cell is (0, 1).")

# ------------------------------------------------
#       Other test
# ------------------------------------------------

def test_slicing_fusion(small_tiling, big_tiling):
    assert len(list(slicing_fusion(small_tiling))) == 2
    assert len(list(slicing_fusion(big_tiling))) == 3

def slicing_fusion_level3():
    t = Tiling(
        obstructions=[Obstruction(Perm((0,1,2)), ((0,0),)*3),
                      Obstruction(Perm((0,1,2,3)), ((0,1),)*4)]
    )
    sf = SlicingFusionLevel3(t, True, 0, 0)
    assert sf.fusable
    assert sf.special_cell == (0,0)
    assert (sf.fusion ==
            Tiling(obstructions=[Obstruction(Perm((0,1,2,3)), ((0,0),)*4)]))

