"""
,--,--'.                          ,--,--'.
`- | . |  ,-. ,-. ,-. ,-. ,-. ,-. `- |   |-. ,-. ,-. ,-.
 , | | |  |-' `-. |   | | | | |-'  , |   | | |   |-' |-'
 `-' ' `' `-' `-' `-' `-' |-' `-'  `-'   ' ' '   `-' `-'
                          |
                          '
"""
from comb_spec_searcher import CombinatorialSpecificationSearcher
from grids_three import Obstruction, Tiling
from permuta import Perm
from permuta.descriptors import Basis
from logzero import logger


class TileScopeTHREE(CombinatorialSpecificationSearcher):
    """
    An instance of TileScope is used to build up knowledge about tilings with
    respect to the given basis.
    """
    def __init__(self,
                 start_class,
                 strategy_pack,
                 # symmetry=False,
                 forward_equivalence=False,
                 logger_kwargs={'processname': 'runner'},
                 **kwargs):
        """Initialise TileScope."""
        if isinstance(start_class, str):
            basis = Basis([Perm.to_standard([int(c) for c in p])
                           for p in start_class.split('_')])
        elif isinstance(start_class, list):
            basis = Basis(start_class)
        elif isinstance(start_class, Tiling):
            start_tiling = start_class
            if start_class.dimensions == (1, 1):
                basis = Basis([o.patt for o in start_class.obstructions])
            else:
                basis = []

        if not isinstance(start_class, Tiling):
            start_tiling = Tiling(
                            obstructions=[Obstruction.single_cell(patt, (0, 0))
                                          for patt in basis])
        if strategy_pack.symmetries==True:
            symmetries = [Tiling.inverse, Tiling.reverse, Tiling.complement,
                          Tiling.antidiagonal, Tiling.rotate90,
                          Tiling.rotate180, Tiling.rotate270]
            symmetries = [sym for sym in symmetries
                          if sym(start_tiling) == start_tiling]
            strategy_pack.symmetries = symmetries
        else:
            symmetries = []

        function_kwargs = {"basis": basis}
        function_kwargs.update(kwargs.get('kwargs', dict()))

        CombinatorialSpecificationSearcher.__init__(
            self,
            start_tiling,
            strategy_pack,
            symmetry=symmetries,
            forward_equivalence=forward_equivalence,
            function_kwargs=function_kwargs,
            logger_kwargs=logger_kwargs,
            **kwargs)

    def to_dict(self):
        """Return dictionary object of self."""
        dict = super().to_dict()
        dict.pop('kwargs')
        logger.warn(("Tilescope assumes only keyword argument is basis from "
                     "all patterns in obstructions in start class so removing"
                     " kwargs."),
                    extra=self.logger_kwargs)
        return dict

    @classmethod
    def from_dict(cls, dict):
        """Return TileScopeTHREE object from dictionary."""
        scope = super(cls, TileScopeTHREE).from_dict(dict, Tiling)
        basis = Basis([ob.patt for ob in scope.start_class.obstructions])
        scope.kwargs['basis'] = basis
        return scope
