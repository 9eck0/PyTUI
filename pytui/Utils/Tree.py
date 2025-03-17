"""
Base implementation of a multi-children generic tree.
"""

from collections import deque
from typing import Collection, Generic, TypeVar


T = TypeVar('T')


class Tree(Generic[T]):

    def __init__(self, value: T = None):
        self.value: T = value
        self.parent: Tree | None = None
        # Uses a read-only property accessor to deter user code changing this variable to an unsupported object
        self._children: list[Tree] = []

    def __iter__(self, algo='dfs'):
        algo = algo.strip().lower()
        if algo not in ('dfs', 'bfs'):
            algo = 'dfs'

        if algo == 'bfs':
            return self.traverse_bfs()
        else:
            return self.traverse_dfs()

    #region ======== Properties ========

    @property
    def children(self):
        return self._children

    #endregion

    #region ======== Manipulation Methods ========

    def add_child(self, child, sort=False, sort_key=None, reversed_sort=False):
        if not isinstance(child, Tree):
            child = Tree(child)
        child.parent = self
        self._children.append(child)
        if sort:
            if sort_key is None:
                sort_key = lambda node: node.value
            self._children.sort(key=sort_key, reverse=reversed_sort)

    def add_children(self, children: Collection, sort=False, sort_key=None, reversed_sort=False):
        for child in children:
            self.add_child(child)
        if sort:
            if sort_key is None:
                sort_key = lambda node: node.value
            self._children.sort(key=sort_key, reverse=reversed_sort)

    def depth(self):
        return len(list(self.traverse_ancestors()))

    def find(self, value):
        for node in self.traverse_bfs():
            if node.value is value:
                return node
        return None

    def get_root(self):
        node = self
        while not node.is_root():
            node = node.parent
        return node

    def is_ancestor_of(self, other):
        for ancestor in other.traverse_ancestors():
            if ancestor is self:
                return True
        return False

    def is_descendant_of(self, other):
        for ancestor in self.traverse_ancestors():
            if ancestor is other:
                return True
        return False

    def is_descendant_of_value(self, value):
        for ancestor in self.traverse_ancestors():
            if ancestor.value is value:
                return True
        return False

    def is_leaf(self):
        return len(self._children) == 0

    def is_root(self):
        return self.parent is None

    def pop(self, preserve_children=True):
        """
        Detach the current node from the tree, creating an orphan tree with current node as root.

        Optionally, unlink all children from current node and promote them to children of parent node.
        If there is no parent node (i.e. this is the root node), all children will become their independent tree.
        In such a case, make sure to keep a reference to children nodes before performing this operation.

        :param preserve_children: False to alienate this node and promote all children to parent node.
        :return: The current detached node.
        """

        if self.parent is not None:
            self.parent._children.remove(self)
        if not preserve_children:
            # promote children to parent node to unlink all children node
            for child in self._children:
                child.parent = self.parent
            if isinstance(self.parent, Tree):
                # if parent is not None
                self.parent.add_children(self._children)
            # Do not perform in-place clear(), due to possible outside referencing of this list before calling pop()
            # Otherwise the user code will lose references to this node's children once cleared.
            self._children = []
        self.parent = None
        return self

    def sort_tree(self, key=None, reverse=False):
        """
        Sort all children of the current tree/subtree.

        If a key function is given, the sorting algorithm will use values provided by the function for each child.
        The default key function is: "lambda node: node.value"

        :param key: key function to provide a sorting value for each child node
        :param reverse: whether to sort in descending order
        """
        if key is None:
            key = lambda node: node.value
        self._children.sort(key=key, reverse=reverse)
        for child in self._children:
            child.sort_tree(key=key, reverse=reverse)

    #endregion

    #region ======== Traversal Methods ========

    def traverse_ancestors(self):
        ancestor = self.parent
        while ancestor is not None:
            yield ancestor
            ancestor = ancestor.parent

    def traverse_bfs(self):
        """
        Create a generator to perform a breadth-first search (BFS) traversal over the current node and all its
        children.

        Breadth-first search will prioritize traversing through all nodes of a depth level first before going to
        the next level, traversing through children of previous-level nodes in order.
        """
        traversal_nodes = deque(self)
        while len(traversal_nodes) > 0:
            next_node = traversal_nodes.popleft()
            traversal_nodes.extend(next_node._children)
            yield next_node

    def traverse_dfs(self):
        """
        Create a generator to perform a depth-first search (DFS) traversal over the current node and all its children.

        Depth-first search will prioritize traversing through children nodes in order, by finding a branch's leaf node
        before backtracking and finding the next leaf node, until exhausted.
        """
        yield self
        for child in self._children:
            yield child.traverse_dfs()

    def dfs_previous(self):
        def rightmost_leaf(node):
            while len(node.children) > 0:
                node = node.children[-1]
            return node

        if self.parent is None:
            # Root node case: loops back to rightmost leaf
            return rightmost_leaf(self)

        current_branch_index = self.parent.children.index(self)
        if current_branch_index == 0:
            # Straightforward case: current node is first child => parent node is previous node
            return self.parent
        else:
            # Backtracks to nearest leaf node to the left
            return rightmost_leaf(self.parent.children[current_branch_index-1])

    def dfs_next(self):
        if len(self.children) > 0:
            # Straightforward case: go to first child
            return self.children[0]

        # Leaf node case: backtracks to nearest branch to the right
        traversal_node = self.parent
        prev_node = self
        while traversal_node is not None:
            next_branch_index = traversal_node.children.index(prev_node) + 1
            if next_branch_index < len(traversal_node.children):
                return traversal_node.children[next_branch_index]
            traversal_node = traversal_node.parent

        # This return is reached when this is the rightmost leaf node: loops back to root node
        return traversal_node

    #endregion
