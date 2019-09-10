from itertools import chain

from comb_spec_searcher import Rule
from tilings.algorithms import (Factor, FactorWithInterleaving,
                                FactorWithMonotoneInterleaving)


def general_factor(tiling, factor_class, union=False, **kwargs):
    """
    Iterator of factor strategy.
    """
    workable = kwargs.get('workable', True)
    factor = factor_class(tiling)
    if factor.factorable():
        yield factor.rule(workable=workable)
        if union:
            yield from factor.all_union_rules()


def factor(tiling, **kwargs):
    return general_factor(tiling, Factor, **kwargs)


def factor_with_monotone_interleaving(tiling, **kwargs):
    return general_factor(tiling, FactorWithMonotoneInterleaving, **kwargs)


def factor_with_interleaving(tiling, **kwargs):
    return general_factor(tiling, FactorWithInterleaving, **kwargs)


def unions_of_factor(tiling, **kwargs):
    return general_factor(tiling, Factor, union=True, **kwargs)


def unions_of_factor_with_monotone_interleaving(tiling, **kwargs):
    return general_factor(tiling, FactorWithMonotoneInterleaving, union=True,
                          **kwargs)


def unions_of_factor_with_interleaving(tiling, **kwargs):
    return general_factor(tiling, FactorWithInterleaving, union=True, **kwargs)
