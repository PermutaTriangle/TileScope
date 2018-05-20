"""A strategy for checking if a tiling is a subset of the class."""

from comb_spec_searcher import VerificationStrategy
from grids_three import Tiling, Obstruction
from permuta import Perm

database = {
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 2), (0, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 2), (0, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 2), (0, 2), (0, 2)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (1, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (1, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (1, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (1, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1)), ((0, 1), (0, 2))),
                      Obstruction(Perm((0, 1)), ((0, 2), (0, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 2)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((0, 0), (0, 1))),
                      Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 2), (0, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 2), (0, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 2), (0, 2), (0, 2)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (1, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((0, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((2, 0), (2, 0), (2, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 0), (2, 0))),
                      Obstruction(Perm((0, 1)), ((2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (2, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((0, 0), (1, 1))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1)), ((2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (1, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((0, 0), (1, 1))),
                      Obstruction(Perm((0, 1)), ((0, 2), (0, 2))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 0), (2, 1))),
                      Obstruction(Perm((0, 1)), ((2, 1), (2, 1))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((2, 0), (2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((2, 0), (2, 0), (2, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 2), (0, 2))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1)), ((2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (0, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (1, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 0), (2, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 2), (0, 2))),
                      Obstruction(Perm((0, 1)), ((1, 1), (1, 1))),
                      Obstruction(Perm((0, 1)), ((2, 0), (2, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 2), (2, 2), (2, 2))),
                      Obstruction(Perm((0, 1, 2)), ((1, 1), (2, 2), (2, 2))),
                      Obstruction(Perm((0, 1, 2)), ((2, 0), (2, 2), (2, 2))),
                      Obstruction(Perm((0, 1, 2)), ((2, 2), (2, 2), (2, 2)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1)), ((0, 1), (1, 2))),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 2), (0, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 2), (0, 2), (0, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 2), (0, 2), (1, 2)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((0, 0), (2, 1))),
                      Obstruction(Perm((0, 1)), ((2, 1), (2, 1))),
                      Obstruction(Perm((0, 1)), ((3, 0), (3, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (1, 0), (3, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (1, 0))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (2, 1))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 0), (3, 0)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 0), (3, 1))),
                      Obstruction(Perm((0, 1)), ((3, 1), (3, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (2, 1), (2, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (2, 1), (3, 1))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (2, 1), (2, 1))),
                      Obstruction(Perm((0, 1, 2)), ((2, 1), (2, 1), (2, 1))),
                      Obstruction(Perm((0, 1, 2)), ((2, 1), (2, 1), (3, 1)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 0), (0, 0))),
                      Obstruction(Perm((0, 1)), ((0, 0), (1, 2))),
                      Obstruction(Perm((0, 1)), ((0, 3), (0, 3))),
                      Obstruction(Perm((0, 1)), ((1, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 0), (0, 1), (0, 3))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 1))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (0, 3))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (0, 1), (1, 2)))),
        requirements=()),
    Tiling(
        obstructions=(Obstruction(Perm((0, 1)), ((0, 1), (0, 1))),
                      Obstruction(Perm((0, 1)), ((0, 1), (1, 3))),
                      Obstruction(Perm((0, 1)), ((1, 0), (1, 0))),
                      Obstruction(Perm((0, 1)), ((1, 3), (1, 3))),
                      Obstruction(Perm((0, 1, 2)), ((0, 1), (1, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((1, 0), (1, 2), (1, 3))),
                      Obstruction(Perm((0, 1, 2)), ((1, 2), (1, 2), (1, 2))),
                      Obstruction(Perm((0, 1, 2)), ((1, 2), (1, 2), (1, 3)))),
        requirements=())
    }


def database_verified(tiling, **kwargs):
    if tiling in database:
        return VerificationStrategy("Already in database!")
