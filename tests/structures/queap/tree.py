class Node:
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


class Tree:
    def __init__(self):
        self.root = Node()

    def insert(self, key, value):
        if len(self.root.keys) == 3:
            new_root = Node()
            new_root.children.append(self.root)
            self.root.parent = new_root
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.is_leaf():
            node.add_key_value(key, value)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 3:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, index):
        new_node = Node()
        child = parent.children[index]
        parent.add_key_value(child.keys[1], child.values[1])
        parent.children.insert(index + 1, new_node)
        new_node.keys = child.keys[2:]
        new_node.values = child.values[2:]
        child.keys = child.keys[:1]
        child.values = child.values[:1]
        if not child.is_leaf():
            new_node.children = child.children[2:]
            child.children = child.children[:2]
        new_node.parent = parent
        for c in new_node.children:
            c.parent = new_node

    def delete_leaf(self, node):
        if not node.is_leaf():
            raise ValueError("Can only delete leaf nodes")
        parent = node.parent
        if parent is None:  # node is root
            if len(node.keys) > 1:
                node.keys.pop(0)
                node.values.pop(0)
            else:
                self.root = Node()
        else:
            index = parent.children.index(node)
            parent.children.pop(index)
            if len(parent.children) < 2:
                self._merge(parent)

    def _merge(self, node):
        if node.parent is None:  # node is root
            if len(node.children) == 1:
                self.root = node.children[0]
                self.root.parent = None
            return
        parent = node.parent
        index = parent.children.index(node)
        if index > 0 and len(parent.children[index - 1].keys) < 3:
            left_sibling = parent.children[index - 1]
            left_sibling.add_key_value(parent.keys[index - 1], parent.values[index - 1])
            left_sibling.keys.extend(node.keys)
            left_sibling.values.extend(node.values)
            left_sibling.children.extend(node.children)
            for child in node.children:
                child.parent = left_sibling
            parent.keys.pop(index - 1)
            parent.values.pop(index - 1)
            parent.children.pop(index)
        elif (
            index < len(parent.children) - 1
            and len(parent.children[index + 1].keys) < 3
        ):
            right_sibling = parent.children[index + 1]
            node.add_key_value(parent.keys[index], parent.values[index])
            node.keys.extend(right_sibling.keys)
            node.values.extend(right_sibling.values)
            node.children.extend(right_sibling.children)
            for child in right_sibling.children:
                child.parent = node
            parent.keys.pop(index)
            parent.values.pop(index)
            parent.children.pop(index + 1)
        else:
            raise ValueError("Unable to merge nodes")
        if len(parent.children) < 2:
            self._merge(parent)

    def find_min(self):
        node = self.root
        while node.children:
            node = node.children[0]
        return node.keys[0], node.values[0]
