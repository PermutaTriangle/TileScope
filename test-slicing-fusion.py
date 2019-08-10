from tilescopethree.tilescope import TileScopeTHREE
from tilescopethree.strategy_packs_v2 import slicing_pack, slicing_pack_rc, slicing_pack_pp

basis = '0231_0312'
pack = slicing_pack_pp(fusion_power=2, slicing_power=3)

t = TileScopeTHREE(basis, pack)
t.auto_search(smallest=True)
