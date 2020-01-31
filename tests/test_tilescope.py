import pytest
import sympy

from comb_spec_searcher import ProofTree
from tilescopethree import TileScopeTHREE
from tilescopethree.strategy_packs_v2 import (
    all_the_strategies_verify_database, point_placements,
    point_placements_fusion, point_placements_fusion_with_interleaving,
    row_and_col_placements_fusion_with_interleaving_fusion)


@pytest.mark.timeout(20)
def test_132():
    searcher = TileScopeTHREE('132', point_placements)
    t = searcher.auto_search(smallest=True)
    assert isinstance(t, ProofTree)


@pytest.mark.xfail(reason='Generating function finding not implemented')
def test_132_genf():
    searcher = TileScopeTHREE('132', point_placements)
    t = searcher.auto_search(smallest=True)
    gf = sympy.series(t.get_genf(), n=15)
    x = sympy.Symbol('x')
    assert ([gf.coeff(x, n) for n in range(13)] ==
            [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012])


@pytest.mark.timeout(20)
def test_123():
    searcher = TileScopeTHREE('123', all_the_strategies_verify_database)
    t = searcher.auto_search(smallest=True)
    assert isinstance(t, ProofTree)


@pytest.mark.timeout(20)
def test_123_with_db():
    searcher = TileScopeTHREE('123', point_placements_fusion)
    t = searcher.auto_search(smallest=True)
    assert isinstance(t, ProofTree)


@pytest.mark.timeout(20)
def test_1342_1423():
    searcher = TileScopeTHREE('1342_1423',
                              point_placements_fusion_with_interleaving)
    t = searcher.auto_search(smallest=True)
    t.number_of_nodes() == 14
    assert isinstance(t, ProofTree)


@pytest.mark.timeout(20)
def test_1324():
    searcher = TileScopeTHREE(
        '1324',
        row_and_col_placements_fusion_with_interleaving_fusion
    )
    t = searcher.auto_search(smallest=True)
    t.number_of_nodes() == 14
    num_fusion = 0
    num_comp_fusion = 0
    for node in t.nodes():
        if 'Fuse' in node.formal_step:
            num_fusion += 1
        if 'Component' in node.formal_step:
            num_comp_fusion += 1
    assert num_fusion == 1
    assert num_comp_fusion == 1
    assert isinstance(t, ProofTree)
