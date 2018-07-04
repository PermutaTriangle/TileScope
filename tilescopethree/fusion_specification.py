"""A specialised class for enumerating ProofTrees found by forward
equivalence."""

from collections import defaultdict
from comb_spec_searcher import ProofTree
from functools import partial, reduce
from permuta import Perm
from grids_three import Tiling
from grids_three.misc import union_reduce
from operator import add, mul
from sympy import Function, Eq, var

from tilescopethree.strategies.equivalence_strategies.point_placements import place_point_of_requirement
from tilescopethree.strategies.equivalence_strategies.fusion import fuse_tiling
from tilescopethree.strategies import row_and_column_separation


class Rule(object):
    """A combinatorial that tracks how regions expand."""
    def __init__(self, start_tiling, end_tilings, start_label, end_labels,
                 formal_step):
        """Parse the formal step to be able to trace regions of rules."""
        self.start_label = start_label
        if "Placing point" in formal_step:
            _, ri, i, DIR, _ = formal_step.split("|")
            rule = place_point_of_requirement(start_tiling, int(ri), int(i),
                                              int(DIR), regions=True)
            self.constructor = "disjoint"
        elif "Insert " in formal_step:
            _, c1, c2, patt, _ = formal_step.split("|")
            cell = (int(c1), int(c2))
            patt = Perm.to_standard(patt)
            avoids = start_tiling.add_single_cell_obstruction(patt, cell)
            contains = start_tiling.add_single_cell_requirement(patt, cell)
            rule = ([avoids, contains],
                    [{c: set([avoids.forward_map[c]])
                      for c in start_tiling.active_cells
                      if (c in avoids.forward_map and
                          avoids.forward_map[c] in
                          avoids.active_cells)},
                     {c: set([contains.forward_map[c]])
                      for c in start_tiling.active_cells
                      if (c in contains.forward_map and
                          contains.forward_map[c] in
                          contains.active_cells)}])
            self.constructor = "disjoint"
        elif "factors of the tiling." in formal_step:
            rule = start_tiling.find_factors(regions=True)
            self.constructor = "cartesian"
        elif "Separated rows" in formal_step:
            rule = row_and_column_separation(start_tiling, regions=True)
            self.constructor = "disjoint"
        elif "Fuse rows" in formal_step:
            _, row_index, _ = formal_step.split("|")
            rule = fuse_tiling(start_tiling, int(row_index),
                               True, regions=True)
            self.constructor = "fusion"
        elif "Fuse columns" in formal_step:
            _, col_index, _ = formal_step.split("|")
            rule = fuse_tiling(start_tiling, int(col_index),
                               False, regions=True)
            self.constructor = "fusion"
        elif "The tiling is a subset of the class" in formal_step:
            rule = ([], [])
            self.constructor = "verified"
        else:
            raise NotImplementedError("Not tracking regions for: " + formal_step)
        self.start_tiling = start_tiling
        self.end_tilings, self.regions = rule
        empty = [t.is_empty() for t in self.end_tilings]
        self.end_tilings = [t for i, t in enumerate(self.end_tilings)
                            if not empty[i]]
        self.regions = [r for i, r in enumerate(self.regions)
                        if not empty[i]]
        self.formal_step = formal_step
        if set(self.end_tilings) != set(end_tilings):
            print("formal_step =", formal_step)
            print("start_tiling =", repr(self.start_tiling))
            print("end_tiling =", self.end_tilings)
        assert set(self.end_tilings) == set(end_tilings), "strategy gave different output second time round"
        labels = {t: l for t, l in zip(end_tilings, end_labels)}
        self.end_labels = [labels[t] for t in self.end_tilings]

    def get_equation(self, regions, variables, fusion_regions, get_function,
                     root_func, root_class):
        lhs = get_function(self.start_label)

        def get_subs(out_index):
            out_tiling = self.end_tilings[out_index]
            # print(self.end_labels[out_index])
            # print(out_tiling.to_old_tiling())
            subs = {}
            for variable, region in zip(variables, regions):
                start_tiling_region = region[self.start_tiling] if self.start_tiling in region else set()
                out_tiling_region = region[out_tiling] if out_tiling in region else set()
                out_strat_region = union_reduce(self.regions[out_index][c] for c in start_tiling_region
                                                if c in self.regions[out_index])
                # if start_tiling_region:
                #     print("===============INTERESTINGINTERESTINGLOOKHEREHere==============================INTERESTINGINTERESTINGLOOKHEREHere==============================INTERESTINGINTERESTINGLOOKHEREHere===============")
                # print("start:", start_tiling_region)
                # print("out:", out_tiling_region)
                # print("strat:", out_strat_region)
                if not out_strat_region:
                    if out_tiling_region:
                        subs[variable] = 1
                else:
                    assert out_strat_region == out_tiling_region, "region not the same as strategy implied region so need a new substitution"
            return subs

        # print("===============NEW RULE===============")
        # print(self.start_tiling.to_old_tiling())


        if self.constructor == "disjoint":
            funcs = [get_function(l).subs(get_subs(i)) for i, l in enumerate(self.end_labels)]
            rhs = reduce(add, funcs, 0)
        if self.constructor == "cartesian":
            funcs = [get_function(l).subs(get_subs(i)) for i, l in enumerate(self.end_labels)]
            rhs = reduce(mul, funcs, 1)
        if self.constructor == "verified":
            rhs = get_genf_with_region(self.start_tiling,
                                       [region[self.start_tiling] if self.start_tiling in region else set()
                                        for region in regions], variables,
                                       root_func, root_class)
        if self.constructor == "fusion":
            _, row_index, _ = self.formal_step.split("|")
            row = "row" in self.formal_step
            fuse_variable = None
            fuse_type = None
            subs = {}
            for i, variable, region, fusion_region in zip(range(len(variables)), variables, regions, fusion_regions):
                start_region = region[self.start_tiling] if self.start_tiling in region else set()
                fuse_tiling, fuse_region = fusion_region
                if fuse_tiling == self.end_tilings[0]:
                    fuse_variable = variable
                    if len(start_region) == 1:
                        fuse_subs = {variable: 1}
                        fuse_type = 1
                    elif len(start_region) == 2:
                        fuse_type = 2
                    elif not start_region:
                        fuse_type = 3
                    else:
                        if not fuse_region:
                            subs[variable] = 1
                        else:
                            # print(self.start_tiling.to_old_tiling())
                            # print(fuse_tiling.to_old_tiling())
                            # print(fuse_region)
                            # print(start_region)
                            assert fuse_region == start_region, "region fusion happens different to start region"
                else:
                    subs = {**subs, **get_subs(0)}
            assert fuse_variable is not None, "no fuse variable found"
            assert fuse_type is not None, "fusion type unknown"
            out_func = get_function(self.end_labels[0])
            if fuse_type == 1:
                rhs = 1/(1-fuse_variable) * (out_func.subs({**subs, **fuse_subs}) - fuse_variable*out_func.subs(subs))
            elif fuse_type == 2:
                raise NotImplementedError("Can't handle fusion type 2.")
            elif fuse_type == 3:
                raise NotImplementedError("Can't handle fusion type 3.")
        # print(lhs,"=", rhs)
        return Eq(lhs, rhs)


class Specification(object):
    def __init__(self, tree):
        """Initialises with a forward equivalence ProofTree object.."""
        assert isinstance(tree, ProofTree), "Input not ProofTree"
        self.rules = {}
        for node in tree.nodes():
            if node.recursion:
                continue
            if len(node.eqv_path_objects) > 1:
                for i, first in enumerate(node.eqv_path_objects[:-1]):
                    second = node.eqv_path_objects[i + 1]
                    start_label = node.eqv_path_labels[i]
                    end_labels = [node.eqv_path_labels[i + 1]]
                    formal_step = node.eqv_explanations[i]
                    self.rules[first] = Rule(first, [second], start_label,
                                             end_labels, formal_step)
            start_tiling = node.eqv_path_objects[-1]
            end_tilings = [child.eqv_path_objects[0]
                           for child in node.children]
            start_label = node.eqv_path_labels[-1]
            end_labels = [child.eqv_path_labels[0] for child in node.children]
            formal_step = node.formal_step
            assert (start_tiling not in self.rules or node.strategy_verified), "More than one rule with same left hand side"
            self.rules[start_tiling] = Rule(start_tiling, end_tilings,
                                            start_label, end_labels,
                                            formal_step)
        self.fusion_regions = self._regions_to_track()
        self.regions = self._get_regions()
        self.variables = var(["y[{}]".format(i)
                              for i in range(len(self.regions))])
        self.functions = {}
        self.root_class = tree.root.eqv_path_objects[0]
        self.root_func = self.get_function(tree.root.eqv_path_labels[0])

    def get_function(self, label):
        if label not in self.functions:
            func_string = "F[{}]".format(label)
            func = Function(func_string)(var('x'), *self.variables)
            self.functions[label] = func
        return self.functions[label]

    def _regions_to_track(self):
        """
        Return regions that need to be tracked.

        Takes in dictionary of rules and returns dictionary of tilings with cells
        that need to be tracked.
        """
        regions = []
        for _, rule in self.rules.items():
            if "Fuse" in rule.formal_step:
                row = "row" in rule.formal_step
                row_index = int(rule.formal_step.split(' ')[2])
                end_tiling = rule.end_tilings[0]
                cells_to_track = tuple(c for c in end_tiling.active_cells
                                       if ((row and c[1] == row_index) or
                                           (not row and c[0] == row_index)))
                regions.append((end_tiling, set(cells_to_track)))
        return regions

    def _get_regions(self):
        """Return a list where each entry is a dictionary pointing from cells to a
        region that needs tracked by a catalytic variable."""
        regions = []
        for tiling, region in self.fusion_regions:
            tiling_to_region = {tiling: set(region)}
            queue = [tiling]
            while queue:
                curr = queue.pop(-1)
                rule = self.rules[curr]
                if "The tiling is a subset of the class" in rule.formal_step:
                    continue
                assert len(rule.regions) == len(rule.end_tilings), "length of regions and end_tilings do not match up in rule"
                for t, r in zip(rule.end_tilings, rule.regions):
                    region = union_reduce(r[c] for c in tiling_to_region[curr]
                                          if c in r)
                    if t in tiling_to_region:
                        assert (not region or not tiling_to_region[t] or
                                region == tiling_to_region[t]), "need a substitution other than y = 1, new variable?1"
                        if tiling_to_region[t] < region:
                            assert tiling_to_region[t] != region, "need a substitution other than y = 1, new variable?2"
                            queue.append(t)
                        tiling_to_region[t] = tiling_to_region[t].union(region)
                    else:
                        tiling_to_region[t] = region
                        queue.append(t)
            regions.append(tiling_to_region)
        return regions

    def get_equations(self):
        eqs = set()
        for rule in self.rules.values():
            eqs.add(rule.get_equation(self.regions, self.variables,
                                      self.fusion_regions, self.get_function,
                                      self.root_func, self.root_class))
        return eqs

def get_genf_with_region(tiling, regions_to_track, variables, root_func, root_class):
    if not all(region <= set(tiling.active_cells) for region in regions_to_track):
        print(regions_to_track)
        print(tiling.active_cells)
        raise ValueError("Region not an active cell.")
    if len(regions_to_track) != len(variables):
        raise ValueError("Number of regions should match number of variables.")
    factors, regions = tiling.find_factors(regions=True)
    if len(factors) > 1:
        f = 1
        for factor, strat_region in zip(factors, regions):
            new_regions_to_track = [union_reduce(strat_region[c]
                                                 for c in region
                                                 if c in strat_region)
                                    for region in regions_to_track]
            f *= get_genf_with_region(factor, new_regions_to_track, variables, root_func, root_class)
        return f
    if all(not region for region in regions_to_track):
        return tiling.get_genf(root_func=root_func, root_class=root_class)
    if tiling.dimensions == (1, 1):
        f = tiling.get_genf()
        for region, variable in zip(regions_to_track, variables):
            if (tiling in region and (0, 0) in region):
                f = f.subs({x: x * variable})
        return f

    def get_new_regions(other_tiling, other_regions_to_track=regions_to_track):
        print(regions_to_track)
        new_regions_to_track = []
        for region in regions_to_track:
            new_region = set(other_tiling.forward_map[c]
                             for c in region if c in region)
            new_regions_to_track.append(new_region)
        return new_regions_to_track

    for i, req_list in enumerate(tiling.requirements):
        if len(req_list) == 1:
            ignore = Tiling(obstructions=tiling.obstructions,
                            requirements=[req for j, req in enumerate(tiling.requirements) if i != j])
            req = tiling.requirements[i][0]
            avoids = ignore.add_obstruction(req.patt, req.pos)
            print(get_new_regions(ignore))
            return (get_genf_with_region(ignore, get_new_regions(ignore), variables, root_func, root_class) -
                    get_genf_with_region(avoids, get_new_regions(avoids, get_new_regions(ignore)), variables, root_func, root_class))
                        req = req_list[0]
        avoids = self.add_obstruction(req.patt, req.pos)
        contains = self.add_requirement(req.patt, req.pos)
        return (get_genf_with_region(avoids, get_new_regions(avoids), variables, root_func, root_class) +
                get_genf_with_region(contains, get_new_regions(contains), variables, root_func, root_class))
    raise NotImplementedError("Can't enumerate factor:\n" + repr(tiling))
