from tilescopethree.strategies import insertion_encoding
from grids_three import Tiling, Obstruction, Requirement
from permuta import Perm

pytest_plugins = [
    'tests.fixtures.positive_one_by_one'
]


def test_insertion_encoding(positive_one_by_one):
    strats = [s.objects for s in insertion_encoding(positive_one_by_one)]
    assert len(strats) == 1
    strat = strats[0]
    for t in strat:
        print(repr(t))
        print("==")

    # middle
    assert strat[0] == Tiling(
        obstructions=(Obstruction(Perm((0,)), ((0, 0),)),
                      Obstruction(Perm((0,)), ((1, 1),)),
                      Obstruction(Perm((0,)), ((2, 0),)),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
                      Obstruction(Perm((1, 0)), ((2, 1), (2, 1))),
                      Obstruction(Perm((0, 2, 1)), ((0, 1), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 2, 1)), ((0, 1), (0, 1), (2, 1)))),
        requirements=((Requirement(Perm((0,)), ((0, 1),)),),
                      (Requirement(Perm((0,)), ((1, 0),)),),
                      (Requirement(Perm((0,)), ((2, 1),)),)))

    # left
    assert strat[1] == Tiling(
        obstructions=(Obstruction(Perm((0,)), ((0, 1),)),
                      Obstruction(Perm((0,)), ((1, 0),)),
                      Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((1, 0)), ((0, 0), (0, 0))),
                      Obstruction(Perm((1, 0)), ((1, 1), (1, 1)))),
        requirements=((Requirement(Perm((0,)), ((0, 0),)),),
                      (Requirement(Perm((0,)), ((1, 1),)),)))

    # right
    assert strat[2] == Tiling(
        obstructions=(Obstruction(Perm((0,)), ((0, 0),)),
                      Obstruction(Perm((0,)), ((1, 1),)),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((1, 0)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 2, 1)), ((0, 1), (0, 1), (0, 1)))),
        requirements=((Requirement(Perm((0,)), ((0, 1),)),),
                      (Requirement(Perm((0,)), ((1, 0),)),)))

    # fill
    assert strat[3] == Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((1, 0)), ((0, 0), (0, 0)))),
        requirements=((Requirement(Perm((0,)), ((0, 0),)),),))
