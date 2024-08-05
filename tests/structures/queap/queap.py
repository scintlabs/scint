from . import Tree


class Element:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.in_list = True

    def __lt__(self, other):
        return self.key < other.key


class QueapNode:
    def __init__(self, key=None, value=None):
        self.keys = [key] if key is not None else []
        self.values = [value] if value is not None else []
        self.children = []
        self.parent = None

    def is_leaf(self):
        return len(self.children) == 0

    def add_key_value(self, key, value):
        for i, k in enumerate(self.keys):
            if key < k:
                self.keys.insert(i, key)
                self.values.insert(i, value)
                return
        self.keys.append(key)
        self.values.append(value)


class Queap:
    def __init__(self):
        self.n = 0
        self.k = 0
        self.linked_list = []
        self.tree = Tree()
        self.min_l = None

    @staticmethod
    def new():
        return Queap()

    def insert(self, key, value):
        element = Element(key, value)
        if not self.linked_list:
            self.min_l = element
        self.linked_list.append(element)
        if element < self.min_l:
            self.min_l = element
        self.n += 1

    def minimum(self):
        if not self.linked_list and self.tree.root.keys:
            return self.tree.find_min()
        if not self.linked_list:
            raise IndexError("Queap is empty")
        if self.tree.root.keys:
            tree_min = self.tree.find_min()
            return min(self.min_l.key, tree_min[0]), (
                self.min_l.value if self.min_l.key < tree_min[0] else tree_min[1]
            )
        return self.min_l.key, self.min_l.value

    def delete(self, key):
        for i, element in enumerate(self.linked_list):
            if element.key == key:
                del self.linked_list[i]
                if element == self.min_l:
                    self.min_l = min(self.linked_list, default=None)
                self.n -= 1
                return
        if self.linked_list:
            self._move_list_to_tree()
        node = self._find_node(self.tree.root, key)
        if node:
            self.tree.delete_leaf(node)
            self.n -= 1
            self.k -= 1

    def delete_min(self):
        if not self.linked_list and not self.tree.root.keys:
            raise IndexError("Queap is empty")
        if self.linked_list:
            min_element = min(self.linked_list)
            self.linked_list.remove(min_element)
            self.n -= 1
            if min_element == self.min_l:
                self.min_l = min(self.linked_list, default=None)
            return min_element.key, min_element.value
        min_key, min_value = self.tree.find_min()
        self.delete(min_key)
        return min_key, min_value

    def _move_list_to_tree(self):
        for element in self.linked_list:
            self.tree.insert(element.key, element.value)
        self.k = self.n
        self.linked_list.clear()
        self.min_l = None

    def _find_node(self, node, key):
        if key in node.keys:
            return node
        if node.is_leaf():
            return None
        for i, k in enumerate(node.keys):
            if key < k:
                return self._find_node(node.children[i], key)
        return self._find_node(node.children[-1], key)
