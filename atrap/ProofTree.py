import sys

#from permuta import Perm, PermSet

from grids import JsonAble, Tiling


__all__ = ["ProofTree", "ProofTreeNode"]


class ProofTreeNode(JsonAble):
    def __init__(self,
                 formal_step,
                 in_tiling,
                 out_tiling,
                 relation,
                 identifier,
                 children=None,
                 recurse=False):
        self.formal_step = formal_step
        self.in_tiling = in_tiling
        self.out_tiling = out_tiling
        self.relation = relation
        self.identifier = identifier
        self.children = [] if children is None else list(children)
        self.recurse = recurse

    @classmethod
    def _from_attr_dict(cls, attr_dict):
        formal_step = attr_dict["formal_step"]
        in_tiling = Tiling._from_attr_dict(attr_dict["in_tiling"])
        out_tiling = Tiling._from_attr_dict(attr_dict["out_tiling"])
        relation = attr_dict["relation"]
        identifier = attr_dict["identifier"]
        children = map(cls._from_attr_dict, attr_dict["children"])
        recurse = attr_dict["recurse"]
        return cls(formal_step,
                   in_tiling,
                   out_tiling,
                   relation,
                   identifier,
                   children,
                   recurse)

    def _get_attr_dict(self):
        attr_dict = {}
        attr_dict["formal_step"] = self.formal_step
        attr_dict["in_tiling"] = self.in_tiling._get_attr_dict()
        attr_dict["out_tiling"] = self.out_tiling._get_attr_dict()
        attr_dict["relation"] = self.relation
        attr_dict["identifier"] = self.identifier
        attr_dict["children"] = [child._get_attr_dict() for child in self.children]
        attr_dict["recurse"] = self.recurse
        return attr_dict


class ProofTree(JsonAble):
    _NODE_CLASS = ProofTreeNode
    __PRETTY_PRINT_DICT = dict(L="└─────", pipe="│     ", T="├─────", empty="      ")

    def __init__(self, root):
        self.root = root

    @classmethod
    def _from_attr_dict(cls, attr_dict):
        root = cls._NODE_CLASS._from_attr_dict(attr_dict["root"])
        return cls(root)

    def _get_attr_dict(self):
        attr_dict = {}
        attr_dict["root"] = self.root._get_attr_dict()
        return attr_dict

    def pretty_print(self, file=sys.stdout):
        legend = [["label counter:", 0]]
        self._pretty_print(self.root, 0, legend, file=file)
        for label, tilings in legend:
            if isinstance(tilings, int):
                continue
            print(file=file)
            print("Label:", label, file=file)
            print(file=file)
            in_tiling, out_tiling = tilings
            print(in_tiling, file=file)
            if out_tiling:
                if out_tiling != in_tiling:
                    print("We use his sibling for the next strategy", file=file)
                    print(out_tiling, file=file)

    def _pretty_print(self, root, depth, legend, prefix="root: ", tail=False, file=sys.stdout):
        tp_L = ProofTree.__PRETTY_PRINT_DICT["L"]
        tp_pipe = ProofTree.__PRETTY_PRINT_DICT["pipe"]
        tp_tee = ProofTree.__PRETTY_PRINT_DICT["T"]
        tp_empty = ProofTree.__PRETTY_PRINT_DICT["empty"]
        label_counter = legend[0][1]
        print(prefix, label_counter, sep="", file=file)
        legend.append([label_counter, (root.in_tiling, root.out_tiling)])
        legend[0][1] += 1
        for subtree_number in range(len(root.children)-1):
            self._pretty_print(root.children[subtree_number],
                               depth+1,
                               legend,
                               prefix[:-6] + (tp_pipe if tail else tp_empty) + tp_tee,
                               True,
                               file)
        if len(root.children) > 1:
            self._pretty_print(root.children[-1],
                               depth+1,
                               legend,
                               prefix[:-6] + (tp_pipe if tail else tp_empty) + tp_L,
                               False,
                               file)
