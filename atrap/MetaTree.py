

from atrap.strategies import all_cell_insertions
from atrap.strategies import row_and_column_separations
from atrap.strategies import all_row_and_col_placements
from atrap.strategies import components

from grids import Tiling

from permuta import PermSet
from permuta.descriptors import Basis

#
# class StrategyCache(object):
#     # TODO: Do better
#     def __init__(self, basis):
#         self.basis = basis
#
#         self.equivalence_strategy_generators = [all_row_and_col_placements,
#                                                 row_and_column_separations]
#         self.batch_strategy_generators = [all_cell_insertions]
#         self.recursive_strategy_generators = [components]
#
#         self.eq_tilings = {}
#         self.batch_tilings = {}
#         self.recursive_tilings = {}
#
#     def get_equivalence_strategies(self, tiling):
#         strats = self.eq_tilings.get(tiling)
#         if strats is None:
#             strats = []
#             for generator in self.equivalence_strategy_generators:
#                 try:
#                     strategies = generator(tiling, self.basis)
#                 except TypeError:
#                     strategies = generator(tiling)
#                 for strategy in strategies:
#                     # TODO: Need to fix it returning None.
#                     if not strategy:
#                         continue
#                     if not isinstance(strategy[0], str):
#                         strategy = ("formal step missing", strategy[0])
#                     strats.append(strategy)
#             self.eq_tilings[tiling] = strats
#         return strats
#
#     def get_batch_strategies(self, tiling):
#         strats = self.batch_tilings.get(tiling)
#         if strats is None:
#             strats = []
#             for generator in self.batch_strategy_generators:
#                 strategies = generator(tiling)
#                 for strategy in strategies:
#                     strats.append(strategy)
#             self.batch_tilings[tiling] = strats
#         return strats
#
#     # TODO: If we go back to the ancestor approach.
#     def get_recursive_strategies(self, tiling):
#

class SiblingNode(set):

    def __init__(self):
        self.expandable = False

    # Can we initialise this here rather than do it in the tree?
    # def _init__(self, tiling, and_node, equivalence_strategy_generators):

    def add(self, or_node):
        if or_node in self:
            raise RuntimeError("Attempting to add node already in sibling node")
        if not isinstance(or_node, OrNode):
            raise TypeError("Non-OR node added to sibling node")
        super(SiblingNode, self).add(or_node)
        or_node.sibling_node = self

    def get_children(self):
        # TODO: Do smarter
        children = set()
        for sibling in self:
            for child_and_node in sibling.children:
                for child_or_node in child_and_node.children:
                    children.add(child_or_node.sibling_node)
        return children

    def __hash__(self):
        return hash(id(self))#hash(sum(hash(sibling) in self))


class OrNode(object):
    def __init__(self, tiling=None):
        self.children = []
        self.parents = []
        self.expanded = False
        self.tiling = tiling
        self.sibling_node = None
        self.recursively_verifiable = [] #list of tilings
        self.verified = False

#    def get_child_sibling_nodes(self):
#        return_set = set()
#        for child_and_node in self.children:
#            for child_or_node in child_and_node.children:
#                return_set.add(child_or_node.sibling_node)
#        return return_set

    def __eq__(self, other):
        return self.tiling == other.tiling

    def __hash__(self):
        return hash(self.tiling)


class AndNode(object):
    def __init__(self, formal_step=""):
        self.formal_step = formal_step
        self.children = []
        self.parents = []
        self.recursively_verifiable = []

    #@property
    #def or_children(self):
    #    for child_or_node in root_and_node.children:
    #        for sibling_or_node in child_or_node.siblings:
    #            self._or_helper(sibling_or_node, requested_depth - 1)


class MetaTree(object):
    def __init__(self, basis):
        # Store basis
        self.basis = Basis(basis)

        # Generators for strategies
        self.equivalence_strategy_generators = [all_row_and_col_placements,
                                                row_and_column_separations]
        self.batch_strategy_generators = [all_cell_insertions]
        self.recursive_strategy_generators = [components]
        self.counting_combining = 0

        # Create the first tiling
        root_tiling = Tiling({(0, 0): PermSet.avoiding(basis)})

        # Create and store the root AND and OR node of the tree
        # Similarly create the sibling node
        root_and_node = AndNode()
        formal_step = "We start off with a 1x1 tiling where the single block is the input set."
        root_and_node.formal_step = formal_step

        root_or_node = OrNode(root_tiling)
        root_or_node.parents.append(root_and_node)
        root_and_node.children.append(root_or_node)

        root_sibling_node = SiblingNode()
        root_sibling_node.add(root_or_node)

        self.root_and_node = root_and_node
        self.root_or_node = root_or_node
        self.root_sibling_node = root_sibling_node

        # Tiling to OR node dictionary
        self.tiling_cache = {root_tiling: root_or_node}

        # How far the DFS or BFS have gone
        self.depth_searched = 0


    def do_level(self, requested_depth=None):
        if requested_depth is None:
            self.do_level(self.depth_searched + 1)
        else:
            if requested_depth <= self.depth_searched:
                print("Depth already searched")
                return
            print("Doing depth", requested_depth)
            self._sibling_helper(self.root_sibling_node, requested_depth)
            self.depth_searched = requested_depth

    def _sibling_helper(self, root_sibling_node, requested_depth):
        drill_set = set()  # Sibling nodes
        expand_set = set()  # OR nodes

        if requested_depth == 0:
            return
        elif requested_depth < 0:
            raise RuntimeError("Negative depth requested")

        for sibling_or_node in root_sibling_node:
            if sibling_or_node.expanded:
                # We need to move further down
                print("Found that I need to move down on:")
                print(sibling_or_node.tiling)
                for child_and_node in sibling_or_node.children:
                    for child_or_node in child_and_node.children:
                        drill_set.add(child_or_node.sibling_node)
            else:
                print("Found that I need to expand down on:")
                print(sibling_or_node.tiling)
                expand_set.add(sibling_or_node)

        # Expand the child nodes into sibling nodes and add to drill set
        for sibling_or_node in expand_set:
            print("Expanding:")
            print(sibling_or_node.tiling)
            child_sibling_nodes = self._expand_helper(sibling_or_node)
            drill_set.update(child_sibling_nodes)

        # Move down entire drill set
        for child_sibling_node in drill_set:
            print("Moving down:")
            print(child_sibling_node)
            self._sibling_helper(child_sibling_node, requested_depth - 1)

    def _expand_helper(self, root_or_node):
        # Expand OR node using batch strategies and return the sibling nodes
        child_sibling_nodes = set()

        # Find all the recursive strategies (including verification if switched on) and add 'em
        for generator in self.recursive_strategy_generators:
            for strategy in generator(tiling, self.basis):
                formal_step, tilings = strategy
                # Create the AND node and connect it to its parent OR node
                child_and_node = AndNode(formal_step)
                child_and_node.parents.append(root_or_node)
                root_or_node.children.append(child_and_node)
                # Go through all the tilings created for the AND node
                for tiling in tilings:
                    # Create/get a sibling node and connect it
                    sibling_node = self._get_recursive_sibling_node(tiling, child_and_node)
                    # Add it to the return set
                    child_sibling_nodes.add(sibling_node)

        # Find all the batch strategies, and add 'em.
        for generator in self.batch_strategy_generators:
            # TODO: Do we need to give it the basis for some strategies?
            for strategy in generator(root_or_node.tiling, basis=self.basis):
                if not strategy:
                    continue
                formal_step, tilings = strategy
                # Create the AND node and connect it to its parent OR node
                child_and_node = AndNode(formal_step)
                child_and_node.parents.append(root_or_node)
                root_or_node.children.append(child_and_node)
                # Go through all the tilings created for the AND node
                for tiling in tilings:
                    # Create/get a sibling node and connect it
                    sibling_node = self._get_sibling_node(tiling, child_and_node)
                    # Add it to the return set
                    child_sibling_nodes.add(sibling_node)
                    sibling_node.expandable = True
        root_or_node.expanded = True
        return child_sibling_nodes

    def _get_recursive_sibling_node(self, tiling, and_node):
        or_node = self.tiling_cache.get(tiling)
        if or_node is None:
            # Make sure we only expand non-recursive strategies
            # therefore the sibling node created will have expandable = False
            # unless found otherwise





    def _get_sibling_node(self, tiling, and_node):
        or_node = self.tiling_cache.get(tiling)

        if or_node is None:
            or_node = OrNode()
            or_node.tiling = tiling
            self.tiling_cache[tiling] = or_node

            # Our new OR node belongs to no sibling node yet

            new_or_nodes = set([or_node])
            existing_sibling_nodes = set()

            for generator in self.equivalence_strategy_generators:
                for strategy in generator(tiling, basis=self.basis):
                    if not strategy:
                        continue
                    if not isinstance(strategy[0], str):
                        strategy = "", strategy[0]
                    formal_step, eq_tiling = strategy
                    # TODO: shouldn't return these in the first place
                    if eq_tiling == tiling:
                        continue
                    # TODO: Christian stepped in, so can be done better probably.
                    # This is ancestry_dict
                    sibling_or_node = self.tiling_cache.get(eq_tiling)

                    if sibling_or_node is None:
                        sibling_or_node = OrNode(eq_tiling)

                        self.tiling_cache[eq_tiling] = sibling_or_node
                        new_or_nodes.add(sibling_or_node)
                    else:
                        existing_sibling_nodes.add(sibling_or_node.sibling_node)

            sibling_node_iter = iter(existing_sibling_nodes)
            if len(existing_sibling_nodes) == 0:
                # Create new sibling node
                sibling_node = SiblingNode()
            else:
                print("yeah!! let's combine our forces for the greater good!")
                self.counting_combining += 1
                sibling_node = next(sibling_node_iter)

            for existing_sibling_node in sibling_node_iter:
                for sibling_or_node in existing_sibling_node:
                    sibling_node.add(sibling_or_node)
            for sibling_or_node in new_or_nodes:
                sibling_node.add(sibling_or_node)
        else:
            sibling_node = or_node.sibling_node
            # Make sure we only expand batch strategies found.
            if sibling_node.expandable:



        # Hook up the OR node with its parent AND node and vice-versa
        or_node.parents.append(and_node)
        and_node.children.append(or_node)

        return sibling_node
