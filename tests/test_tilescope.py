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
    x = sympy.Symbol('x')
    expected_gf = (1 - sympy.sqrt(1 - 4*x))/(2*x)
    assert t.get_genf() == expected_gf


@pytest.mark.timeout(20)
def test_123():
    searcher = TileScopeTHREE('123', row_and_col_placements_fusion)
    t = searcher.auto_search()
    assert isinstance(t, ProofTree)
