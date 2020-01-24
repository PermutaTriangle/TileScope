from tilings.algorithms.enumeration import (LocalEnumeration,
                                            OneByOneEnumeration)


def subset_verified(tiling, no_reqs=False, **kwargs):
    """
    The subset verified strategy.

    A tiling is subset verified if every obstruction and every requirement is
    localized and the tiling is not 1x1.
    """
    return LocalEnumeration(tiling, no_reqs).verification_rule()


def one_by_one_verified(tiling, basis, **kwargs):
    """Return a verification if one-by-one verified."""
    return OneByOneEnumeration(tiling, basis).verification_rule()
