import pytest
import sympy

from comb_spec_searcher import ProofTree
from tilescopethree import TileScopeTHREE
from tilescopethree.strategy_packs_v2 import (row_and_col_placements,
                                              row_and_col_placements_fusion)


@pytest.mark.timeout(20)
def test_132():
    searcher = TileScopeTHREE('132', row_and_col_placements)
    t = searcher.auto_search()
    assert isinstance(t, ProofTree)
    gf = sympy.series(t.get_genf(), n=15)
    x = sympy.Symbol('x')
    assert ([gf.coeff(x, n) for n in range(13)] ==
            [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012])


@pytest.mark.timeout(20)
def test_123():
    searcher = TileScopeTHREE('123', row_and_col_placements_fusion)
    t = searcher.auto_search()
    assert isinstance(t, ProofTree)
