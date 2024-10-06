"""

"""

from typing import Dict, Sequence

from Utils.MathHelper import norm, sign


class ComparisonTreeND:
    """
    A multidimensional vector comparison tree.

    The vector key value is a sequence of the vector's components.
    ComparisonTreeND is built by component-wise comparison of vectors.
    Larger-dimension vectors require more operations for comparison, in the order of O(2^D),
    where D is the dimensionality of the key vectors.
    """

    def __init__(self, value, key_vector: Sequence):
        self.value = value
        self.key = key_vector
        self._parent: "ComparisonTreeND | None" = None
        self._children: "Dict[tuple:ComparisonTreeND]" = {}
        self._length = 1

    def add(self, value, key_vector: Sequence, overwrite=True):
        """

        :param value:
        :param key_vector:
        :param overwrite:
        :return:
        """

        if len(key_vector) != len(self.key):
            raise AttributeError(
                "Attempting to insert child with mismatched dimensionality: expects {0}D, got {1}D."
                .format(len(self.key), len(key_vector))
            )

        key_vector = tuple(key_vector)
        if key_vector == self.key:
            # The current node is same as comparison, overwrite
            if overwrite or self.value is None:
                self.value = value
            return overwrite
        else:
            return self._add_node(ComparisonTreeND(value, key_vector))

    def _add_node(self, node: "ComparisonTreeND", overwrite=False):
        """
        (Internal function)
        Adds a tree node to this node's children hierarchy.
        :param node: The node to add.
        :param overwrite: Whether to overwrite the current node with the given node if they match,
                          as well as child nodes.
        :return: Whether a node has been added or not (e.g. overwriting existing node).
        """
        direction_key = self.compare(node.key)
        if not any(direction_key):
            # Current key is same as new node, overwrite & add children to current node
            appended_node = False
            if overwrite or self.value is None:
                self.value = node.value
                for child_node in node._children.values():
                    appended_node |= self._add_node(child_node)
            return appended_node
        elif direction_key in self._children:
            # Child direction already occupied; pass new node to that child for addition
            return self._children[direction_key]._add_node(node)
        else:
            # Add as child of current node
            node._parent = self
            self._children[direction_key] = node
            self._change_length(len(node))
            return True

    def _change_length(self, delta: int):
        """
        (Internal function)
        Changes the current node's length value and propagates the change to its parents in the tree hierarchy.
        :param delta: The amount to change.
        """
        self._length += delta
        if self._parent is not None:
            self._parent._change_length(delta)

    def compare(self, key_vector: Sequence[int | float]):
        """
        Calculates the components' signs of the vector formed from the current node's key to the given vector.

        Example:
            Current node's key: (3, 5, 2);
            Comparison vector:  (7, 4, 2);
            Result:             (1, -1, 0).
        :param key_vector: A vector of same dimension to compare this node with.
        :return: A list of int unit values (-1, 0, or 1) representing the signs of the comparison vector's components.
        """
        return sign(*self.distance_vector(key_vector))

    def distance(self, key_vector: Sequence[int | float]):
        """
        Calculates the distance between the current vector key and the given vector of same dimension.
        :param key_vector: A vector of same dimension to compare this node with.
        :return: The float value of the calculated distance.
        """
        return norm(*self.distance_vector(key_vector))

    def distance_vector(self, key_vector: Sequence[int | float]):
        """
        Returns the vector formed between the current tree node's key and a given vector.
        :param key_vector: A vector of same dimension to compare this node with.
        :return: A list of values representing the distance vector.
        """
        if len(key_vector) != len(self.key):
            raise AttributeError(
                "Attempting to compare vector with mismatched dimensionality: expects {0}D, got {1}D."
                .format(len(self.key), len(key_vector))
            )
        return [key_vector[i] - self.key[i] for i in range(len(self.key))]

    def remove(self):
        # Remove self from parent node
        parent_node = self._parent
        self._parent = None
        if parent_node is not None:
            parent_node._children.pop(self.key)
            # Propagate length change to parents in the tree hierarchy
            parent_node._change_length(-len(self))

        # Promote the closest child with the longest length to current position
        promo_key = max(self._children, key=lambda k: len(self._children[k]))
        promo_node: "ComparisonTreeND" = self._children[promo_key]
        self._children.pop(promo_key)

        # Add existing children to current node
        for other_key, other_node in self._children:
            promo_node._add_node(other_node)

        if parent_node is not None:
            parent_node._add_node(promo_node)

        # Disposal: return to initial state
        self._children.clear()
        self._length = 1

    def seek(self, key_vector: Sequence, closest_approx=False):
        if len(key_vector) != len(self.key):
            raise AttributeError(
                "Attempting to compare vector with mismatched dimensionality: expects {0}D, got {1}D."
                .format(len(self.key), len(key_vector))
            )

        key_vector = tuple(key_vector)
        if key_vector == self.key:
            return self
        else:
            direction_key = self.compare(key_vector)
            if direction_key in self._children:
                return self._children[direction_key].seek(key_vector, closest_approx)
            elif closest_approx:
                return self
        return None

    def __len__(self):
        return self._length

    def __str__(self):
        return "({0} : {1})".format(self.key, self.value)

    def __repr__(self):
        return "{0} {{1}}".format(str(self), "\n".join(self._children.values()))
