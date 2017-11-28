"""
A proof tree class.

This has been built specific to tilings and gridded perms. Needs to be
generalised.
"""

from .tree_searcher import Node as tree_searcher_node
from permuta.misc.ordered_set_partitions import partitions_of_n_of_size_k

import sys


class ProofTreeNode(object):
    def __init__(self, label, eqv_path_labels, eqv_path_objects,
                 eqv_explanations=[], children=[], strategy_verified=False,
                 comlement_verified=False, decomposition=False,
                 disjoint_union=False, recursion=False, formal_step="",
                 back_maps=None, forward_maps=None):
        self.label = label
        self.eqv_path_labels = eqv_path_labels
        self.eqv_path_objects = eqv_path_objects
        self.eqv_explanations = eqv_explanations

        self.children = children
        self.strategy_verified = strategy_verified
        self.complement_verified = comlement_verified
        self.decomposition = decomposition
        self.disjoint_union = disjoint_union
        self.recursion = recursion
        # TODO: Add assertions for assumptions made about each type of strategy.
        self.formal_step = formal_step
        self.back_maps = back_maps
        self.forward_maps = forward_maps

    def _error_string(self, parent, children, strat_type,
                      length, parent_total, children_total):
        error = "Insane " + strat_type + " Strategy Found!\n"
        error += "Found at length {} \n".format(length)
        error += "The parent tiling was:\n{}\n".format(parent.__repr__())
        error += "It produced {} many things\n".format(length)
        error += "The children were:\n"
        for obj in children:
            error += obj.__repr__()
            error += "\n"
        error += "They produced {} many things\n\n".format(children_total)
        return error


    def sanity_check(self, length, of_length=None):
        if of_length is None:
            raise ValueError("of_length is undefined.")
        if self.complement_verified:
            return ("Don't use complement_verified, its dangerous.")

        number_perms = of_length(self.eqv_path_objects[0], length)
        for obj in self.eqv_path_objects[1:]:
            eqv_number = of_length(obj, length)
            if number_perms != eqv_number:
                return self._error_string(self.eqv_path_objects[0],
                                          [obj],
                                          "Equivalent",
                                          length,
                                          number_perms,
                                          eqv_number)
        if self.disjoint_union:
            child_objs = [child.eqv_path_objects[0] for child in self.children]
            total = 0
            for obj in child_objs:
                total += of_length(obj, length)
            if number_perms != total:
                return self._error_string(self.eqv_path_objects[0],
                                          child_objs,
                                          "Batch",
                                          length,
                                          number_perms,
                                          total)
        if self.decomposition:
            if not self.has_interleaving_decomposition():
                child_objs = [child.eqv_path_objects[0] for child in self.children]
                total = 0
                for part in partitions_of_n_of_size_k(length, len(child_objs)):
                    subtotal = 1
                    for obj, partlen in zip(child_objs, part):
                        if subtotal == 0:
                            break
                        subtotal *= of_length(obj, partlen)
                    total += subtotal
                if number_perms != total:
                    return self._error_string(self.eqv_path_objects[0],
                                              child_objs,
                                              "Decomposition",
                                              length,
                                              number_perms,
                                              total)

    def has_interleaving_decomposition(self):
        if self.back_maps is None:
            return False
        mixing = False
        bmps1 = [{c.i for c in dic.values()} for dic in self.back_maps]
        bmps2 = [{c.j for c in dic.values()} for dic in self.back_maps]
        for i in range(len(self.back_maps)):
            for j in range(len(self.back_maps)):
                if i != j:
                    if (bmps1[i] & bmps1[j]) or (bmps2[i] & bmps2[j]):
                        mixing = True
        if mixing:
            return True
        return False

class InsaneTreeError(Exception):
    pass

class ProofTree(object):
    def __init__(self, root):
        if not isinstance(root, ProofTreeNode):
            raise TypeError("Root must be a ProofTreeNode.")
        self.root = root
        self._of_length_cache = {}

    def _of_length(self, obj, length):
        if obj not in self._of_length_cache:
            self._of_length_cache[obj] = {}

        number = self._of_length_cache[obj].get(length)

        if number is None:
            number = len(list(obj.gridded_perms_of_length(length)))
            self._of_length_cache[obj][length] = number

        return number

    def print_equivalences(self):
        for node in self.nodes():
            print("===============")
            print(node.label)
            for o in node.eqv_path_objects:
                print(o.__repr__())
                print()

    def to_old_proof_tree(self):
        from .ProofTree import ProofTree as OldProofTree
        old_proof_tree = OldProofTree(self._to_old_proof_tree_node(self.root))
        return old_proof_tree


    def _to_old_proof_tree_node(self, root):
        from .ProofTree import ProofTreeNode as OldProofTreeNode
        relation = ""
        for x in root.eqv_explanations:
            relation = relation + x
        return OldProofTreeNode(root.formal_step,
                                root.eqv_path_objects[0].to_old_tiling(),
                                root.eqv_path_objects[-1].to_old_tiling(),
                                relation,
                                root.label,
                                children=[self._to_old_proof_tree_node(x) for x in root.children],
                                recurse=root.back_maps,
                                strategy_verified=root.strategy_verified)

    def to_json(self):
        """Return json of old proof tree class."""
        return self.to_old_proof_tree().to_json()

    def pretty_print(self, file=sys.stderr):
        """Pretty print using olf proof tree class."""
        self.to_old_proof_tree().pretty_print(file=file)

    def get_genf(self):
        """Try to enumerate using olf proof tree class."""
        return self.to_old_proof_tree().get_genf()

    def nodes(self, root=None):
        if root is None:
            root = self.root
        yield root
        for child in root.children:
            for node in self.nodes(root=child):
                yield node

    def number_of_nodes(self):
        return len(list(self.nodes))

    def number_of_objects(self):
        count = 0
        for node in self.nodes():
            count += len(node.eqv_path_objects)
        return count

    def sanity_check(self, length=8, raiseerror=True):
        overall_error = ""
        for node in self.nodes():
            error = node.sanity_check(length, self._of_length)
            if error is not None:
                if raiseerror:
                    raise InsaneTreeError(error)
                else:
                    overall_error += error
        if overall_error:
            return False, overall_error
        else:
            return True, "Sanity checked, all good at length {}".format(length)

    @classmethod
    def from_comb_spec_searcher(cls, root, css):
        if not isinstance(root, tree_searcher_node):
            raise TypeError("Requires a tree searcher node, treated as root.")
        proof_tree = ProofTree(ProofTree.from_comb_spec_searcher_node(root, css))
        proof_tree._recursion_fixer(css)
        return proof_tree

    def _recursion_fixer(self, css, root=None, in_labels=None):
        if root is None:
            root = self.root
        if in_labels is None:
            in_labels = list(self.non_recursive_in_labels())
        if root.recursion:
            in_label = root.eqv_path_labels[0]
            out_label = in_label
            for eqv_label in in_labels:
                if css.equivdb.equivalent(in_label, eqv_label):
                    out_label = eqv_label
                    break
            assert css.equivdb.equivalent(in_label, out_label)

            eqv_path = css.equivdb.find_path(in_label, out_label)
            eqv_objs = [css.objectdb.get_object(l) for l in eqv_path]
            eqv_explanations = [css.equivdb.get_explanation(x, y) for x, y in zip(eqv_path[:-1], eqv_path[1:])]

            root.eqv_path_labels = eqv_path
            root.eqv_path_objects = eqv_objs
            root.eqv_explanations = eqv_explanations

        for child in root.children:
            self._recursion_fixer(css, child, in_labels)

    def non_recursive_in_labels(self, root=None):
        if root is None:
            root = self.root
        if not root.recursion:
            yield root.eqv_path_labels[0]
        for child in root.children:
            for x in self.non_recursive_in_labels(child):
                yield x

    @classmethod
    def from_comb_spec_searcher_node(cls, root, css, in_label=None):
        if not isinstance(root, tree_searcher_node):
            raise TypeError("Requires a tree searcher node, treated as root.")
        label = root.label
        if in_label is None:
            in_label = root.label
        else:
            assert css.equivdb.equivalent(root.label, in_label)
        children = root.children

        if not children:
            eqv_ver_label = css.equivalent_strategy_verified_label(in_label)
            if eqv_ver_label is not None:
                #verified!
                eqv_path = css.equivdb.find_path(in_label, eqv_ver_label)
                eqv_objs = [css.objectdb.get_object(l) for l in eqv_path]
                eqv_explanations = [css.equivdb.get_explanation(x, y) for x, y in zip(eqv_path[:-1], eqv_path[1:])]

                formal_step = css.objectdb.verification_reason(eqv_ver_label)
                return ProofTreeNode(label, eqv_path, eqv_objs,
                                     eqv_explanations, strategy_verified=True,
                                     formal_step=formal_step)
            else:
                #recurse! we reparse these at the end, so recursed labels etc are not interesting.
                return ProofTreeNode(label, [in_label],
                                    [css.objectdb.get_object(in_label)],
                                    formal_step="recurse",
                                    recursion=True)
        else:
            start, ends = css.rule_from_equivence_rule(root.label,
                                                       tuple(c.label for c in root.children))
            formal_step = css.ruledb.explanation(start, ends)
            back_maps = css.ruledb.get_back_maps(start, ends)

            eqv_path = css.equivdb.find_path(in_label, start)
            eqv_objs = [css.objectdb.get_object(l) for l in eqv_path]
            eqv_explanations = [css.equivdb.get_explanation(x, y) for x, y in zip(eqv_path[:-1], eqv_path[1:])]

            strat_children = []
            for next_label in ends:
                for child in root.children:
                    if css.equivdb.equivalent(next_label, child.label):
                        sub_tree = ProofTree.from_comb_spec_searcher_node(child, css, next_label)
                        strat_children.append(sub_tree)
                        break
            if back_maps is not None:
                #decomposition!
                return ProofTreeNode(label, eqv_path, eqv_objs,
                                     eqv_explanations, decomposition=True,
                                     back_maps=back_maps,
                                     formal_step=formal_step,
                                     children=strat_children)
            else:
                #batch!
                if "Complement" in formal_step:
                    return ProofTreeNode(label, eqv_path, eqv_objs,
                                         eqv_explanations,
                                         complement_verified=True,
                                         formal_step=formal_step)
                return ProofTreeNode(label, eqv_path, eqv_objs,
                                     eqv_explanations, disjoint_union=True,
                                     formal_step=formal_step,
                                     children=strat_children)
