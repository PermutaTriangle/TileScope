from atrap.strategies import all_cell_insertions
from atrap.strategies import row_and_column_separations
from atrap.strategies import components
from atrap.strategies import all_point_placements
from atrap.strategies import one_by_one_verification
from atrap.strategies import empty_cell_inferral
from atrap.strategies import subclass_inferral
from atrap.strategies import subset_verified
from atrap.ProofTree import ProofTree, ProofTreeNode

from atrap.strategies import BatchStrategy
from atrap.strategies import EquivalenceStrategy
from atrap.strategies import InferralStrategy
from atrap.strategies import RecursiveStrategy
from atrap.strategies import VerificationStrategy

from grids import Tiling

from permuta import PermSet
from permuta.descriptors import Basis

from itertools import product


class SiblingNode(set):
    '''An set of OR nodes with equivalent tilings.
    It is considered natural if found by some batch strategy.
    There exists a proof tree below if its verification contains the empty frozenset.'''
    def __init__(self):
        self.natural = False
        self.verification = set()

    def add(self, or_node):
        '''An OR node has only one sibling node.
        Therefore, when adding an OR node it points to that SiblingNode.'''
        if not isinstance(or_node, OrNode):
            raise TypeError("Non-OR node added to sibling node")
        super(SiblingNode, self).add(or_node)
        or_node.sibling_node = self

    def get_parent_and_nodes(self):
        '''An iterator of all AND node parents of the SiblingNode's OR nodes.'''
        for sibling in self:
            for parent_and_node in sibling.parents:
                yield parent_and_node

    def get_children_and_nodes(self):
        child_and_nodes = set()
        for sibling_or_node in self:
            child_and_nodes.update( sibling_or_node.children )
        for child_and_node in child_and_nodes:
            yield child_and_node

    def is_verified(self):
        '''There exists a proof tree below if its verification contains the empty frozenset.'''
        return frozenset() in self.verification

    def __eq__(self, other):
        for x in self:
            if x not in other:
                return False
        for x in other:
            if x not in self:
                return False
        return True

    def __hash__(self):
        return hash(id(self))


class OrNode(object):
    '''An OR node points to a tiling. There is one OR node for a tiling.
    The children are AND nodes given by the batch strategies from its tiling.
    The parents are AND nodes in which the tiling is part of the strategy.
    It keeps track if it has been expanded by batch/equivalents strategies.
    It also points to its SiblingNode.
    For it to be verified, one of its children must be verified.'''
    def __init__(self, tiling=None):
        self.children = []
        self.parents = []
        self.expanded = False
        self.tiling = tiling
        self.sibling_node = None
        self.equivalent_expanded = False

    def is_verified(self):
        return self.sibling_node.is_verified()

    def __eq__(self, other):
        return self.tiling == other.tiling

    def __hash__(self):
        return hash(self.tiling)


class AndNode(object):
    '''An AND node encapsulates a strategy.
    Its parent node is the tiling the strategy came from.
    Its children are the tilings in the strategy.
    '''
    def __init__(self, formal_step=""):
        self.formal_step = formal_step
        self.children = []
        self.parents = []
        self.verification = set()

    def is_verified(self):
        return frozenset() in self.verification

    def parent_sibling_node(self):
        if len(self.parents) != 1:
            print(self.formal_step)
            print(self.parents)
            for parent_or_node in self.parents:
                print(parent_or_node)
                print(parent_or_node.tiling)
        assert len(self.parents) == 1

        return self.parents[0].sibling_node

    def __eq__(self, other):
        return set(self.parents) == set(other.parents) and self.formal_step == other.formal_step and set(self.children) == set(other.children)

    def __hash__(self):
        return hash(id(self))


class MetaTree(object):
    '''This searches for a proof tree for a given basis'''
    def __init__(self, basis, batch_strategies=None, equivalence_strategies=None, inferral_strategies=None, recursive_strategies=None, verification_strategies=None):
        self.basis = Basis(basis)

        '''Initialise the proof strategies to be used.'''
        if batch_strategies:
            self.batch_strategy_generators = batch_strategies
        else:
            self.batch_strategy_generators = [all_cell_insertions]
        if equivalence_strategies:
            self.equivalence_strategy_generators = equivalence_strategies
        else:
            self.equivalence_strategy_generators = [all_point_placements]
        if inferral_strategies:
            self.inferral_strategy_generators = inferral_strategies
        else:
            self.inferral_strategy_generators = [empty_cell_inferral]
        if recursive_strategies:
            self.recursive_strategy_generators = recursive_strategies
        else:
            self.recursive_strategy_generators = [components]
        if verification_strategies:
            verification_strategy_generators = verification_strategies
        else:
            self.verification_strategy_generators = [one_by_one_verification]

        '''We then initialise the tree with the one by one tiling, with input set.'''
        root_tiling = Tiling({(0,0): PermSet.avoiding(self.basis)})

        '''Create and store the root AND and OR node of the tree.'''
        root_and_node = AndNode("We start off with a 1x1 tiling where the single block is the input set.")
        root_or_node = OrNode(root_tiling)
        root_or_node.parents.append(root_and_node)
        root_and_node.children.append(root_or_node)

        '''Create the SiblingNode of the root OR node.'''
        root_sibling_node = SiblingNode()
        root_sibling_node.add(root_or_node)
        root_sibling_node.natural = True

        # '''Store them for quick access'''
        self.root_and_node = root_and_node
        self.root_or_node = root_or_node
        self.root_sibling_node = root_sibling_node

        '''Tiling to OR node dictionary'''
        self.tiling_cache = {root_tiling: root_or_node}

        '''How far the DFS or BFS have gone'''
        self.depth_searched = 0

    ''' There exists a proof tree if the frozenset() is contained in the root AND node.'''
    def has_proof_tree(self):
        return frozenset() in self.root_and_node.verification

    def do_level(self, requested_depth=None):
        '''This searches to depth first to the requested depth.
        It stops when a proof tree is found returns it, if found.'''
        if requested_depth is None:
            self.do_level(self.depth_searched + 1)
        else:
            if requested_depth <= self.depth_searched:
                print("Depth already searched")
                return
            print("Doing depth", requested_depth)
            '''The work to go deeper is hidden in the helper function.
            This returns True when a proof tree is found.'''
            if self._sibling_helper(self.root_sibling_node, requested_depth):
                print("A proof tree has been found.")
                proof_tree = self.find_proof_tree()
                # proof_tree.pretty_print()
                return self.find_proof_tree()
            self.depth_searched = requested_depth

    def _sibling_helper(self, sibling_node, requested_depth):
        '''This expands from the given SiblingNode to the requested depth.
        SiblingNodes to search on are added to the drill set.
        The OR nodes found that need expanding are added to the expand set.'''
        drill_set = set()
        expand_set = set()

        if requested_depth == 0:
            return
        elif requested_depth < 0:
            raise RuntimeError("Negative depth requested")
        '''We only expand and search on natural tilings (those found by batch strategies)
        and those which do not already have a proof tree.'''
        if not sibling_node.natural or sibling_node.is_verified():
            return

        for sibling_or_node in sibling_node:
            '''For all the sibling nodes, either'''
            if sibling_or_node.expanded:
                '''it has been expanded and we continue to search down the tree,'''
                for child_and_node in sibling_or_node.children:
                    for child_or_node in child_and_node.children:
                        drill_set.add(child_or_node.sibling_node)
            else:
                '''or the sibling needs to be expanded.'''
                expand_set.add(sibling_or_node)

        '''We then expand the nodes that need expanding.'''
        for sibling_or_node in expand_set:
            '''We first try all recursive strategies and return the set of
            child SiblingNodes created which are natural'''
            child_sibling_nodes = self._recursively_expand(sibling_or_node)
            drill_set.update(child_sibling_nodes)
            if self.has_proof_tree():
                return True
            '''We then try all batch strategies and return the set of
            child SiblingNode created'''
            child_sibling_nodes = self._batch_expand(sibling_or_node)
            drill_set.update(child_sibling_nodes)
            sibling_or_node.expanded = True
            if self.has_proof_tree():
                return True

        for child_sibling_node in drill_set:
            '''We then continue to search down the tree, lowering the requested depth.'''
            if self._sibling_helper(child_sibling_node, requested_depth - 1):
                return True

    def _recursively_expand(self, or_node):
        '''This function will expand a given OR node, and return the
        child SiblingNodes created which are natural and unverified.'''
        child_sibling_nodes = set()

        for recursive_generator in self.recursive_strategy_generators:
            '''For each recursive strategy.'''
            for recursive_strategy in recursive_generator(or_node.tiling, basis=self.basis):

                if not isinstance(recursive_strategy, RecursiveStrategy):
                    raise TypeError("Attempted to recurse on a non RecursiveStrategy.")
                # print("on the tiling:")
                # print(root_or_node.tiling)
                # print("we get the following strategy")
                formal_step = recursive_strategy.formal_step
                tilings = recursive_strategy.tilings
                # print(formal_step)
                # for tiling in tilings:
                #     print(tiling)
                # print("----------------------")

                '''We create the AND node for the strategy and connect it its parent.'''
                recursive_and_node = AndNode(formal_step)
                recursive_and_node.parents.append(or_node)
                or_node.children.append(recursive_and_node)

                '''For each tiling in the strategy,'''
                for index, tiling in enumerate(tilings):
                    '''we use the inferral strategies.'''
                    inferred_tiling = self._inferral(tiling)
                    '''We replace the tiling in the strategy with the inferred tiling.'''
                    tilings[index] = inferred_tiling

                '''Collect the verified AND nodes as they will need to propagate this information'''
                verified_and_nodes = set()

                for tiling in tilings:
                    '''We attempt to find the OR node of the tiling in the cache.'''
                    child_or_node = self.tiling_cache.get(tiling)
                    if child_or_node is None:
                        '''If it is not there we create it.'''
                        child_or_node = OrNode(tiling)
                        self.tiling_cache[tiling] = child_or_node
                        child_sibling_node = SiblingNode()
                        child_sibling_node.add(child_or_node)
                    else:
                        child_sibling_node = child_or_node.sibling_node

                    '''We connect it to the recursive AND node it belong too.'''
                    child_or_node.parents.append(recursive_and_node)
                    recursive_and_node.children.append(child_or_node)

                    '''We attempt to verify the tiling using verification strategies.'''
                    verified_and_node = self._verify(child_or_node)
                    if verified_and_node:
                        verified_and_nodes.add(verified_and_node)
                        self._equivalent_expand(child_or_node)
                        child_sibling_node = child_or_node.sibling_node
                        child_sibling_node.natural = True

                    '''If the SiblingNode is not verified we append the tiling
                    to the verification possibilities of the SiblingNode.'''
                    if not child_sibling_node.is_verified():
                        child_sibling_node.verification.add(frozenset([tiling]))

                    '''We return natural unverified SiblingNodes.'''
                    if child_sibling_node.natural and not child_sibling_node.is_verified():
                        child_sibling_nodes.add(child_sibling_node)

                for and_node in verified_and_nodes:
                    self._propagate_and_node_verification(and_node)
                self._propagate_and_node_verification(recursive_and_node)

        return child_sibling_nodes

    def _batch_expand(self, or_node):
        '''This function will expand an OR node using the batch strategies.
        It will return all unverified SiblingNodes found.'''
        child_sibling_nodes = set()

        for batch_strategy_generator in self.batch_strategy_generators:
            '''For each batch strategy.'''
            for batch_strategy in batch_strategy_generator(or_node.tiling, basis=self.basis):

                if not isinstance(batch_strategy, BatchStrategy):
                    raise TypeError("Attempted to expand with non BatchStrategy.")

                formal_step = batch_strategy.formal_step
                tilings = batch_strategy.tilings

                '''We create the AND node containing the batch strategy
                and connect it to its parent OR node.'''
                batch_and_node = AndNode(formal_step)
                batch_and_node.parents.append(or_node)
                or_node.children.append(batch_and_node)

                '''We then keep track of the AND nodes to be propagated.'''
                verified_and_nodes_to_be_propagated = set()

                '''For each tiling in the strategy,'''
                for index, tiling in enumerate(tilings):
                    '''we use the inferral strategies.'''
                    inferred_tiling = self._inferral(tiling)
                    '''We replace the tiling in the strategy with the inferred tiling.'''
                    tilings[index] = inferred_tiling

                for tiling in tilings:
                    '''We attempt to find the OR node of the tiling in the cache.'''
                    child_or_node = self.tiling_cache.get(tiling)
                    if child_or_node is None:
                        '''If it is not there we create it.'''
                        child_or_node = OrNode(tiling)
                        self.tiling_cache[tiling] = child_or_node
                        '''Attempt to expand the new OR node into a maximal SiblingNode.'''
                        self._equivalent_expand(child_or_node)
                        child_sibling_node = child_or_node.sibling_node
                        '''As it was found by a batch strategy it is natural'''
                        child_sibling_node.natural = True
                    else:
                        child_sibling_node = child_or_node.sibling_node

                    '''We connect it to the batch AND node it belongs too.'''
                    child_or_node.parents.append(batch_and_node)
                    batch_and_node.children.append(child_or_node)

                    '''We attempt to verify the tiling using verification strategies.
                    If it verifies, the function returns the verified AND node.'''
                    verified_and_node = self._verify(child_or_node)
                    if verified_and_node:
                        verified_and_nodes_to_be_propagated.add(verified_and_node)

                    '''We return natural unverified SiblingNodes.'''
                    if child_sibling_node.is_verified() and child_sibling_node.natural:
                        child_sibling_nodes.add(child_sibling_node)

                '''Propagate the AND nodes' verifications that need to be propagated'''
                for verified_and_node in verified_and_nodes_to_be_propagated:
                    self._propagate_and_node_verification(verified_and_node)
                self._propagate_and_node_verification(batch_and_node)

        return child_sibling_nodes

    def _inferral(self, tiling):
        for inferral_strategy_generator in self.inferral_strategy_generators:
            '''For each inferral strategy,'''
            for inferral_strategy in inferral_strategy_generator(tiling, basis=self.basis):
                if not isinstance(inferral_strategy, InferralStrategy):
                    raise TypeError("Attempted to infer on a non InferralStrategy")
                formal_step = inferral_strategy.formal_step
                '''we infer as much as possible about the tiling and replace it.'''
                tiling = inferral_strategy.tiling
        return tiling

    def _verify(self, or_node):
        '''Attempt to verify an OR node using verification strategies.'''
        tiling = or_node.tiling
        verified = False
        for verification_generator in self.verification_strategy_generators:
            if verified:
                '''It only needs to be verified by one verification strategy.'''
                break
            for verification_strategy in verification_generator(tiling, basis=self.basis):
                if not isinstance(verification_strategy, VerificationStrategy):
                    raise TypeError("Attempting to verify with non VerificationStrategy.")
                formal_step = verification_strategy.formal_step
                '''We create the AND node, containing the verifiction step.'''
                verified_and_node = AndNode(formal_step)
                verified_and_node.parents.append(or_node)
                or_node.children.append(verified_and_node)
                '''We add the empty frozenset which implies that a node is verified.'''
                verified_and_node.verification.add(frozenset())
                '''A verified node is considered natural.'''
                or_node.sibling_node.natural = True
                verified = True
                break
        if verified:
            return verified_and_node

    def _equivalent_expand(self, or_node):
        '''Creates the OR node's SiblingNode. It will apply the equivalence
        strategies as often as possible to make the biggest SiblingNode possible.'''
        sibling_node = SiblingNode()
        sibling_node.add(or_node)
        equivalent_tilings = set([or_node.tiling])
        tilings_to_expand = set([or_node.tiling])
        while tilings_to_expand:
            '''For each tiling to be expanded and'''
            tiling = tilings_to_expand.pop()
            for equivalence_generator in self.equivalence_strategy_generators:
                '''for all equivalent strategies'''
                for equivalence_strategy in equivalence_generator(tiling, basis=self.basis):

                    if not isinstance(equivalence_strategy, EquivalenceStrategy):
                        raise TypeError("Attempting to combine non EquivalenceStrategy.")

                    formal_step = equivalence_strategy.formal_step
                    eq_tiling = equivalence_strategy.tiling

                    '''If we have already seen this tiling while building, we skip it'''
                    if eq_tiling in equivalent_tilings:
                        continue

                    '''We look for the tiling in the cache.'''
                    eq_or_node = self.tiling_cache.get(eq_tiling)

                    '''If it is not there, we create it.'''
                    if eq_or_node is None:
                        eq_or_node = OrNode(eq_tiling)
                        sibling_node.add(eq_or_node)
                        '''Add it to the equivalent tilings found'''
                        equivalent_tilings.add(eq_tiling)
                        '''And the tilings to be checked for equivalences'''
                        tilings_to_expand.add(eq_tiling)
                    else:
                        eq_sibling_node = eq_or_node.sibling_node
                        '''The SiblingNode can be verified in anyway that the equivalent SiblingNode can be'''
                        sibling_node.verification.update(eq_sibling_node.verification)

                        if eq_sibling_node.natural:
                            '''If it is natural, we add the OR nodes to the sibling node
                            noting that we have already attempted to expand these'''
                            for eq_or_node in eq_sibling_node:
                                sibling_node.add(eq_or_node)
                                equivalent_tilings.add(eq_or_node.tiling)
                        else:
                            '''Otherwise we need to try equivalence strategies on them/it.'''
                            for eq_or_node in eq_sibling_node:
                                sibling_node.add(eq_or_node)
                                equivalent_tilings.add(eq_or_node.tiling)
                                tilings_to_expand.add(eq_tiling)

    def _propagate_and_node_verification(self, and_node, seen_nodes=None):
        if seen_nodes is None:
            seen_nodes = set()

        if and_node in seen_nodes:
            '''Already attempted the propagation of this AND node'''
            return

        '''In order to propagate we need that all our children are natural (else they have not occurred in the tree),
        and have some verification conditions.'''
        if not and_node.children:
            '''propagate this verification to its parent node'''
            if and_node is not self.root_and_node:
                self._propagate_sibling_node_verification(and_node.parent_sibling_node(), seen_nodes)
        elif all( child_or_node.sibling_node.natural and child_or_node.sibling_node.verification for child_or_node in and_node.children ):
            child_verifications = []
            for child_or_node in and_node.children:
                child_verifications.append( child_or_node.sibling_node.verification )

            '''We need to take all possible ways of taking one verification possibility
            from each child. We then union the verifications.'''
            new_verification = set()
            for verification_product in product(*child_verifications):
                new_verification.add(frozenset().union(*verification_product))

            '''and overwrite the old verification'''
            and_node.verification = new_verification

            '''we then propagate this information to its parent node'''
            if and_node is not self.root_and_node:
                self._propagate_sibling_node_verification(and_node.parent_sibling_node(), seen_nodes)

    def _propagate_sibling_node_verification(self, sibling_node, seen_nodes=None):
        '''In order to propagate we need that at least one AND node has a verified strategy'''
        if any( child_and_node.is_verified() for child_and_node in sibling_node.get_children_and_nodes() ):
            new_verifications = set()
            '''To be verified we need only one of the children AND nodes to be verified.
            We collect them all.'''
            for child_and_node in sibling_node.get_children_and_nodes():
                new_verifications.update(child_and_node.verification)
            '''We now have access to the tilings in the current SiblingNode, so we can remove
            these from our verifications'''
            final_verifications = set([ verification - sibling_node for verification in new_verifications ])

            '''we overwrite the old verification'''
            sibling_node.verification = final_verifications

            '''and propagate this information to parent AND nodes'''
            for parent_and_node in sibling_node.get_parent_and_nodes():
                self._propagate_and_node_verification(parent_and_node, seen_nodes)

    def find_proof_tree(self):
        pass
