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

        self.end_tilings, self.forwards_maps = [], []
        for tiling, mapping in zip(*(strategy(start_tiling))):
            if not tiling.is_empty():
                self.end_tilings.append(tiling)
                self.forwards_maps.append(mapping)



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
                    if self.specification.tracking_region(end_tiling, traced_region):
                        continue
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

    def common_intersection(self, other):
        """Return True if all comon tilings are coloured the same with respect
        to other."""
        common_tilings = set(self.regions).intersection(other.regions)
        return all(self.get_coloured_region(t) == other.get_coloured_region(t)
                   for t in common_tilings)

    def extend(self, other):
        """Extend self with all of the regions given by self. Will raise an
        error if two tilings are coloured differentlt."""
        for tiling, region in other.regions.items():
            if tiling in self.regions:
                if self.get_coloured_region(tiling) != region:
                    raise ValueError(("Can not extend with a colour which"
                                      "contradicts my colour"))
        for tiling, region in other.regions.items():
            self.regions[tiling] = other.regions[tiling]

    def __str__(self):
        s = "The colour of the following tilings regions\n"
        for t, r in self.regions.items():
            s += str(t)
            s += "\n"
            s += str(r)
            s += "\n"
            s += str(self.specification.get_label(t))
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
            print(repr(start_tiling))
            raise KeyError("No rule with tiling as left hand side in the "
                           "specification.")

    def find_colour(self, tiling, region, other_tiling=None):
        """Return the colour which exactly colours the region of tiling.
        Return None if no such."""
        region = frozenset(region)
        res = None
        for colour in self.colours:
            if region == colour.get_coloured_region(tiling):
                if other_tiling is not None:
                    if not colour.get_coloured_region(other_tiling):
                        continue
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
            subs = [{colour.get_variable(): 1 for colour in self.colours}
                    for _ in rule.end_tilings]
            for colour in self.colours:
                first_variable = colour.get_variable()
                first_region = colour.get_coloured_region(rule.start_tiling)
                tiling_with_regions = rule.trace_region(first_region)
                for i, (tiling, region) in enumerate(tiling_with_regions):
                    second_colour = self.find_colour(tiling, region)
                    second_variable = (False if second_colour is None else
                                       second_colour.get_variable())
                    if second_variable:
                        subs[i][second_variable] *= first_variable

            if rule.constructor == "disjoint" or rule.constructor == "symmetry":
                rhs = reduce(add,
                             [self.get_function(tiling).subs(sub,
                                                             simultaneous=True)
                              for tiling, sub in zip(rule.end_tilings, subs)],
                             0)
            elif rule.constructor == "cartesian":
                rhs = reduce(mul,
                             [self.get_function(tiling).subs(sub,
                                                             simultaneous=True)
                              for tiling, sub in zip(rule.end_tilings, subs)],
                             1)
            elif rule.constructor == "other":
                # print("================NEW RULE================")
                # print(self.get_label(rule.start_tiling))
                # print(rule.start_tiling)
                # print(rule.formal_step)
                left_fuse_region, right_fuse_region = get_fuse_region(
                                                            rule.start_tiling,
                                                            rule.formal_step)
                both_fuse_region = left_fuse_region.union(right_fuse_region)
                rhs_func = self.get_function(rule.end_tilings[0])
                rhs_func = rhs_func.subs(subs[0], simultaneous=True)
                rhs = rhs_func
                # Find the colour/variable/type for the fusion.
                fuse_colour = self.find_colour(rule.end_tilings[0],
                                               left_fuse_region)
                fuse_region = fuse_colour.get_coloured_region(
                                                            rule.start_tiling)
                # print(fuse_region)
                # print(left_fuse_region)
                # print(right_fuse_region)
                # print(both_fuse_region)
                fuse_type = ("left" if fuse_region == left_fuse_region else
                             "right" if fuse_region == right_fuse_region else
                             "both" if fuse_region == both_fuse_region else
                             "empty" if not fuse_region else None)
                print(rule.start_tiling)
                print(left_fuse_region)
                print(right_fuse_region)
                print(both_fuse_region)
                print(fuse_region)
                assert fuse_type is not None, "unknown fuse type"

                fuse_variable = fuse_colour.get_variable()
                if fuse_type == "empty":
                    raise NotImplementedError("Not done the empty case :(")
                    # label = self.get_label(rule.start_tiling)
                    # variables = self.get_variables(rule.start_tiling)
                    # if fuse_variable in variables:
                    #     raise NotImplementedError("Not implemented case empty where the empty part moves.")
                    # x = sympy.abc.x
                    # new_func = "G_{}".format(label)
                    # newlhs = sympy.Function(new_func)(x, fuse_variable,
                    #                                   *variables)
                    # dummy_eq = sympy.Eq(lhs, newlhs.subs({fuse_variable: 1}))
                    # print(dummy_eq)
                    # equations.add(dummy_eq)
                    # lhs = newlhs
                    # fuse_type = "left"
                if fuse_type == "both":
                    raise NotImplementedError(("Not implemented fuse type '{}'"
                                               "".format(fuse_type)))
                both_colours = self.find_colours(rule.start_tiling,
                                                 both_fuse_region)
                left_colours = [c for c in self.find_colours(rule.start_tiling,
                                                             left_fuse_region)
                                if c not in both_colours]
                right_colours = [c for c in self.find_colours(
                                          rule.start_tiling, right_fuse_region)
                                 if c not in both_colours]

                # both_variable = reduce(mul, [c.get_variable()
                #                              for c in both_colours], 1)
                # print("both:", both_variable)
                left_variable = reduce(mul,
                                       [1/c.get_variable()
                                        for c in right_colours
                                        if c != fuse_colour],
                                       (fuse_variable
                                        if fuse_type == "left" else 1))
                # print("left:", left_variable)
                right_variable = reduce(mul,
                                       [1/c.get_variable()
                                        for c in left_colours
                                        if c != fuse_colour],
                                       (fuse_variable
                                        if fuse_type == "right" else 1))
                # print("right:", right_variable)
                # print("fuse:", fuse_variable)

                # print("start_func:", rhs_func)
                # if both_variable == 1:
                # if left_variable == 1 and right_variable == 1:
                #     # derivative with respect to fuse variable
                #     raise NotImplementedError("Track nothing not implemented.")
                rhs = (1/(left_variable - right_variable) *
                        (left_variable*rhs_func.subs({fuse_variable:
                                                      left_variable}) -
                         right_variable*rhs_func.subs({fuse_variable:
                                                       right_variable})))
                # else:
                #     rhs = rhs_func * sympy.Function("DOITYOURSELF")(sympy.abc.x)
                #     raise NotImplementedError("Can't handle non-trivial both variable.")
            else:
                raise NotImplementedError("Can't do it :(")
            # print("!================================NEW EQUATION!================================")
            # print(rule.start_tiling)
            # print(lhs, "=", rhs)
            # for et in rule.end_tilings:
            #     print(et)
            #     print(self.get_function(et))
            #     print(self.get_variables(et))
            equations.add(sympy.Eq(lhs, rhs))
        for tiling in self.verified_nodes:
            lhs = self.get_function(tiling)
            # TODO: redo enumeration code for tree factors
            rhs = sympy.Function("VERIFIEDNODE")(sympy.abc.x, *self.get_variables(tiling))

            subs = {colour.get_variable(): 1 for colour in self.colours
                    if not colour.is_coloured(tiling)}
            equations.add(sympy.Eq(lhs, rhs.subs(subs)))

        return equations

    def add_colour(self, start_tiling, region, seen=set()):
        """Add a new colour to the specification."""
        if (start_tiling, frozenset(region)) in seen:
            return
        else:
            seen.add((start_tiling, frozenset(region)))
        if not self.tracking_region(start_tiling, region):
            new_colour = Colour(start_tiling, region, self)
            self.colours.append(new_colour)

    def tracking_region(self, tiling, region):
        """Return True if there is a colour that tracks this region on the
        tiling."""
        return any(colour.get_coloured_region(tiling) == region
                   for colour in self.colours)

    def cleanup_colours(self):
        """Remove all colours that are a subset of another colour and combine
        those that share a common intersection."""
        # remove subcolours
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

        indices_to_remove = []
        # combine colours which agree upon intersections
        for i in range(len(self.colours) - 1):
            for j in range(i + 1, len(self.colours)):
                if i in indices_to_remove or j in indices_to_remove:
                    continue
                colour1 = self.colours[i]
                colour2 = self.colours[j]
                if colour1.common_intersection(colour2):
                    print("COMMON")
                    colour1.extend(colour2)
                    indices_to_remove.append(j)
        self.colours = [colour for i, colour in enumerate(self.colours)
                        if i not in indices_to_remove]

    def __add_rules(self, proof_tree):
        """Will add the rules implied by the proof tree."""
        def add_symmetries(node):
            print(node.eqv_explanations)
            return

        for node in proof_tree.nodes():
            start_tiling = node.eqv_path_objects[0]
            if not node.recursion:
                if len(node.eqv_path_objects) > 1:
                    raise ValueError("Proof tree must be found using forward "
                                     "equivalence.")
                if node.strategy_verified:
                    self.verified_nodes.add(start_tiling)
                else:
                    constructor = ("disjoint" if node.disjoint_union
                                   else "cartesian" if node.decomposition
                                   else "other")
                    if start_tiling in self.rules:
                        assert self.rules[start_tiling].formal_step == node.formal_step, "on lhs twice"
                    self.rules[start_tiling] = Rule(start_tiling,
                                                    node.formal_step,
                                                    constructor)
            else:
                if len(node.eqv_path_objects) > 1:
                    assert len(node.eqv_path_objects) == 2
                    formal_step = node.eqv_explanations[0]
                    add_symmetries(node)
                    constructor = "symmetry"
                    if start_tiling in self.rules:
                        print(node.eqv_path_labels)
                        print(start_tiling)
                        print(formal_step)
                        print(self.rules[start_tiling].formal_step)
                        assert self.rules[start_tiling].formal_step == formal_step, "on lhs twice"
                    self.rules[start_tiling] = Rule(start_tiling,
                                                    formal_step,
                                                    constructor)


    def pretty_print_equations(self):
        """Return a string for all equations which can be read by Maple."""
        equations = "eqs := [\n"
        equations += ",\n".join("{} = {}".format(eq.lhs, eq.rhs)
                                for eq in self.get_equations())
        equations += "\n]:"
        return equations

    def sage_input(self):
        def get_variables(func):
            name, variables = func.split("(")
            return name, variables.split(")")[0].split(", ")
        def get_rest_and_func(func):
            if "F" in func:
                rest, func = func.split("F")
                func = "F" + func
            elif "G" in func:
                rest, func = func.split("G")
                func = "G" + func
            return rest, func
        def substitute(func, variables):
            string = ", ".join("{} = {}".format(x, y) for x, y in zip(variables_dict[func], variables) if x != y)
            if string:
                return ".subs({})".format(string)
            else:
                return ""
        def fuse_fixer(partial_eq):
            print(partial_eq)
            partial_eq_split = partial_eq.split("(")
            right = "(".join(x for x in partial_eq_split[1:])
            left = partial_eq_split[0]
            split_lhs = left.split("*")
            func = split_lhs[-1]
            rest, func = get_rest_and_func(func)
            rest = rest + "*".join(x for x in split_lhs[:-1])
            right = right[:-1]
            variables = right.split(", ")
            return "{}find_power_series({}){}".format(rest + "*" if rest != "-" and rest else rest, func, substitute(func, variables))


        def sage_eq(eq):
            lhs, rhs = str(eq.lhs), str(eq.rhs)
            final_lhs, variables = get_variables(lhs)
            if "VERIFIED" in rhs:
                final_rhs = rhs
            elif "/" in rhs:
                top, bottom = eq.rhs.expand().as_numer_denom()
                print(eq.rhs)
                print(top)
                print(bottom)
                top = top.expand()
                bottom = str(bottom)
                left, right = top.expand().as_ordered_terms()
                left = fuse_fixer(str(left.expand()))
                right = fuse_fixer(str(right.expand()))
                top = "({} {} {})".format(left, "+", right)
                final_rhs = "({})/({})".format(top, bottom)
            elif "+" in rhs:
                functions = rhs.split(" + ")
                rhs_rest_and_funcs = [get_rest_and_func(func) for func in functions]
                print("a", rhs_rest_and_funcs)
                rhs_name_and_variables = [get_variables(func) for _, func in rhs_rest_and_funcs]
                print("b", rhs_name_and_variables)
                final_rhs = " + ".join("find_power_series({}{}){}".format(name, rest, substitute(name, rhs_variables)) for (rest, _), (name, rhs_variables) in zip(rhs_rest_and_funcs, rhs_name_and_variables))
            else:
                functions = rhs.split("*F")
                print(functions)
                if len(functions) > 1:
                    functions = ([functions[0]] +
                                 ["F" + func for func in functions[1:]])
                rhs_rest_and_funcs = [get_rest_and_func(func) for func in functions]
                print("a", rhs_rest_and_funcs)
                rhs_name_and_variables = [get_variables(func) for _, func in rhs_rest_and_funcs]
                print("b", rhs_name_and_variables)
                final_rhs = " * ".join("find_power_series({}{}){}".format(name, rest, substitute(name, rhs_variables)) for (rest, _), (name, rhs_variables) in zip(rhs_rest_and_funcs, rhs_name_and_variables))
            return "{} = {}".format(final_lhs, final_rhs)

        eqs = self.get_equations()
        variables_dict = {}
        for eq in eqs:
            lhs = str(eq.lhs)
            name, variables = get_variables(lhs)
            variables_dict[name] = variables
        all_variables = list(sorted(set(chain(*(get_variables(str(eq.lhs))[1] for eq in eqs)))))

        taylor = "def find_power_series(f, N=8):\n    return " + "taylor("* len(all_variables) + "f, "
        taylor += ", ".join("{}, 0, N)".format(v) for v in all_variables)
        variables = ", ".join(v for v in all_variables)
        variables = "{} = var('{}')".format(variables, variables)
        initial = "\n".join("{} = 0".format(name) for name in variables_dict)
        equations = "\n    ".join(sage_eq(eq) for eq in eqs)
        subs = ", ".join("{} = 1".format(v) for v in all_variables if v != 'x')
        print_statement = "\n    ".join("print '{}', find_power_series({}).subs({}).coefficients(sparse=False)".format(name, name, subs) for name in variables_dict)
        code = "{}\n\n{}\n\n{}\n\nfor i in range(20):\n    {}\n\n    print i\n    {}\n    print ''".format(variables, taylor, initial, equations, print_statement)
        return code

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

    with open("tree.txt") as f:
        line = list(f)[0]
        d = json.loads(line)
        tree = ProofTree.from_dict(Tiling, d)
        # try:
        colourspec = ColouredSpecification(tree)
        for rule in colourspec.get_rules():
            if rule.constructor == "other":
                region, _ = get_fuse_region(rule.start_tiling, rule.formal_step)
                colourspec.add_colour(rule.end_tilings[0], region)
        colourspec.cleanup_colours()
        colourspec.cleanup_colours()
        print(colourspec.sage_input())
        print(colourspec.pretty_print_equations())
        # colourspec.show_colours()
        for tiling, label in colourspec.labels.items():
            print(label)
            print(tiling)
            print([len(list(tiling.gridded_perms_of_length(i))) for i in range(8)])

        # except (AssertionError, ValueError, NotImplementedError) as e:
        #     print(e)

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

    # from tilescopethree import TileScopeTHREE, StrategyPacks
    # with open("some_bases.txt", 'r') as f:
    #     for line in f:
    #         print(line.strip())
    #         tiling = Tiling.from_string(line.strip())
    #         tilescope = TileScopeTHREE(tiling, StrategyPacks.negative_row_placements_fusion)
    #         tree = tilescope.auto_search(max_time=30)
    #         if tree is not None:
    #             try:
    #                 colourspec = ColouredSpecification(tree)
    #                 for rule in colourspec.get_rules():
    #                     if rule.constructor == "other":
    #                         region, _ = get_fuse_region(rule.start_tiling, rule.formal_step)
    #                         colourspec.add_colour(rule.end_tilings[0], region)
    #                 colourspec.cleanup_colours()
    #                 print(colourspec.pretty_print_equations())
    #             except (AssertionError, ValueError, NotImplementedError, RecursionError) as e:
    #                 print(e)

