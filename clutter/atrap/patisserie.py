"""A smart implementation of the meta tree."""


import collections
import itertools
import tqdm
import sys


from builtins import dict
from grids import Tiling


from .recipes import all_cell_insertions
from .recipes import all_row_and_column_insertions
from .recipes import row_column_separations
from .verification import verify_tiling
from .recursion import reachable_tilings_by_reversibly_deleting
from .ProofTree import ProofTree, ProofTreeNode

import random

RECIPES = [all_cell_insertions, all_row_and_column_insertions]


def print(*args, **kwargs):
    pass


class Starter(object):
    def __init__(self, tiling):
        self.tiling = tiling

        self.verified = False
        self.self_verified = False
        self.recursively_verified = []

        self.child_batches = []
        self.parent_batches = []

    def __eq__(self, other):
        # TODO: Type checking, or whatever
        return self.tiling == other.tiling

    def __hash__(self):
        return hash(self.tiling)


class Batch(object):
    def __init__(self):
        self.label = ""

        self.verified = False

        self.child_starters = []
        self.parent_starters = []


class StarterCache(object):
    def __init__(self):
        self._cache = dict()

    def get(self, tiling):
        data = self._cache.get(tiling)
        if data is None:
            return None
        else:
            data[1] += 1
            return data[0]

    def cache(self, starter):
        self._cache[starter.tiling] = [starter, 1]


class Bakery(object):
    def __init__(self, input_set, recipes=RECIPES):
        # Store input set
        self.input_set = input_set

        # Set tiling class to display input set in the way we want
        # TODO: This will be deprecated
        Tiling.label(input_set, "X")

        # Store recipes
        self.recipes = tuple(recipes)

        # Create root starter
        tiling = Tiling({(0, 0): input_set})
        starter = Starter(tiling)

        # Create first batch
        batch = Batch()
        batch.label = "Original batch"
        batch.child_starters.append(starter)
        starter.parent_batches.append(batch)

        # Store first batch
        self.first_batch = batch

        # Seen starters and how often they have been seen
        self.seen_starters = StarterCache()
        self.seen_starters.cache(starter)

        # All starters with unverified tilings that have yet to be verified
        # by means other than self-verification
        self.frontier = [starter]

        # The last generation of starters made
        self.generation = 0

    def bake(self, verbose=False, file=sys.stdout):
        if self.frontier:
            self.generation += 1
            new_frontier = []

            l_bar = "{l_bar}"
            bar = "{bar}"
            r_bar = "|[{elapsed}<{remaining} @ {rate_fmt}]"
            bar_format = l_bar + bar + r_bar
            frontier_iterator = tqdm.tqdm(self.frontier,
                                          disable=not verbose,
                                          bar_format=bar_format,
                                          unit="starter",
                                          file=file,
                                          ncols=80,
                                          desc="Gen-"+str(self.generation))

            for frontier_starter in frontier_iterator:
                # Ready the "batch materials generator"
                derived = itertools.chain(*(recipe(frontier_starter.tiling,
                                                   self.input_set)
                                            for recipe in self.recipes))

                # If you want a probabalistic version or pick a single strategy for dealing with finite classes
                # if True: derived = random.sample(list(derived),2)
                # if True: derived = [random.choice(list(derived))]
                # if True: derived = [list(derived)[1]]
                # if True: derived = list(derived)[0:2]
                for label, tilings in derived:
                    # Construct each batch
                    derived_batch = Batch()
                    derived_batch.label = label

                    # Give the batch a parent
                    derived_batch.parent_starters.append(frontier_starter)

                    # Give the parent starter its child batch
                    frontier_starter.child_batches.append(derived_batch)

                    # A variable that says whether or not all derived
                    # starters were verified
                    all_verified = True

                    # Give the batch its starters
                    for tiling in tilings:
                        # Check if a derived starter for that tiling
                        # already exists

                        # For using row column separation.
                        tiling = row_column_separations(tiling, self.input_set)

                        cached_starter = self.seen_starters.get(tiling)

                        if cached_starter is None:
                            derived_starter = Starter(tiling)
                            self.seen_starters.cache(derived_starter)

                            # Verify starter

                            if verify_tiling(tiling, self.input_set):
                                print("Tiling verified:")
                                print(tiling)
                                derived_starter.verified = True
                                derived_starter.self_verified = True
                            else:
                                #print("Frontier extended")
                                # Add to new frontier
                                new_frontier.append(derived_starter)
                                # TODO
                                derived_starter.parent_batches.append(derived_batch)
                                ancestor_set = set(self.ancestral_starters(derived_starter))
                                for reachable_tiling, cells in reachable_tilings_by_reversibly_deleting(derived_starter.tiling, self.input_set.basis):
                                    if reachable_tiling in ancestor_set:
                                        print("Tiling RECURSIVELY verified!")
                                        print(tiling)
                                        print(reachable_tiling)
                                        derived_starter.verified = True
                                        derived_starter.recursively_verified.append((reachable_tiling, cells))
                                        break
                                derived_starter.parent_batches.pop()

                        else:
                            #print("Cache hit!")
                            # Unverified cached starter already existed
                            # TODO: Perhaps new ancestors gained for some
                            #       derived starters lower in the tree,
                            #       need to check those for recursion
                            derived_starter = cached_starter

                        # Give derived starter its parent and vice-versa
                        derived_starter.parent_batches.append(derived_batch)
                        derived_batch.child_starters.append(derived_starter)

                        # Update variable that says whether or not all starters
                        # of the batch were verified
                        all_verified &= derived_starter.verified

                    if all_verified:
                        #print("All verified for a batch!")
                        done = self._propagate_batch(derived_batch)
                        #print(done)
                        if done:
                            if verbose:
                                frontier_iterator.update()
                                frontier_iterator.close()
                            return True

            # Replace old frontier with new one
            self.frontier = new_frontier

            # Didn't verify the first batch
            return False
        else:
            raise RuntimeError("Ran out of frontier")

    def _propagate_batch(self, batch):
        """Propagate batch verification.

        Call on a batch whose child starters have all been verified, to
        propagate verification farther up the tree. Returns true if the
        propagation manages to verify the first batch (the root)."""


        #print("Calling propagate with batch:")
        #print(batch)

        # TODO: Do smarter with better data structure
        #       And probably different arguments

        # All the batches child starters are verified
        batch.verified = True

        if batch is self.first_batch:
            # First batch verified
            #print("Arrived at root batch")
            return True
        else:
            #print("Generic propagating")
            #print("Parent starters:")
            for parent_starter in batch.parent_starters:
                #print(parent_starter.tiling)
                if parent_starter.verified:
                    #print("Parent starter already verified!")
                    # Already been propagated to
                    continue

                # Parent starter verified by batch
                parent_starter.verified = True

                # Propagate starter verification farther up
                #print("Parent batches:")
                for parent_batch in parent_starter.parent_batches:
                    #print(parent_batch)
                    # Check if all the child starters of the batch above are
                    # verified, then we can propagate further (recurse)
                    if all(child_starter.verified
                           for child_starter
                           in parent_batch.child_starters):
                        if self._propagate_batch(parent_batch):
                            # First batch verified farther up
                            return True
            # First batch not verified
            return False

    def ancestral_starters(self, starter):
        ancestral_starters = {}
        starter_frontier = [starter]
        while starter_frontier:
            ancestral_starter = starter_frontier.pop()
            if ancestral_starter == self.first_batch.child_starters[0]:
                continue
            for parent_batch in ancestral_starter.parent_batches:
                if parent_batch is self.first_batch:
                    continue
                else:
                    starter_frontier.extend(parent_batch.parent_starters)
            if ancestral_starter is starter:
                continue
            else:
                ancestral_starters[ancestral_starter.tiling] = ancestral_starter
        return ancestral_starters

    def get_proof_tree(self):
        if self.first_batch.verified:
            root = self._tree_helper(self.first_batch.child_starters[0])
            proof_tree = ProofTree(root)
            return proof_tree
        else:
            return None

    def _tree_helper(self, starter):
        node = ProofTreeNode(starter.tiling)
        if starter.verified:
            if starter.self_verified:
                #node.verified_by.append(starter.tiling)
                node.formal_step += "Tiling now self verified"
            for tiling, cells in starter.recursively_verified:
                node.verified_by.append(tiling)
                node.formal_step += "Tiling recursively verified with cells " + str(cells)
        for batch in starter.child_batches:
            if batch.verified:
                node.formal_step += batch.label
                node.children = [self._tree_helper(child_starter)
                                 for child_starter in batch.child_starters]
                break
        return node