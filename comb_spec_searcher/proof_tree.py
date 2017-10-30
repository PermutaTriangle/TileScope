from comb_spec_searcher import CombinatorialSpecificationSearcher
from .tree_searcher import Node as tree_searcher_node

class ProofTreeNode(object):
    def __init__(self, label, eqv_path_labels, eqv_path_objects,
                 eqv_formal_step="", children=[], strategy_verified=False,
                 comlement_verified=False, decomposition=False,
                 disjoint_union=False, recursion=False, formal_step="",
                 back_maps=None, forward_maps=None, dependencies=[]):
        self.label = label
        self.eqv_path_labels = eqv_path_labels
        self.eqv_path_objects = eqv_path_objects
        self.eqv_formal_step = eqv_formal_step

        self.children = children
        self.strategy_verified = strategy_verified
        self.complement_verified = comlement_verified
        self.decomposition = decomposition
        self.disjoint_union = disjoint_union
        self.recursion = recursion
        # TODO: Add assertions for assumptions made about each type of strategy.
        self.formal_step = formal_step
        self.back_maps = []
        self.forward_maps = forward_map
        self.dependencies = dependencies

class ProofTree(object):
    def __init__(self, root):
        if not isinstance(root, ProofTreeNode):
            raise TypeError("Root must be a ProofTreeNode.")
        self.root = root

    @classmethod
    def from_comb_spec_searcher(root, css, in_label=None):
        if not isinstance(css, CombinatorialSpecificationSearcher):
            raise TypeError("Requires a CombinatorialSpecificationSearcher.")
        if not isinstance(tree, tree_searcher_node):
            raise TypeError("Requires a tree searcher node, treated as root.")
        label = root.label
        if in_label is None:
            label = root.label
        else:
            label = in_label
            assert css.equivdb.equivalent(root.label, in_label)
        children = root.children

        if not children:
            eqv_ver_label = css.equivalent_strategy_verified_label(label)
            if eqv_ver_label is not None:
                eqv_exp, eqv_path = css.equivdb.get_explanation(label,
                                                                eqv_ver_label,
                                                                with_path=True)
                eqv_objs = [css.objectdb.get_object(l) for l in eqv_path]
                formal_step = css.objectdb.verification_reason(eqv_ver_label)
                return ProofTreeNode(label, eqv_path, eqv_objs, eqv_exp,
                                     strategy_verified=True,
                                     formal_step=formal_step)
            else:
                #recurse! we reparse these at the end, so recursed labels etc are not interesting.
                return ProofTreeNode(label, [label], [self.obj])
