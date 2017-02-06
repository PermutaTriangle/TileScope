"""A smart implementation of the meta tree."""


import collections
import itertools


from builtins import dict
from grids import Tiling


from .recipes import all_cell_insertions
from .recipes import all_row_and_column_insertions
from .verification import verify_tiling


RECIPES = [all_cell_insertions, all_row_and_column_insertions]


class Starter(object):
    def __init__(self, tiling):
        self.tiling = tiling

        self.verified = False
        self.self_verified = False

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

    def bake(self):
        if self.frontier:
            new_frontier = []
            for frontier_starter in self.frontier:
                # Ready the "batch materials generator"
                derived = itertools.chain(*(recipe(frontier_starter.tiling,
                                                   self.input_set)
                                            for recipe in self.recipes))

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
                        else:
                            #print("Cache hit!")
                            # Unverified cached starter already existed
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

    def give_me_proof(self):
        if self.first_batch.verified:
            proof = []
            frontier = list(self.first_batch.child_starters)
            while frontier:
                starter = frontier.pop()

                verified_batch = None
                for child_batch in starter.child_batches:
                    if child_batch.verified:
                        verified_batch = child_batch
                        break

                if verified_batch is None:
                    raise RuntimeError("No batch verifies a verified starter")

                for child_starter in verified_batch.child_starters:
                    assert child_starter.verified
                    if child_starter.self_verified:
                        proof.append(child_starter.tiling)
                    else:
                        frontier.append(child_starter)
            return proof
        else:
            return None
