"""A specification for keeping track of regions of tilings.

We create a set Rules from the input of a proof tree. The Rule class has
    Rule: start_tiling, end_tiling, forward_map, constructor
and from any rule it should be possible to get an equation. The Colour class
has
    Colour: tilings -> cells which have this colour
and each Colour will return a unique catalytic variable. A Specification is
then a set of rules and colours
    Spec: Rules, Colours.
Each tiling in the specification will appear once as a start_tiling in a rule,
and have a unique function/variable assigneb to it.
"""

from collections import deque
from itertools import chain, product
from functools import reduce
from operator import add, mul

from grids_three import Tiling
from regions import get_fuse_region, parse_formal_step

import sympy

class Rule:
    """A class for a combinatorial rule of tilings. It keeps track of how the
    regions of the tiling change when the strategy is applied."""
    labels = {}
    def __init__(self, start_tiling, formal_step, constructor):
        self.start_tiling = start_tiling
        self.formal_step = formal_step
        self.constructor = constructor
        strategy = parse_formal_step(formal_step)
        self.end_tilings, self.forwards_maps = strategy(start_tiling)

    def trace_region(self, region_to_trace):
        """Return the list of pairs (tiling, region) of the end tilings and the
        region that corresponds to the region to trace in the start tiling."""
        region_to_trace = set(region_to_trace)
        if not region_to_trace <= self.start_tiling.active_cells:
            raise ValueError(("The region {} is not active on the start tiling"
                              "\n{}".format(region_to_trace,
                                            self.start_tiling)))
        res = []
        for end_tiling, forward_map in zip(self.end_tilings,
                                           self.forwards_maps):
            traced_region = set(chain(*[forward_map[c] if c in forward_map else set()
                                      for c in region_to_trace]))
            res.append((end_tiling, traced_region))

        return res


class Colour:
    """A colour represents a region of points within the specification that is
    traced by applying strategies."""
    variable_counter = 0
    def __init__(self, initial_tiling, initial_region, spec):
        self.initial_tiling = initial_tiling
        # a dictionary pointing from tiling to the region with this colour.
        self.regions = {initial_tiling: frozenset(initial_region)}
        self.specification = spec
        new_colours = self.trace_colour()
        # add the colours needed in order to trace this colour
        for tiling, region in new_colours:
            self.specification.add_colour(tiling, region)

    def get_variable(self):
        if not hasattr(self, "variable"):
            self.variable = sympy.var("y_{}".format(self.variable_counter))
            Colour.variable_counter += 1
        return self.variable

    def get_coloured_region(self, tiling):
        """Return the region of the tiling that has this colour."""
        try:
            return self.regions[tiling]
        except KeyError:
            return frozenset()

    def is_coloured(self, tiling):
        """Return True if the tiling is colourd by the colour,
        i.e. has a non empty region using this colour."""
        return tiling in self.regions

    def trace_colour(self):
        """This will trace the colour through the rules. It returns a list of
        (tiling, region) pairs of tilings whose regions need to be tracked to
        ensure tracking of the original colour."""
        queue = deque([self.initial_tiling])
        seen = set()
        # for collecting colours that need to be traced.
        new_colours = []
        while queue:
            start = queue.popleft()
            if start in seen or self.specification.is_verified(start):
                continue
            else:
                seen.add(start)
            coloured_region = self.get_coloured_region(start)
            rule = self.specification.get_rule(start)
            for end_tiling, traced_region in rule.trace_region(coloured_region):
                if traced_region:
                    if end_tiling in self.regions:
                        if not frozenset(traced_region) == self.regions[end_tiling]:
                            new_colours.append((end_tiling, traced_region))
                    else:
                        self.regions[end_tiling] = frozenset(traced_region)
                        queue.append(end_tiling)
        return new_colours

    def is_subset(self, other):
        """Return True if other colour is a subset of self."""
        try:
            return all((self.get_coloured_region(tiling) ==
                        other.get_coloured_region(tiling))
                       for tiling in other.regions)
        except AttributeError:
            raise AttributeError("Checking for a subset uses a Colour object.")

    def __str__(self):
        s = "The colour of the following tilings regions\n"
        for t, r in self.regions.items():
            s += str(t)
            s += "\n"
            s += str(r)
            s += "\n"
        return s


class ColouredSpecification:
    """A specification with coloured regions. This class can be used to find
    the equations of a tree where regions need to be tracked.

    The tree must be found by forward equivlance."""
    labels = {}
    def __init__(self, proof_tree):
        # All the tilings that are verified by the specification.
        self.verified_nodes = set()
        # A dictionary from tiling to rule it is the left hand side of.
        self.rules = {}
        self.colours = []
        self.__add_rules(proof_tree)

    def get_function(self, tiling):
        """Return the function corresponding to a tiling."""
        label = self.get_label(tiling)
        variables = self.get_variables(tiling)
        x = sympy.abc.x
        return sympy.Function("F_{}".format(label))(x, *variables)

    def get_label(self, tiling):
        """Return the label for a tiling."""
        if tiling not in self.labels:
            self.labels[tiling] = len(self.labels)
        return self.labels[tiling]

    def get_variables(self, tiling):
        """Return the variables implied by the colours for a tiling."""
        return tuple(colour.get_variable() for colour in self.colours
                        if colour.is_coloured(tiling))

    def is_verified(self, tiling):
        """Return True if the tiling is verified."""
        return tiling in self.verified_nodes

    def get_rules(self):
        """Return a list containing all rules."""
        return list(self.rules.values())

    def get_rule(self, start_tiling):
        try:
            return self.rules[start_tiling]
        except KeyError:
            raise KeyError("No rule with tiling as left hand side in the "
                           "specification.")

    def find_colour(self, tiling, region):
        """Return the colour which exactly colours the region of tiling.
        Return None if no such."""
        region = frozenset(region)
        res = None
        for colour in self.colours:
            if region == colour.get_coloured_region(tiling):
                # print(self.get_label(tiling))
                # if res is not None:
                #     print("COLOUR 1:")
                #     for t, r in sorted(res.regions.items(), key=lambda x: self.get_label(x[0])):
                #         print(self.get_label(t), r)
                #     print("COLOUR 2:")
                #     for t, r in sorted(colour.regions.items(), key=lambda x: self.get_label(x[0])):
                        # print(self.get_label(t), r)
                # assert res is None, "Same region twice"
                return colour
        return res

    def find_colours(self, tiling, region):
        """Return the colours which colour the region of tiling."""
        region = frozenset(region)
        res = []
        for colour in self.colours:
            if region <= colour.get_coloured_region(tiling):
                res.append(colour)
        return res

    def get_equations(self):
        """Return system of equations implied by the specification."""
        equations = set()
        for rule in self.get_rules():
            lhs = self.get_function(rule.start_tiling)
            if rule.constructor == "disjoint":
                rhs = reduce(add, [self.get_function(tiling)
                                   for tiling in rule.end_tilings], 0)
            elif rule.constructor == "cartesian":
                rhs = reduce(mul, [self.get_function(tiling)
                                   for tiling in rule.end_tilings], 1)
            elif rule.constructor == "other":
                left_fuse_region, right_fuse_region = get_fuse_region(
                                                            rule.start_tiling,
                                                            rule.formal_step)

                # Find the colour/variable that the fusion step happens to.
                colour = self.find_colour(rule.end_tilings[0],
                                          left_fuse_region)

                # print(rule.start_tiling)
                # print(left_fuse_region)
                # print(self.get_label(rule.start_tiling))
                fuse_variable = colour.get_variable()

                # both_colours = self.find_colours(rule.start_tiling,
                #                                  (left_fuse_region +
                #                                   right_fuse_region))
                left_colours = [c for c in self.find_colours(rule.start_tiling,
                                                             left_fuse_region)]
                                # if c not in both_colours]
                right_colours = [c for c in self.find_colours(rule.start_tiling,
                                                              right_fuse_region)]
                                # if c not in both_colours]
                # both_variable = reduce(mul, [c.get_variable()
                #                              for c in both_colours], 1)
                # print("both:", both_variable)
                left_variable = reduce(mul, [c.get_variable()
                                             for c in left_colours], 1)
                # print("left:", left_variable)
                right_variable = reduce(mul, [c.get_variable()
                                              for c in right_colours], 1)
                # print("right:", right_variable)
                # print("fuse:", fuse_variable)
                rhs_func = self.get_function(rule.end_tilings[0])
                # if both_variable == 1:
                if left_variable == 1 and right_variable == 1:
                    # derivative with respect to fuse variable
                    raise NotImplementedError("Track nothing not implemented.")
                rhs = (1/(right_variable - left_variable) *
                        (right_variable*rhs_func.subs({fuse_variable:
                                                        fuse_variable/left_variable}) -
                         left_variable*rhs_func.subs({fuse_variable:
                                                        fuse_variable/right_variable})))
                # else:
                #     rhs = rhs_func * sympy.Function("DOITYOURSELF")(sympy.abc.x)
                #     raise NotImplementedError("Can't handle non-trivial both variable.")
            else:
                raise NotImplementedError("Can't do it :(")
            subs = {colour.get_variable(): 1 for colour in self.colours
                    if not colour.is_coloured(rule.start_tiling)}
            equations.add(sympy.Eq(lhs, rhs.subs(subs)))
        for tiling in self.verified_nodes:
            lhs = self.get_function(tiling)
            # TODO: redo enumeration code for tree factors
            rhs = sympy.Function("VERIFIEDNODE")(sympy.abc.x, *self.get_variables(tiling))
            subs = {colour.get_variable(): 1 for colour in self.colours
                    if not colour.is_coloured(tiling)}
            equations.add(sympy.Eq(lhs, rhs.subs(subs)))

        return equations

    def add_colour(self, start_tiling, region):
        """Add a new colour to the specification."""
        new_colour = Colour(start_tiling, region, self)
        self.colours.append(new_colour)

    def cleanup_colours(self):
        """Remove all colours that are a subset of another colour."""
        indices_to_remove = []
        for i in range(len(self.colours) - 1):
            for j in range(i + 1, len(self.colours)):
                if i in indices_to_remove or j in indices_to_remove:
                    continue
                colour1 = self.colours[i]
                colour2 = self.colours[j]
                if colour1.is_subset(colour2):
                    indices_to_remove.append(j)
                elif colour2.is_subset(colour1):
                    indices_to_remove.append(i)
        self.colours = [colour for i, colour in enumerate(self.colours)
                        if i not in indices_to_remove]

    def __add_rules(self, proof_tree):
        """Will add the rules implied by the proof tree."""
        for node in proof_tree.nodes():
            if not node.recursion:
                if len(node.eqv_path_objects) > 1:
                    raise ValueError("Proof tree must be found using forward "
                                     "equivalence.")
                start_tiling = node.eqv_path_objects[0]
                if node.strategy_verified:
                    self.verified_nodes.add(start_tiling)
                else:
                    constructor = ("disjoint" if node.disjoint_union
                                   else "cartesian" if node.decomposition
                                   else "other")
                    assert start_tiling not in self.rules, "on lhs twice"
                    self.rules[start_tiling] = Rule(start_tiling,
                                                    node.formal_step,
                                                    constructor)

    def pretty_print_equations(self):
        """Return a string for all equations which can be read by Maple."""
        equations = "eqs := [\n"
        equations += ",\n".join("{} = {}".format(eq.lhs, eq.rhs)
                              for eq in self.get_equations())
        equations += "\n]:"
        return equations

    def show_rules(self):
        for start, rule in self.rules.items():
            print()
            assert start == rule.start_tiling
            print("The left hand side is:")
            print(rule.start_tiling)
            print("The right hand side is:")
            for t in rule.end_tilings:
                print(t)
            print("with formal step: {}".format(rule.formal_step))
            print("using the constructor {}".format(rule.constructor))

    def show_colours(self):
        for i, colour in enumerate(self.colours):
            print("================COLOUR {}================".format(i))
            print(colour)

if __name__ == "__main__":
    import json
    from comb_spec_searcher import ProofTree

    # with open("all_fusion_trees.txt", 'r') as f:
    #     for line in f:
    #         d = json.loads(line)
    #         tree = ProofTree.from_dict(Tiling, d)

    #         try:
    #             colourspec = ColouredSpecification(tree)
    #             for rule in colourspec.get_rules():
    #                 if rule.constructor == "other":
    #                     region, _ = get_fuse_region(rule.start_tiling, rule.formal_step)
    #                     colourspec.add_colour(rule.end_tilings[0], region)
    #             colourspec.cleanup_colours()
    #             print(colourspec.pretty_print_equations())
    #         except (AssertionError, ValueError, NotImplementedError) as e:
    #             print(e)

    from tilescopethree import TileScopeTHREE, StrategyPacks
    with open("some_bases.txt", 'r') as f:
        for line in f:
            print(line.strip())
            tiling = Tiling.from_string(line.strip())
            tilescope = TileScopeTHREE(tiling, StrategyPacks.negative_row_placements_fusion)
            tree = tilescope.auto_search(max_time=30)
            if tree is not None:
                try:
                    colourspec = ColouredSpecification(tree)
                    for rule in colourspec.get_rules():
                        if rule.constructor == "other":
                            region, _ = get_fuse_region(rule.start_tiling, rule.formal_step)
                            colourspec.add_colour(rule.end_tilings[0], region)
                    colourspec.cleanup_colours()
                    print(colourspec.pretty_print_equations())
                except (AssertionError, ValueError, NotImplementedError, RecursionError) as e:
                    print(e)

