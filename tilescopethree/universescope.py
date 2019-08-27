import json
import time
from itertools import combinations

from tilescopethree.strategies import verify_points
from tilescopethree.strategy_packs_v2 import (row_and_col_placements,
                                              row_placements)

from comb_spec_searcher import CombinatorialSpecificationSearcher, ProofTree
from comb_spec_searcher.tree_searcher import (iterative_proof_tree_finder,
                                              iterative_prune,
                                              proof_tree_generator_bfs,
                                              proof_tree_generator_dfs, prune,
                                              random_proof_tree)
from permuta import PermSet
from tilings import Obstruction, Tiling


class UniveralScope(CombinatorialSpecificationSearcher):
    def __init__(
            self,
            n=None,
            k=None,
            strategy_pack=None,
            flogger_kwargs={
                'processname': 'runner'},
            **kwargs):
        self.start_tilings = []
        if filename is not None:
            assert n is None and k is None
            f = open(filename, 'r')
            for line in f:
                line = line.strip()
                self.start_tilings.append(Tiling.from_string(line))
            f.close()
        else:
            for basis in combinations(PermSet(n), k):
                self.start_tilings.append(
                    Tiling([Obstruction.single_cell(patt, (0, 0))
                            for patt in basis]))

        strategy_pack.ver_strats = [verify_points]

        function_kwargs = {"basis": []}
        function_kwargs.update(kwargs.get('kwargs', dict()))

        CombinatorialSpecificationSearcher.__init__(
            self,
            self.start_tilings[0],
            strategy_pack,
            function_kwargs=function_kwargs,
            **kwargs)

        self.start_labels = []
        for start_tiling in self.start_tilings:
            self.classdb.add(start_tiling, expandable=True)
            self.start_labels.append(self.classdb.get_label(start_tiling))
        for label in self.start_labels:
            self.classqueue.add_to_working(label)

    def has_proof_tree(self):
        return all(self.equivdb.is_verified(label)
                   for label in self.start_labels)

    def find_trees(self):
        """Search for a random tree based on current data found."""
        start = time.time()

        rules_dict = self.tree_search_prep()
        # Prune all unverified labels (recursively)
        if self.iterative:
            rules_dict = iterative_prune(rules_dict,
                                         root=self.equivdb[self.start_label])
        else:
            rules_dict = prune(rules_dict)

        # only verified labels in rules_dict, in particular, there is a proof
        # tree if the start label is in the rules_dict
        for label in rules_dict.keys():
            self.equivdb.update_verified(label)
        trees = []
        for label in self.start_labels:
            if label in rules_dict:
                if self.iterative:
                    proof_tree = iterative_proof_tree_finder(
                        rules_dict,
                        root=self.equivdb[label])
                else:
                    proof_tree = random_proof_tree(
                        rules_dict,
                        root=self.equivdb[label])
            else:
                proof_tree = None

            trees.append(proof_tree)

        self.tree_search_time += time.time() - start
        self._time_taken += time.time() - start
        return trees

    def auto_search(self, **kwargs):
        verbose = kwargs.get('verbose', False)
        kwargs['verbose'] = False

        if verbose:
            max_time = kwargs.get('max_time', None)
            kwargs['max_time'] = kwargs.get('status_update', None)
            status_update = kwargs.get('status_update', None)
            kwargs['status_update'] = None
            print("Starting universe scope with the tilings:")
            for t in self.start_tilings:
                print(t)
        else:
            max_time = kwargs.get('max_time', None)
            status_update = None

        trees = None
        time = 0
        while trees is None:
            trees = CombinatorialSpecificationSearcher.auto_search(
                self, **kwargs)
            time += self._time_taken
            if max_time is not None and max_time > time:
                break
            if status_update is not None:
                kwargs['max_time'] = self._time_taken + status_update
            if verbose:
                print(scope.status())

        if verbose:
            print("PROOF TREES FOUND")
            for start_tiling, tree in zip(self.start_tilings, trees):
                print(start_tiling)
                print(json.dumps(tree.to_jsonable()))

    def get_proof_tree(self):
        proof_tree_nodes = self.find_trees()
        if all(node is not None for node in proof_tree_nodes):
            proof_trees = []
            for proof_tree_node in proof_tree_nodes:
                proof_tree = ProofTree.from_comb_spec_searcher(proof_tree_node,
                                                               self)
                proof_trees.append(proof_tree)
                assert proof_tree is not None
            return proof_trees

    @classmethod
    def from_file(self, filename):
        return UniveralScope(filename=filename)


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]

    scope = UniveralScope(
        filename=filename,
        strategy_pack=row_and_col_placements)
    trees = scope.auto_search(verbose=True, status_update=30)
    trees = scope.auto_search()
    print(scope.status())
