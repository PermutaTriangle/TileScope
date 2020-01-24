from tilings.algorithms.enumeration import (ElementaryEnumeration,
                                            LocallyFactorableEnumeration)


def globally_verified(tiling, **kwargs):
    """
    The globally verified strategy.

    A tiling is globally verified if every requirement and obstruction is
    non-interleaving.
    """
    return LocallyFactorableEnumeration(tiling).verification_rule()


def elementary_verified(tiling, **kwargs):
    """
    A tiling is elementary verified if it is globally verified and has no
    interleaving cells.
    """
    return ElementaryEnumeration(tiling).verification_rule()
