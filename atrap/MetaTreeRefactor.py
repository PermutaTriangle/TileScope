from atrap.strategies import all_cell_insertions
from atrap.strategies import components
from atrap.strategies import all_point_placements
from atrap.strategies import one_by_one_verification
from atrap.strategies import empty_cell_inferral
from atrap.strategies import subclass_inferral
from atrap.strategies import subset_verified
from atrap.ProofTree import ProofTree, ProofTreeNode

from atrap.strategies import BatchStrategy
from atrap.strategies import EquivalenceStrategy, all_symmetric_tilings
from atrap.strategies import InferralStrategy
from atrap.strategies import RecursiveStrategy
from atrap.strategies import VerificationStrategy
from .LRUCache import LRUCache

import time

from grids import Tiling

from permuta.descriptors import Basis
from permuta import PermSet

from itertools import product

import sys
import traceback


class SiblingNode(set):
    '''A set of OR nodes with equivalent tilings.
    The node is considered natural if it contains a tiling found by a batch
    strategy. There exists a proof tree below the node if its verification
    contains the empty frozenset.'''
    def __init__(self):
        self.natural = False
        self.verification = set()
        self.explanations = {}

    def add(self, or_node):
        '''An OR node has only one sibling node.
        Therefore, when adding an OR node it points to that SiblingNode.'''
        if not isinstance(or_node, OrNode):
            raise TypeError("Non-OR node added to sibling node")
        super(SiblingNode, self).add(or_node)
        or_node.sibling_node = self

    def join(self, tiling, other_tiling, explanation):
        key = (tiling, other_tiling)
        if key not in self.explanations:
            self.explanations[key] = explanation

    def get_parent_and_nodes(self):
        '''An iterator of all AND node parents of the SiblingNode's OR nodes.'''
        for sibling in self:
            for parent_and_node in sibling.parents:
                yield parent_and_node

    def get_children_and_nodes(self):
        '''An iterator of all AND nodes that are children of a tiling in
        self.'''
        child_and_nodes = set()
        for sibling_or_node in self:
            child_and_nodes.update( sibling_or_node.children )
        for child_and_node in child_and_nodes:
            yield child_and_node

    def is_verified(self):
        '''There exists a proof tree below if its verification contains the
        empty frozenset.'''
        return frozenset() in self.verification

    def get_relation(self, tiling, other_tiling):
        if tiling == other_tiling:
            return ""

        path = self.find_path(tiling, other_tiling)
        if path:
            explanation = "| "
            for i in range(len(path) - 1):
                for j in range(i+1, len(path)):
                    t1 = path[i]
                    t2 = path[j]
                    key = (t1, t2)
                    if key in self.explanations:
                        explanation = explanation + self.explanations[key] + ". | "
                    key = (t2, t1)
                    if key in self.explanations:
                        explanation = explanation + "The reverse of: " + self.explanations[key] + ". | "
            return explanation
        '''We hopefully never get here'''
        return "they are on the same SiblingNode"

    def find_path(self, tiling, other_tiling):
        '''Floyd-Warshall algorithm for shortest path'''
        sibling_tilings = {}
        reverse_map = {}
        for or_node in self:
            n = len(sibling_tilings)
            sibling_tilings[or_node.tiling] = n
            reverse_map[n] = or_node.tiling

        dist = [ [99999999 for i in range(len(sibling_tilings))] for j in range(len(sibling_tilings))]
        nxt = [ [None for i in range(len(sibling_tilings))] for j in range(len(sibling_tilings))]
        for key in self.explanations.keys():
            u = sibling_tilings[key[0]]
            v = sibling_tilings[key[1]]
            dist[u][v] = 1
            nxt[u][v] = v
            dist[v][u] = 1
            nxt[v][u] = u

        for k in range(len(sibling_tilings)):
            for i in range(len(sibling_tilings)):
                for j in range(len(sibling_tilings)):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]

        u = sibling_tilings[tiling]
        v = sibling_tilings[other_tiling]
        if nxt[u][v] is None:
            return []
        path = [u]
        while u != v:
            u = nxt[u][v]
            path.append(u)
        return [reverse_map[x] for x in path]

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
    It keeps track if it has been expanded by batch/equivalence strategies.
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
        self.recursion = False
        self.back_maps = []

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
        '''A cache for the tilings generated by inferral functions'''
        self._inferral_cache = LRUCache(100000)
        self.inferral_cache_hits = 0
        '''A caching of the output of the basis partitioning of a tiling'''
        self._basis_partitioning_cache = LRUCache(100000)
        self.partitioning_cache_hits = 0
        '''A cache for labels'''
        self._tiling_to_label = {}
        self._labels_to_or_node = {}
        self._partitioning_calls = {}
        self._cached_tilings = set()
        self._cache_misses = 0
        self.timed_out = False

        '''Initialise the proof strategies to be used.'''
        if batch_strategies is not None:
            self.batch_strategy_generators = batch_strategies
        else:
            self.batch_strategy_generators = [all_cell_insertions]
        if equivalence_strategies is not None:
            self.equivalence_strategy_generators = equivalence_strategies
        else:
            self.equivalence_strategy_generators = [all_point_placements]
        if inferral_strategies is not None:
            self.inferral_strategy_generators = inferral_strategies
        else:
            self.inferral_strategy_generators = [empty_cell_inferral]
        if recursive_strategies is not None:
            self.recursive_strategy_generators = recursive_strategies
        else:
            self.recursive_strategy_generators = [components]
        if verification_strategies is not None:
            self.verification_strategy_generators = verification_strategies
        else:
            self.verification_strategy_generators = [one_by_one_verification]

        '''Initialise the tree with the one by one tiling, with Av(basis.'''
        root_tiling = Tiling({(0,0): PermSet.avoiding(self.basis)})

        '''Create and store the root AND and OR node of the tree.'''
        root_and_node = AndNode("We start off with a 1x1 tiling where the single block is Av({}).".format(self.basis))
        root_or_node = OrNode(root_tiling)
        root_or_node.parents.append(root_and_node)
        root_and_node.children.append(root_or_node)

        '''Create the SiblingNode of the root OR node.'''
        root_sibling_node = SiblingNode()
        root_sibling_node.add(root_or_node)
        root_sibling_node.natural = True

        '''Store them for quick access'''
        self.root_and_node = root_and_node
        self.root_or_node = root_or_node
        self.root_sibling_node = root_sibling_node

        '''Tiling to OR node dictionary'''
        '''Remember to update the cache'''
        self.tiling_cache = {root_tiling: root_or_node}

        '''How far the DFS or BFS have gone'''
        self.depth_searched = 0

    ''' There exists a proof tree if the frozenset() is contained in the root AND node.'''
    def has_proof_tree(self):
        return frozenset() in self.root_and_node.verification

    def do_level(self, requested_depth=None, file=sys.stdout, max_time=None):
        '''This searches to depth first to the requested depth.
        It stops when a proof tree is found, and returns it, if found.'''
        start_time = time.time()
        if requested_depth is None:
            self.do_level(self.depth_searched + 1, file=file, max_time=max_time)
        else:
            if requested_depth <= self.depth_searched:
                print("Depth already searched", file=file)
                return
            print("Doing depth", requested_depth, file=file)
            '''The work to go deeper is hidden in the helper function.
            This returns True when a proof tree is found.'''
            if self._sibling_helper(self.root_sibling_node, requested_depth, max_time=max_time):
                print("A proof tree has been found.", file=file)
                proof_tree = self.find_proof_tree()
                # proof_tree.pretty_print()
                return proof_tree
            if max_time is not None:
                if time.time() - start_time > max_time:
                    self.timed_out = True
            self.depth_searched = requested_depth

    def _sibling_helper(self, sibling_node, requested_depth, max_time=None, start_time=None):
        '''This expands from the given SiblingNode to the requested depth.
        SiblingNodes to search on are added to the drill set.
        The OR nodes found that need expanding are added to the expand set.'''
        drill_set = set()
        expand_set = set()

        if max_time is not None:
            if start_time is None:
                start_time = time.time()

        if requested_depth == 0:
            return
        elif requested_depth < 0:
            raise RuntimeError("Negative depth requested")
        '''We only expand and search on natural tilings (those found by batch strategies)
        and those which do not already have a proof tree.'''
        if (not sibling_node.natural) or sibling_node.is_verified():
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

            if max_time is not None:
                if time.time() - start_time > max_time:
                    return False

        for sibling_or_node in expand_set:
            '''We then try all batch strategies and return the set of
            child SiblingNode created'''
            child_sibling_nodes = self._batch_expand(sibling_or_node)
            drill_set.update(child_sibling_nodes)
            sibling_or_node.expanded = True
            '''cleanup the cache'''
            if sibling_or_node.tiling in self._basis_partitioning_cache:
                self._basis_partitioning_cache.pop(sibling_or_node.tiling)
            if self.has_proof_tree():
                return True

            if max_time is not None:
                if time.time() - start_time > max_time:
                    return False

        for child_sibling_node in drill_set:
            '''We then continue to search down the tree, lowering the requested depth.'''
            if max_time is not None:
                if self._sibling_helper(child_sibling_node, requested_depth - 1, max_time=max_time, start_time=start_time):
                    return True
                if time.time() - start_time > max_time:
                    return False
            else:
                self._sibling_helper(child_sibling_node, requested_depth - 1)

    def _recursively_expand(self, or_node):
        '''This function will expand a given OR node, and return the
        child SiblingNodes created which are natural and unverified.'''
        child_sibling_nodes = set()

        for recursive_generator in self.recursive_strategy_generators:
            '''For each recursive strategy.'''
            for recursive_strategy in recursive_generator(or_node.tiling, basis=self.basis, basis_partitioning=self._basis_partitioning, verification_strategies=self.verification_strategy_generators, tiling_cache=self.tiling_cache):

                if not isinstance(recursive_strategy, RecursiveStrategy):
                    raise TypeError("Attempted to recurse on a non RecursiveStrategy.")

                formal_step = recursive_strategy.formal_step
                tilings = recursive_strategy.tilings

                '''We create the AND node for the strategy and connect it its parent.'''
                recursive_and_node = AndNode(formal_step)
                recursive_and_node.parents.append(or_node)
                recursive_and_node.recursion = True
                recursive_and_node.back_maps = recursive_strategy.back_maps
                or_node.children.append(recursive_and_node)

                '''Collect the verified AND nodes as they will need to propagate this information'''
                sibling_nodes_to_be_propagated = set()

                for tiling in tilings:
                    '''We attempt to find the OR node of the tiling in the cache.'''
                    child_or_node = self.tiling_cache.get(tiling)

                    if child_or_node is None:
                        '''If it is not there we create it.'''
                        child_or_node = OrNode(tiling)
                        '''Remember to update the cache'''
                        self.tiling_cache[tiling] = child_or_node
                        child_sibling_node = SiblingNode()
                        child_sibling_node.add(child_or_node)

                        '''We attempt to verify the tiling using verification strategies.'''
                        if self._verify(child_or_node):
                            '''If it is verified we need to propagate the information to the sibling node'''
                            sibling_nodes_to_be_propagated.add(child_sibling_node)
                            child_sibling_node.natural = True
                    else:
                        child_sibling_node = child_or_node.sibling_node

                    '''We connect it to the recursive AND node it belong too.'''
                    child_or_node.parents.append(recursive_and_node)
                    recursive_and_node.children.append(child_or_node)

                    '''If the SiblingNode is not verified we append the tiling
                    to the verification possibilities of the SiblingNode.'''
                    if not child_sibling_node.is_verified():
                        child_sibling_node.verification.add( frozenset([ self._tiling_labeler(tiling) ]) )

                    '''We return natural unverified SiblingNodes.'''
                    child_sibling_nodes.add(child_sibling_node)

                    temp_or_node = self.tiling_cache.get(tiling)
                    temp_sibling_node = temp_or_node.sibling_node

                    '''We only want to cache natural things'''
                    if not child_or_node.sibling_node.natural:
                        if tiling in self._basis_partitioning_cache:
                            self._basis_partitioning_cache.pop(tiling)




                for sibling_node in sibling_nodes_to_be_propagated:
                    if sibling_node.is_verified():
                        '''clean the cache'''
                        self._sibling_node_cache_cleaner(sibling_node)
                    '''propagate the information'''
                    self._propagate_sibling_node_verification(sibling_node)
                self._propagate_and_node_verification(recursive_and_node)

        return child_sibling_nodes

    def _batch_expand(self, or_node):
        '''This function will expand an OR node using the batch strategies.
        It will return all unverified SiblingNodes found.'''
        child_sibling_nodes = set()

        for batch_strategy_generator in self.batch_strategy_generators:
            '''For each batch strategy.'''
            for batch_strategy in batch_strategy_generator(or_node.tiling, basis=self.basis, basis_partitioning=self._basis_partitioning):

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
                verified_sibling_nodes = set()

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
                        '''Remember to update the cache'''
                        self.tiling_cache[tiling] = child_or_node
                        '''Attempt to expand the new OR node into a maximal SiblingNode.'''
                        verified = self._equivalent_expand(child_or_node)
                        child_sibling_node = child_or_node.sibling_node
                        if verified:
                            verified_sibling_nodes.add( child_sibling_node )
                        elif self._verify(child_or_node):
                            '''We attempt to verify the tiling using verification strategies.
                            If it verifies, we need to propagate the information to the sibling node.'''
                            verified_sibling_nodes.add( child_sibling_node )
                        '''As it was found by a batch strategy it is natural'''
                        child_sibling_node.natural = True
                    else:
                        child_sibling_node = child_or_node.sibling_node
                        if not child_sibling_node.natural:
                            verified = self._equivalent_expand(child_or_node)
                            child_sibling_node = child_or_node.sibling_node
                            if verified:
                                verified_sibling_nodes.add( child_sibling_node )
                            '''As it was found by a batch strategy it is natural'''
                            child_sibling_node.natural = True

                            '''Should we be propagating tilings which become natural?'''
                            verified_sibling_nodes.add(child_sibling_node)
                            # print("propagating tiling which became natural")
                            # print(tiling)

                    '''We connect it to the batch AND node it belongs too.'''
                    child_or_node.parents.append(batch_and_node)
                    batch_and_node.children.append(child_or_node)

                    '''We try expanding further'''
                    child_sibling_nodes.add(child_sibling_node)

                '''Propagate the verifications that need to be propagated'''
                for sibling_node in verified_sibling_nodes:
                    '''clean the cache'''
                    self._sibling_node_cache_cleaner(sibling_node)
                    '''then propagate'''
                    self._propagate_sibling_node_verification(sibling_node)
                self._propagate_and_node_verification( batch_and_node )
        return child_sibling_nodes

    def _inferral(self, tiling):
        inferred_tiling = self._inferral_cache.get(tiling)
        semi_inferred_tilings = []
        if inferred_tiling is None:
            inferred_tiling = tiling
            fully_inferred = False
            for inferral_strategy_generator in self.inferral_strategy_generators:
                '''For each inferral strategy,'''
                if fully_inferred:
                    break
                for inferral_strategy in inferral_strategy_generator(inferred_tiling, basis=self.basis, basis_partitioning=self._basis_partitioning):
                    if not isinstance(inferral_strategy, InferralStrategy):
                        raise TypeError("Attempted to infer on a non InferralStrategy")
                    formal_step = inferral_strategy.formal_step
                    '''we infer as much as possible about the tiling and replace it.'''
                    soon_to_be_tiling = inferral_strategy.tiling

                    if soon_to_be_tiling is inferred_tiling:
                        continue

                    if soon_to_be_tiling in self._inferral_cache:
                        soon_to_be_tiling = self._inferral_cache.get(soon_to_be_tiling)
                        semi_inferred_tilings.append(inferred_tiling)
                        inferred_tiling = soon_to_be_tiling
                        fully_inferred = True
                        break
                    else:
                        semi_inferred_tilings.append(inferred_tiling)
                        inferred_tiling = soon_to_be_tiling
            for semi_inferred_tiling in semi_inferred_tilings:
                self._inferral_cache.set(semi_inferred_tiling, inferred_tiling)
                '''Clean up the cache'''
                if semi_inferred_tiling in self._basis_partitioning_cache:
                    self._basis_partitioning_cache.pop(semi_inferred_tiling)
            self._inferral_cache.set(inferred_tiling, inferred_tiling)
        else:
            self.inferral_cache_hits += 1
        return inferred_tiling

    def _basis_partitioning(self, tiling, length, basis, function_name=None):
        """A cached basis partitioning function."""

        if function_name is not None:
            if function_name in self._partitioning_calls:
                self._partitioning_calls[function_name][0] += 1
            else:
                self._partitioning_calls[function_name] = [1,0]


        cache = self._basis_partitioning_cache.get(tiling)
        if cache is None:
            if tiling in self._cached_tilings:
                self._cache_misses += 1
            else:
                self._cached_tilings.add(tiling)
            self._basis_partitioning_cache.set(tiling, {})
            cache = self._basis_partitioning_cache.get(tiling)
        else:
            self.partitioning_cache_hits += 1
        if length not in cache:
            if function_name is not None:
                self._partitioning_calls[function_name][1] += 1
            else:
                print("SOMEONE IS CALLING NONE!")
                for line in traceback.format_stack():
                    print(line.strip())
            cache[length] = tiling.basis_partitioning(length, basis)
        return cache[length]

    def _verify(self, or_node):
        '''Attempt to verify an OR node using verification strategies.
        It will connect an AND node carrying the formal step.'''
        tiling = or_node.tiling
        verified = False
        for verification_generator in self.verification_strategy_generators:
            for verification_strategy in verification_generator(tiling, basis=self.basis, basis_partitioning=self._basis_partitioning):
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
                '''clean the cache'''
                if or_node.tiling in self._basis_partitioning_cache:
                    self._basis_partitioning_cache.pop(or_node.tiling)
                return True
        return False

    def _equivalent_expand(self, or_node):
        '''Creates the OR node's SiblingNode. It will apply the equivalence
        strategies as often as possible to make the biggest SiblingNode possible.
        It will return true if any equivalent tiling is verified, false otherwise.'''
        sibling_node = SiblingNode()
        sibling_node.add(or_node)
        '''We only equivalent expand on natural OR nodes'''
        sibling_node.natural = True
        equivalent_tilings = set([or_node.tiling])
        tilings_to_expand = set([or_node.tiling])
        verified = False
        while tilings_to_expand:
            '''For each tiling to be expanded and'''
            tiling = tilings_to_expand.pop()
            for equivalence_generator in self.equivalence_strategy_generators:
                '''for all equivalent strategies'''
                for equivalence_strategy in equivalence_generator(tiling, basis=self.basis, basis_partitioning=self._basis_partitioning):

                    if not isinstance(equivalence_strategy, EquivalenceStrategy):
                        raise TypeError("Attempting to combine non EquivalenceStrategy.")

                    formal_step = equivalence_strategy.formal_step
                    eq_tiling = equivalence_strategy.tiling

                    '''We infer on the equivalent tiling'''
                    if equivalence_generator != all_symmetric_tilings:
                        eq_tiling = self._inferral(eq_tiling)

                    '''If we have already seen this tiling while building, we skip it'''
                    if eq_tiling in equivalent_tilings:
                        continue

                    '''We look for the tiling in the cache.'''
                    eq_or_node = self.tiling_cache.get(eq_tiling)

                    '''If it is not there, we create it.'''
                    if eq_or_node is None:
                        eq_or_node = OrNode(eq_tiling)
                        '''Remember to update the cache'''
                        self.tiling_cache[eq_tiling] = eq_or_node
                        sibling_node.add(eq_or_node)
                        sibling_node.join(tiling, eq_tiling, formal_step)
                        '''Add it to the equivalent tilings found'''
                        equivalent_tilings.add(eq_tiling)
                        '''And the tilings to be checked for equivalences'''
                        tilings_to_expand.add(eq_tiling)
                        '''We try to verify the equivalent tiling'''
                        if self._verify(eq_or_node):
                            verified = True
                    else:
                        eq_sibling_node = eq_or_node.sibling_node
                        '''The SiblingNode can be verified in anyway that the equivalent SiblingNode can be'''
                        sibling_node.verification.update(eq_sibling_node.verification)
                        sibling_node.explanations.update(eq_sibling_node.explanations)
                        sibling_node.join(tiling, eq_tiling, formal_step)

                        if eq_sibling_node.natural:
                            '''If it is natural, we add the OR nodes to the sibling node
                            noting that we have already attempted to expand these'''
                            for sibling_or_node in eq_sibling_node:
                                sibling_node.add(sibling_or_node)
                                equivalent_tilings.add(sibling_or_node.tiling)
                        else:
                            '''Otherwise we need to try equivalence strategies on them/it.'''
                            for sibling_or_node in eq_sibling_node:
                                sibling_node.add(sibling_or_node)
                                equivalent_tilings.add(sibling_or_node.tiling)
                                tilings_to_expand.add(sibling_or_node.tiling)
        return verified

    def _sibling_node_cache_cleaner(self, sibling_node):
        for or_node in sibling_node:
            tiling = or_node.tiling
            if tiling in self._basis_partitioning_cache:
                self._basis_partitioning_cache.pop(tiling)


    def _tiling_labeler( self, tiling ):
        '''Labels a tiling. It tries to label tilings in the same sibling node.'''
        or_node = self.tiling_cache.get(tiling)
        assert or_node is not None
        sibling_node = or_node.sibling_node
        for node in sibling_node:
            label = self._tiling_to_label.get(node.tiling)
            if label is not None:
                return label
        label = len(self._tiling_to_label)
        self._tiling_to_label[tiling] = label
        self._labels_to_or_node[label] = or_node
        return label

    def _get_sibling_labels(self, sibling_node, force=False):
        '''Return all the labels of the tilings in the sibling node'''
        labels = set()
        for or_node in sibling_node:
            label = self._tiling_to_label.get(or_node.tiling)
            if label is not None:
                labels.add(label)
        if not labels and force:
            labels.add( self._tiling_labeler( or_node.tiling ) )
        return labels


    def _propagate_and_node_verification(self, and_node):

        if and_node.is_verified():
            '''The AND node is already verified, so propagated this information already'''
            return

        '''In order to propagate we need that all our children are natural (else they have not occurred in the tree),
        and have some verification conditions.'''
        if all( child_or_node.sibling_node.natural and child_or_node.sibling_node.verification for child_or_node in and_node.children ):

            if all( child_or_node.sibling_node.is_verified() for child_or_node in and_node.children ):
                new_verifications = set([frozenset()])
            else:
                child_verifications = []
                for child_or_node in and_node.children:
                    child_verifications.append( child_or_node.sibling_node.verification )

                '''We need to take all possible ways of taking one verification possibility
                from each child. We then union the verifications.'''
                new_verifications = self._multiple_cleaner_products(child_verifications)

            if and_node.verification == new_verifications:
                '''The status of the AND node's verification didn't change, we therefore
                already propagated this information before'''
                return

            and_node.verification = new_verifications

            if and_node.is_verified():
                if and_node is not self.root_and_node:
                    # self._propagate_sibling_node_verification(and_node.parent_sibling_node(), set([and_node]))
                    self._propagate_sibling_node_verification(and_node.parent_sibling_node())
                return

            '''we then propagate this information to its parent node'''
            if and_node is not self.root_and_node:
                # self._propagate_sibling_node_verification(and_node.parent_sibling_node(), seen_nodes)
                self._propagate_sibling_node_verification(and_node.parent_sibling_node())

    def _propagate_sibling_node_verification(self, sibling_node):#, seen_nodes=None):

        # if seen_nodes is None:
        #     seen_nodes = set()
        # if sibling_node in seen_nodes:
        #     return
        # else:
        #     seen_nodes.add(sibling_node)

        if sibling_node.is_verified():
            '''The node is already verified, we've already pushed this information around'''
            return

        '''In order to propagate we need that at least one AND node has a verified strategy'''
        if any( child_and_node.verification for child_and_node in sibling_node.get_children_and_nodes() ):

            if any(child_and_node.is_verified() for child_and_node in sibling_node.get_children_and_nodes() ):
                cleaned_verifications = set([frozenset()])
            else:
                cleaned_verifications = set()
                sibling_node_labels = self._get_sibling_labels(sibling_node)
                child_and_node_verifications = sorted( [ child_and_node.verification for child_and_node in sibling_node.get_children_and_nodes()], key = len  )

                for child_verification in child_and_node_verifications:
                    self._cleaner_update( cleaned_verifications, child_verification, sibling_node_labels )
                    if frozenset() in cleaned_verifications:
                        '''Then the node is verified.'''
                        cleaned_verifications = set( [frozenset()] )
                        break
                    else:
                        # assert ( frozenset(sibling_node_labels) not in cleaned_verifications and frozenset(sibling_node_labels) in sibling_node.verification) == ( not any( verification.issubset(sibling_node_labels) for verification in cleaned_verifications ) and any( verification.issubset(sibling_node_labels) for verification in sibling_node.verification ) )
                        if not any( verification.issubset(sibling_node_labels) for verification in cleaned_verifications ) and any( verification.issubset(sibling_node_labels) for verification in sibling_node.verification ):
                            cleaned_verifications.add( frozenset( sibling_node_labels ) )


            if cleaned_verifications == sibling_node.verification:
                '''sibling node status unchanged, no need to propagate further'''
                return
            sibling_node.verification = cleaned_verifications

            if sibling_node.is_verified():
                self._sibling_node_cache_cleaner(sibling_node)
                for parent_and_node in sibling_node.get_parent_and_nodes():
                    # self._propagate_and_node_verification(parent_and_node, set([sibling_node]))
                    self._propagate_and_node_verification( parent_and_node )
                return

            '''and propagate this information to parent AND nodes'''
            for parent_and_node in sibling_node.get_parent_and_nodes():
                # self._propagate_and_node_verification(parent_and_node, seen_nodes)
                self._propagate_and_node_verification(parent_and_node)

    def _cleaner_update(self, A, B, sibling_labels):
        for x in B:
            want_to_add = frozenset( label for label in x if not self._labels_to_or_node.get(label).sibling_node.is_verified() and label not in sibling_labels )
            supersets = set()
            is_superset = False
            for z in A:
                if z <= want_to_add:
                    is_superset = True
                    break
                elif z > want_to_add:
                    supersets.add(z)
            if is_superset:
                continue

            A.add( want_to_add )
            A.difference_update(supersets)


    def _cleaner_cartesian_product( self, A, B ):
        '''Two sets A and B, with sets of tilings (can be thought of as integers).
        We want to take all (a,b) in A x B, and take the union a u b, and then
        return all those that are not superset of another.'''
        intermediate_answer = set()
        for x in A:
            temp_B = sorted( set( y - x for y in B ), key = len )
            for y in temp_B:
                want_to_add = x.union(y)
                supersets = set()

                is_superset = False

                for z in intermediate_answer:
                    if z <= want_to_add:
                        is_superset = True
                        break
                    elif z > want_to_add:
                        supersets.add(z)
                if is_superset:
                    continue
                if want_to_add is frozenset():
                    '''Everything else is a superset of this'''
                    return set( [frozenset()] )
                intermediate_answer.add( want_to_add )
                intermediate_answer = intermediate_answer - supersets

        return intermediate_answer

    def _multiple_cleaner_products(self, child_verifications):
        if not child_verifications:
            return set()

        child_verifications.sort(key = len)

        current_product = set( frozenset( label for label in x if not self._labels_to_or_node.get(label).sibling_node.is_verified() ) for x in child_verifications[0] )
        child_verifications = child_verifications[1:]

        while child_verifications:
            current_child_verifications = set( frozenset( label for label in x if not self._labels_to_or_node.get(label).sibling_node.is_verified() ) for x in child_verifications[0] )
            child_verifications = child_verifications[1:]
            current_product = self._cleaner_cartesian_product(current_product, current_child_verifications)

        return current_product


    def find_proof_tree(self):
        if self.has_proof_tree():
            proof_tree = ProofTree( self._find_proof_tree_below_or_node(self.root_or_node) )
            return proof_tree
        else:
            print("There is no proof tree yet. Use the do_level function to try and find one.")


    def _find_proof_tree_below_or_node(self, or_node, seen_tilings=None, in_tiling_or_nodes=None):
        '''Return the ProofTreeNode that is verified below the OR node.'''
        if seen_tilings is None:
            seen_tilings = set()
        if in_tiling_or_nodes is None:
            in_tiling_or_nodes = set()

        '''If the tiling has already been seen, we have a recursion.'''
        if or_node.tiling in seen_tilings:
            label = min( self._get_sibling_labels(or_node.sibling_node, force=True) )
            in_tiling = or_node.tiling
            for other_or_node in in_tiling_or_nodes:
                if other_or_node.sibling_node == or_node.sibling_node:
                    out_tiling = other_or_node.tiling
            return ProofTreeNode("recurse", in_tiling, out_tiling, or_node.sibling_node.get_relation(in_tiling, out_tiling), label, recurse=[] )

        '''We add the tilings from the SiblingNode. These can now be used for recursions.'''
        sibling_tilings = [ sibling_or_node.tiling for sibling_or_node in or_node.sibling_node ]
        seen_tilings.update( sibling_tilings )

        '''The tiling we come in to the node by.'''
        in_tiling = or_node.tiling

        '''We add it to the in tiling or nodes, these are used for finding out tiling when recursing.'''
        in_tiling_or_nodes.add(or_node)

        formal_step = None
        recurse = []

        for child_and_node in or_node.sibling_node.get_children_and_nodes():
            '''If the child AND node is verified'''
            if any( verification.issubset(seen_tilings) for verification in child_and_node.verification ):
                '''We use it for the next level'''
                assert len(child_and_node.parents) == 1
                '''Keep track of the strategy used by the verified AND node.'''
                formal_step = child_and_node.formal_step
                '''The tiling we left the ProofTreeNode by is the tiling on the parent of the AND node.'''
                out_tiling = child_and_node.parents[0].tiling
                '''The children are the ProofTreeNodes using the tilings of the strategy.'''
                if child_and_node.recursion:
                    recurse = child_and_node.back_maps
                children = [ self._find_proof_tree_below_or_node(child_or_node, seen_tilings, in_tiling_or_nodes ) for child_or_node in child_and_node.children ]
                '''We only want one tree'''
                break

        '''We should only get here after finding a strategy for the ProofTreeNode'''
        assert formal_step is not None
        label = min( self._get_sibling_labels(or_node.sibling_node, force=True) )
        if children:
            return ProofTreeNode(formal_step, in_tiling, out_tiling, or_node.sibling_node.get_relation(in_tiling, out_tiling), label, children=children, recurse=recurse)

        return ProofTreeNode(formal_step, in_tiling, out_tiling, or_node.sibling_node.get_relation(in_tiling, out_tiling), label, recurse=recurse)
